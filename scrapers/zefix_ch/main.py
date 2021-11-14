import mimetypes
import re
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core
import Hrcintapp


from lxml import html
from absl import app, flags
import json


class ZefixCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.zefix.ch/"
    DB_NAME = "zefix_ch"

    OFFSET = 39
    WILDCARD = "__"
    MAX_ENTRIES = 1

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
    }

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/docs/")

        with open("registry_offices.json", "r") as f:
            registry_offices = list(json.loads(f.read()))

        # for result in registry_offices:
        #     print(result)
        start_url = "https://www.zefix.ch/ZefixREST/api/v1/firm/search.json"

        json_data = {
            "name": self.WILDCARD,
            "languageKey": "en",
            "deletedFirms": "true",
            "searchType": "exact",
            "maxEntries": self.MAX_ENTRIES,
            "offset": self.OFFSET,
        }

        async with self.http_request(
            start_url, headers=self.HEADERS, json_data=json_data
        ) as response:
            resp = await response.json()
            for result in resp["list"]:
                await self.enqueue_request(result["cantonalExcerptWeb"])

    async def handle_request(self, request):
        parsed = await self.parse(request)
        if parsed is not None:
            await self.enqueue_result(parsed)

    async def parse(self, url):
        table_results = []
        entry = {}
        attachments = {}
        try:
            if "chregister.ch" in url:
                async with self.http_request(url, headers=self.HEADERS) as response:
                    nonces = response.headers["Content-Security-Policy"]
                    nonce = nonces.split(" ")[-1].replace("nonce-", "")
                    # print(nonce)

                tree = html.fromstring(html=await response.text())
                view_state = tree.xpath(
                    '//input[@type="hidden" and @name="javax.faces.ViewState"]/@value'
                )

                form_data = {
                    "javax.faces.partial.ajax": "true",
                    "javax.faces.source": "idAuszugForm:auszugContentPanel",
                    "primefaces.ignoreautoupdate": "true",
                    "javax.faces.partial.execute": "idAuszugForm:auszugContentPanel",
                    "javax.faces.partial.render": "idAuszugForm:auszugContentPanel",
                    "idAuszugForm:auszugContentPanel": "idAuszugForm:auszugContentPanel",
                    "idAuszugForm:auszugContentPanel_load": "true",
                    "idAuszugForm": "idAuszugForm",
                    "javax.faces.ViewState": view_state,
                    "primefaces.nonce": nonce,
                }

                headers = {
                    "Faces-Request": "partial/ajax",
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }

                cookie = response.headers["SET-Cookie"].split(";")[0]
                _url = re.sub(r"jsession.+", "", str(response.url))
                final_url = _url + cookie.lower()
                async with self.http_request(
                    final_url,
                    headers=headers,
                    post_data=form_data,
                    query_params=response.headers,
                ) as resp:
                    tree = html.fromstring(
                        html=bytes(await resp.text(), encoding="utf-8")
                    )
                    tables = tree.xpath("//table")

                    for table in tables:

                        theads = table.xpath(".//thead/tr/th")
                        trs = table.xpath(".//tbody/tr")
                        results = {}
                        keys = []
                        for th_val in theads:
                            texts = th_val.xpath(".//text()")
                            key = "".join(texts).strip()
                            keys.append(key)
                            results[key] = []
                        for tr in trs:
                            tds = tr.xpath(".//td")

                            for idx, td_val in enumerate(tds):
                                values = td_val.xpath(".//text()")
                                value = "".join(values).strip()
                                results[keys[idx]].append(value)
                        table_results.append(results)

                entry = {"url": url, "result": table_results}

            elif "prestations" in url:
                prestations_url = (
                    "https://prestations.vd.ch/pub/101266/api/public/hrcexcerpts/"
                )
                if "CHE" not in url:
                    logger.info(f"no CHE in url {url}")

                else:

                    uid = re.search(r"(CHE.+)$", url)[1]

                    headers = {
                        "Accept-Language": "en-US,en;q=0.9",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                        # 'X-XSRF-TOKEN': 'bf16c53b-f1bc-4485-adfc-769be3f9a210'
                    }
                    body = {
                        "rcentId": "",
                        "lng": "EN",
                        "rad": True,
                        "companyOfsUid": uid,
                        "extraitTravail": True,
                        "admOrderDirection": "ASC",
                        "order": "R",
                    }

                    async with self.http_request(
                        prestations_url, headers=headers, json_data=body
                    ) as resp:
                        result = await resp.json()

                entry = {"url": url, "result": result}

            elif "hrcintapp/" in url:
                url = url.replace("externalCompanyReport", "companyReport") + "&lang=EN"
                async with self.http_request(url, headers=self.HEADERS) as resp:
                    result = Hrcintapp.Hrcintapp(await resp.text()).table_results
                entry = {"url": url, "result": result}
            else:
                logger.info("Cannot found in a scraper")

            return entry, attachments
        except:
            logger.exception(url)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["url"]
            async with self.get_doc(collection, _id) as doc:
                doc.update(entry)

            for file_name, file_content in attachments.items():
                extension = mimetypes.guess_type(file_name)[0]
                if extension is not None:
                    await doc.attachment(file_name).save(file_content, extension)
                else:
                    logger.exception(file_name)


def main(_):
    scraper = ZefixCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

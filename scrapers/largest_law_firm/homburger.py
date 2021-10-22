import json
import mimetypes

from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class HomburgerPeople(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://homburger.ch/"
    DB_NAME = "homburger_people"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en/team")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//a[@class="lawyers__lawyer__link"]/@href')
        for link in links:
            logger.info(f"Initializing {link=}")
            await self.enqueue_request(link)

    async def handle_request(self, request):
        request_url = urljoin(self.ROOT_URL, request)
        async with self.http_request(request_url) as response:
            parsed = await self.parse(request_url, await response.text())
            if parsed is not None:
                await self.enqueue_result(parsed)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["url"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():
                extension = mimetypes.guess_type(file_name)[0]
                if extension is not None:
                    await doc.attachment(file_name).save(file_content, extension)
                else:
                    logger.debug(f"No file extension {file_name}")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)
            person_id_tree = tree.xpath('//script[@id ="__NEXT_DATA__"]/text()')[0]
            person_id = re.search(r"\"ID\"\:\"(\d+)\"", person_id_tree).group(1)

            # entries
            person = self.get_name(url)

            img_link = tree.xpath("//picture/source/@srcset")[0]

            publications_raw = await self.query_publications_api(person_id)
            publications = publications_raw["data"]["dd_publications_list"]["result"]

            english_entry = await self.person_api("en", person)
            german_entry = await self.person_api("de", person)
            attachments = {}

            entry = {
                "url": url,
                "person_id": person_id,
                "person": person,
                "EN": english_entry,
                "DE": german_entry,
            }

            fname, fcontent = await self.get_img(img_link, url)
            attachments[fname] = fcontent

            for publication in publications:
                title = publication["acf"]["title"]
                try:
                    pdf_url = publication["acf"]["document"]["attachment_url"]
                    u = pdf_url.split("/")
                    true_pdf_link = urljoin(
                        "https://homburger.ch/api/ms/", f"{u[0]}/{u[1]}/_/{u[-1]}"
                    )
                    dl_link, fcontent = await self.get_file(true_pdf_link)
                    attachments[dl_link] = fcontent
                    logger.info(f"DOWNLOADING . . . {title}")
                except:
                    logger.info(f"{title} has no pdf file")

            return entry, attachments
        except:
            logger.exception(url)

    def get_name(self, url):
        name = re.search(r"team\/([\w-]+)", url)
        return name.group(1)

    async def person_api(self, lang, name):
        url = f"https://homburger.ch/_next/data/FVamggN94htdv7GyvegFZ/{lang}/team/{name}.json?lang={lang}&path=team&path={name}"
        async with self.http_request(url) as resp:
            return await resp.json()

    async def query_publications_api(self, person_id):
        payload = {
            "operationName": "publications_filter",
            "variables": {
                "lang": "en",
                "expertise": None,
                "author": [int(person_id)],
                "search": None,
                "cursor": "0",
                "pageSize": 1000,
            },
            "query": "fragment publication on Publications {\n  ID\n  lang\n  slug\n  translations {\n    de\n    en\n    __typename\n  }\n  post_date\n  acf {\n    title\n    text\n    external_link {\n      target\n      title\n      url\n      __typename\n    }\n    document {\n      ID\n      post_title\n      attachment_url\n      __typename\n    }\n    authors {\n      ... on Publications_Acf_authors_list_group_5f1812df4b8d3_authors_extern {\n        extern {\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on Publications_Acf_authors_list_group_5f1812df4b8d3_authors_intern {\n        intern {\n          ref {\n            slug\n            acf {\n              name\n              surname\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery publications_filter($lang: String!, $author: [Int!], $expertise: [Int!], $search: String, $cursor: String, $pageSize: Int) {\n  dd_publications_list(lang: $lang, pageSize: $pageSize, cursor: $cursor, search: $search, filterBy: {acf__expertise: {in: $expertise}, acf__authors__ref: {in: $author}}) {\n    cursor\n    hasMore\n    result {\n      ...publication\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        async with self.http_request(
            "https://api.homburger.ch/", json_data=payload
        ) as resp:
            return await resp.json()

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def get_img(self, dl_link, url):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return file_url, await resp.read()

    async def get_bulletin(self, dl_link):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        dl_url = dl_link.replace("\\", "")
        async with self.http_request(dl_url) as resp:
            resp_text = await resp.text()
            try:
                tree = html.fromstring(html=resp_text)
                content = " ".join(
                    tree.xpath('//section[@class="bulletin__content"]//text()')
                )
                return content
            except:
                logger.exception(dl_url)


def main(_):
    scraper = HomburgerPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

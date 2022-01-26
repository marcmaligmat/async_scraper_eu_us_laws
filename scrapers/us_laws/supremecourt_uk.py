from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin


class SupremeCourtUK(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.supremecourt.uk/"
    START_URL = "https://www.supremecourt.uk/decided-cases/index.html"
    DB_NAME = "supreme_court_uk"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        async with self.http_request(self.START_URL) as response:
            tree = html.fromstring(html=await response.text())

            # get years link
            years = tree.xpath(
                '//div[@id="primaryContent"]/div/div/p/a[contains(@href, ".html")]/@href'
            )
            # for year in years[::-1]:
            for y in years:

                year_link = urljoin("https://www.supremecourt.uk/decided-cases/", y)
                logger.info(f"Initializing {year_link=}")
                await self.enqueue_request(year_link)

    async def handle_request(self, request):
        async with self.http_request(request) as response:
            tree = html.fromstring(html=await response.text())
            rows = tree.xpath('//table[@id="caselist-test"]/tbody/tr')

            entry = {}
            for r in rows:
                date = r.xpath("normalize-space(.//td[1]/text())")
                neutral_citation = r.xpath("normalize-space(.//td[2]/text())")
                case_id = r.xpath("normalize-space(.//td[3]/text())")
                case_name = r.xpath("normalize-space(.//td[4]/a/@title)")

                info_link = r.xpath("normalize-space(.//td[4]/a/@href)")

                pdf_link = await self.get_more_info(info_link)

                entry = {
                    "case_id": case_id,
                    "neutral_citation": neutral_citation,
                    "date": date,
                    "case_name": case_name,
                    "pdf_link": pdf_link,
                }
                parsed = await self.parse(entry)
                if parsed is not None:
                    await self.enqueue_result(parsed)

    async def parse(self, entry):
        try:
            attachments = {}
            fname, fcontent = await self.get_file(entry["pdf_link"])
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(entry["case_id"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["case_id"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():

                try:
                    if "getattachment" in file_name:
                        await doc.attachment(file_name).save(file_content, "image/jpeg")
                    else:
                        await doc.attachment(file_name).save(
                            file_content, "application/pdf"
                        )
                    logger.info(f"Downloading {file_name}")
                except:
                    logger.debug(f"Cannot download {file_name}")

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def get_more_info(self, link):
        l = urljoin("https://www.supremecourt.uk/cases/", link)
        async with self.http_request(l) as response:
            t = html.fromstring(html=await response.text())
            return urljoin(
                self.ROOT_URL,
                t.xpath('//a[contains(@title, "Judgment (PDF)")]/@href')[0],
            )


def main():
    scraper = SupremeCourtUK()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

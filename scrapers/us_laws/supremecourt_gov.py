from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin


class SupremecourtGov(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.supremecourt.gov/opinions/slipopinion/21"
    DB_NAME = "supremecourt_gov"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        async with self.http_request(self.ROOT_URL) as response:
            tree = html.fromstring(html=await response.text())

            # get years link
            years = tree.xpath(
                '//div[@id="ctl00_ctl00_MainEditable_mainContent_upButtons"]//a/@href')
            # for year in years[::-1]:
            # remove last link
            for year_link in years[:-1]:
                url = urljoin(
                    'https://www.supremecourt.gov/opinions/slipopinion/', year_link)
                logger.info(f"Initializing {url=}")
                await self.enqueue_request(url)

    async def handle_request(self, request):
        logger.info(f"Scraping {request}")
        async with self.http_request(request) as response:
            tree = html.fromstring(html=await response.text())

            # use postman to get the exact xpath
            # chrometool is not enough
            rows = tree.xpath(
                '//div[@class="alt-table-responsive"]/table/tr')

            for row in rows:
                pdf_link = row.xpath('./td[4]/a/@href')
                if (pdf_link):
                    date = row.xpath('./td[2]/text()')[0]
                    docket_nr = row.xpath('./td[3]/text()')[0]

                    revision = row.xpath('./td[5]/a/@href')
                    if revision:
                        revision = urljoin(
                            'https://www.supremecourt.gov/', revision[0])
                    else:
                        revision = None

                    entry = {
                        "docket_nr": docket_nr,
                        "pdf_file": urljoin('https://www.supremecourt.gov/', pdf_link[0]),
                        "date": date,
                        "revision": revision
                    }
                    parsed = await self.parse(entry)
                    if parsed is not None:
                        await self.enqueue_result(parsed)

    async def parse(self, entry):
        try:
            attachments = {}
            fname, fcontent = await self.get_file(entry['pdf_file'])
            attachments[fname] = fcontent

            if entry['revision']:
                fname, fcontent = await self.get_file(entry['revision'])
                attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(entry["docket_nr"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["docket_nr"]
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


def main():
    scraper = SupremecourtGov()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin


class CaselawFindlaw(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://caselaw.findlaw.com/court/us-supreme-court"
    DB_NAME = "caselaw_findlaw"

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
            years = tree.xpath('//div[@id="brwsopncal"]/ul/li/a/@href')
            # for year in years[::-1]:
            for year_link in years:
                logger.info(f"Initializing {year_link=}")
                await self.enqueue_request(year_link)

    async def handle_request(self, request):
        async with self.http_request(request) as response:
            tree = html.fromstring(html=await response.text())
            links = tree.xpath(
                '//div[@class="caselawCases section"]//table//tbody/tr/td/a/@href')

            for l in links:
                logger.info(f"Second level link:  {l}")
                async with self.http_request(l) as response:
                    tree = html.fromstring(html=await response.text())
                    desc = tree.xpath(
                        '//div[@class="caselawTitle section"]/h1//text()')
                    description = ' '.join(desc)

                    docket = tree.xpath(
                        '//center[@id="target-full"]//h3[2]/text()')[0]

                    dates = tree.xpath(
                        '//center[@id="target-full"]//h3[3]//text()')

                    content = tree.xpath(
                        '//div[@class="caselawContent section"]//text()')

                    entry = {
                        "description": description,
                        "docket_nr": docket,
                        "dates": dates,
                        "content": content
                    }
                    parsed = await self.parse(entry)
                    if parsed is not None:
                        await self.enqueue_result(parsed)

    async def parse(self, entry):
        try:
            attachments = {}
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


def main():
    scraper = CaselawFindlaw()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

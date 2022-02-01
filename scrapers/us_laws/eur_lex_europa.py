from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

# german eng french italian


class EurLexEurpa(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://eur-lex.europa.eu/"
    START_URL = "https://eur-lex.europa.eu/oj/2021/direct-access-search-result.html?ojYearSearch=2021&ojSeriesSearch=ALL&ojSeries=ALL"
    DB_NAME = "eur_lex_europa"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        await self.enqueue_request(self.START_URL)

    async def handle_request(self, request):
        try:
            logger.info(f"Going Page Link: {request}")
            async with self.http_request(request) as response:
                t = html.fromstring(html=await response.text())

                # next_page = t.xpath('//img[@title="Show next document"]/../@href')[0]
                # # table rows
                trows = t.xpath("//tbody/tr")

                for trow in trows[4:5]:

                    try:

                        date = trow.xpath("./td[1]/text()")[0]
                        leg_links = trow.xpath("./td[2]/a/@href")
                        for leg_link in leg_links:
                            entry = {}
                            attachments = {}

                            f_link = urljoin(
                                self.ROOT_URL, leg_link.replace("./../../", "")
                            )

                            entry = {
                                "url": f_link,
                                "date": date,
                            }
                            logger.info(f"Scraping {f_link}")
                            fname, fcontent = await self.get_html(f_link)
                            attachments[fname] = fcontent

                            parsed = await self.parse(entry, attachments)
                            if parsed is not None:
                                await self.enqueue_result(parsed)
                    except:
                        logger.exception(f"Error on {date}")

                # if next_page:
                #     await self.enqueue_request(next_page)
        except:
            logger.exception(request)

    async def parse(self, entry, attachments):
        try:
            return entry, attachments
        except:
            logger.exception(entry["url"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["url"]
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

    async def get_html(self, link):
        if link:
            logger.info(f"Downloading PDF file of {link}")
            async with self.http_request(link) as response:
                t = html.fromstring(html=await response.text())

            pdf_link = t.xpath(
                '//li/a[contains(@id,"format_language_table_PDF_EN")]/@href'
            )[0]

            return await self.get_file(
                urljoin(self.ROOT_URL, pdf_link.replace("./../../../", ""))
            )


def main():
    scraper = EurLexEurpa()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

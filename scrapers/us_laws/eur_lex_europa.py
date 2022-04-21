from lxml import html

import dj_scrape.core


from loguru import logger

from urllib.parse import urljoin

# german eng french italian


class EurLexEuropa(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://eur-lex.europa.eu/"
    START_URL = "https://eur-lex.europa.eu/oj/2021/direct-access-search-result.html?ojYearSearch=2021&ojSeriesSearch=ALL&ojSeries=ALL"
    DB_NAME = "eur_lex_europa"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 2

    async def initialize(self):
        await super().initialize()

        async with self.http_request(self.START_URL) as response:
            t = html.fromstring(html=await response.text())

        years = t.xpath('//select[@id="daily-ojYear"]/option/text()')

        for y in years:
            logger.debug(f"Scraping for YEAR {y}")
            url = f"https://eur-lex.europa.eu/oj/2021/direct-access-search-result.html?ojYearSearch={y}&ojSeriesSearch=ALL&ojSeries=ALL"
            await self.enqueue_request(url)

    async def handle_request(self, request):
        try:
            async with self.http_request(request) as response:
                _t = html.fromstring(html=await response.text())

            # # table rows
            trows = _t.xpath("//tbody/tr")
            for trow in trows:

                try:
                    date = trow.xpath("./td[1]/text()")[0]
                    # legislation links and parsing
                    leg_links = trow.xpath("./td[2]/a/@href")
                    leg_names = trow.xpath("./td[2]/a/text()")
                    await self.parse_trows(date, leg_links, leg_names)

                    # for information and notices
                    info_links = trow.xpath("./td[3]/a/@href")
                    info_names = trow.xpath("./td[3]/a/text()")
                    await self.parse_trows(date, info_links, info_names)

                except:
                    logger.exception(f"Error on {date}")

            # next page
            try:
                next_page = _t.xpath('//a[@title="Next Page"]/@href')[0]
            except:
                next_page = None

            if next_page is not None:
                next_p_link = urljoin(self.ROOT_URL, next_page.replace("./../../", ""))
                logger.debug(f"Moving to next page {next_p_link}")
                await self.enqueue_request(next_p_link)

        except:
            logger.exception(request)

    async def parse_trows(self, date, links, names):
        for i, leg_link in enumerate(links):
            entry = {}
            attachments = {}

            leg_name = names[i]

            f_link = urljoin(self.ROOT_URL, leg_link.replace("./../../", ""))

            entry = {
                "url": f_link,
                "leg_name": leg_name,
                "date": date,
            }
            logger.info(f"Scraping {date} {leg_name} {f_link}")

            # languages
            langs = ["EN", "FR", "IT", "DE"]

            for lang in langs:
                # get PDF files
                fname, fcontent = await self.follow_link(f_link, lang, "PDF")
                attachments[fname] = fcontent

                # get HTML files
                fname, fcontent = await self.follow_link(f_link, lang, "HTML")
                attachments[fname] = fcontent

            parsed = await self.parse(entry, attachments)
            if parsed is not None:
                await self.enqueue_result(parsed)

    async def parse(self, entry, attachments):
        try:
            return entry, attachments
        except:
            logger.exception(entry["url"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["date"] + " " + entry["leg_name"]
            async with self.get_doc(collection, _id) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():
                try:
                    logger.info(f"Downloading {file_name}")

                    if "HTML" in file_name:
                        file_type = "text/html"
                    else:
                        file_type = "application/pdf"

                    await doc.attachment(file_name).save(file_content, file_type)

                except:
                    logger.debug(f"Cannot download {file_name}")

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def follow_link(self, link, lang, file_type):
        if link:
            logger.info(f"Try to Download {file_type} files of {link}")
            async with self.http_request(link) as response:
                t = html.fromstring(html=await response.text())

            try:
                pdf_link = t.xpath(
                    f'//li/a[contains(@id,"format_language_table_{file_type}_{lang}")]/@href'
                )[0]
                return await self.get_file(
                    urljoin(self.ROOT_URL, pdf_link.replace("./../../../", ""))
                )
            except:
                return "", ""


def main():
    scraper = EurLexEuropa()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

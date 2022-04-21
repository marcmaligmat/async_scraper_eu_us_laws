from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin


class GermanSupremeCourt(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://juris.bundesgerichtshof.de/"
    DB_NAME = "german_supreme_court"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(
            self.ROOT_URL, "/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en"
        )

        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())

            # get years link
            years = tree.xpath('//div[@id="kaljahr"]/div/a/@href')
            # years in reverse order (ascending)
            for year in years[::-1]:
                print(year)
                await self.enqueue_request(
                    "https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/" + year
                )

    async def handle_request(self, request):

        request_url = urljoin(self.ROOT_URL, request)
        async with self.http_request(request_url) as response:
            tree = html.fromstring(html=await response.text())
            pdf_links = tree.xpath(
                '//form[@name="list"]/table/tbody/tr/td/span/a[2]/@href'
            )

            file_numbers = tree.xpath(
                '//form[@name="list"]/table/tbody/tr/td/span/a[1]/text()'
            )

            senates = tree.xpath('//td[@class="ESpruchk"]/text()')
            dates = tree.xpath('//td[@class="EDatum"]/text()')

            # capture see also in every td element
            see_alsos = []
            for see in tree.xpath('//td[@class="ETitel"]'):
                see_alsos.append(see.xpath("./a/@href"))

            for i, link in enumerate(pdf_links):
                nr = file_numbers[i]
                parsed = await self.parse(nr, link, senates[i], dates[i], see_alsos[i])
                if parsed is not None:
                    await self.enqueue_result(parsed)

            has_next_page = tree.xpath(
                '//td[@class="pagenumber"]//img[contains(@alt,"nächste Seite")]'
            )

            if has_next_page:
                # use postman to get the value
                next_link = tree.xpath(
                    '//td[@class="ETitelKopf"]/table/tr/td[5]/a[1]/@href'
                )
                next_link = (
                    "https://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/"
                    + next_link[0]
                )
                logger.info(f"Next page {next_link}")
                await self.handle_request(next_link)

    async def parse(self, nr, link, senate, date, see_also):
        try:
            entry = {"nr": nr, "senate": senate, "date": date, "see_also": see_also}

            attachments = {}
            real_image_link = urljoin(
                self.ROOT_URL + "cgi-bin/rechtsprechung/",
                link,
            )
            fname, fcontent = await self.get_file(real_image_link)
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(nr)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["nr"]
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
    scraper = GermanSupremeCourt()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

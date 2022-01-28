from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin


class SupremecourtFR(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.courdecassation.fr/"
    START_URL = "https://www.courdecassation.fr/en/recherche-judilibre?sort=date-desc&items_per_page=30"
    DB_NAME = "supremecourt_fr"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        await self.enqueue_request(self.START_URL)

    async def handle_request(self, request):
        logger.info(f"Going Page Link: {request}")
        async with self.http_request(request) as response:
            t = html.fromstring(html=await response.text())
            next_page = urljoin(
                self.ROOT_URL,
                t.xpath('//li[@class="pager__item pager__item--next"]/a/@href')[0],
            )

            links = t.xpath('//p[contains(@class,"lien-voir")]/a/@href')

            for l in links:
                url = urljoin(self.ROOT_URL, l)
                logger.info(f"Initializing {url=}")
                try:
                    logger.info(f"Scraping {url}")
                    async with self.http_request(url) as response:
                        t = html.fromstring(html=await response.text())

                        title_texts = t.xpath(
                            '//div[@class="decision-content decision-content--main"]/h1//text()'
                        )
                        title = " ".join([i.strip() for i in title_texts])

                        pdf_link = t.xpath(
                            '//p[contains(@class,"decision-export-link")]/a/@href'
                        )[0]

                        entry = {
                            "title": title,
                            "pdf_link": urljoin(self.ROOT_URL, pdf_link),
                        }
                        parsed = await self.parse(entry)
                        if parsed is not None:
                            await self.enqueue_result(parsed)
                except:
                    logger.exception(url)

            if next_page:
                await self.enqueue_request(next_page)

    async def parse(self, entry):
        try:
            attachments = {}
            fname, fcontent = await self.get_file(entry["pdf_link"])
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(entry["title"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["title"]
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
    scraper = SupremecourtFR()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

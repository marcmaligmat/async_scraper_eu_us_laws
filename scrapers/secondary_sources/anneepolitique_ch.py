# -*- coding: UTF-8 -*-

import mimetypes

from urllib.parse import unquote
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core

from lxml import html


class AnneepolitiqueCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://anneepolitique.swiss/"
    DB_NAME = "anneepolitique"
    PAGE = 1

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()

        while True:
            url = f"https://anneepolitique.swiss/articles?page={self.PAGE}&start_date=1965-01-01&stop_date=3000-01-01"
            await self.enqueue_request(url)
            self.PAGE += 1

    async def handle_request(self, url):
        async with self.http_request(url) as response:
            tree = html.fromstring(html=await response.text())
        articles = tree.xpath('//article[@class="article"]')

        for article in articles:
            parsed = await self.parse(url, article)
            if parsed is not None:
                await self.enqueue_result(parsed)

    async def parse(self, url, tree):
        try:
            attachments = {}
            name = tree.xpath("./a/@name")[0]
            logger.info(f"initializing article name {name}")

            summary = tree.xpath("./div/div/p//text()")
            refer_links = tree.xpath(".//a/@href")

            topic = tree.xpath(
                './/div[contains(@class,"article-meta")]/div/h3/a/text()'
            )[0]
            subtopic = tree.xpath(
                './/div[contains(@class,"article-meta")]//div[contains(@class,"subtopic")]/h4/a/text()'
            )[0]
            sources = tree.xpath('.//ul[@class="references"]//a/@href')
            catchwords = tree.xpath(
                './/dl[@class="metadata dl-horizontal"]/dt[contains(text(),"Schlagworte")]/following-sibling::dd[1]/ul//span/text()'
            )
            date = tree.xpath(
                './/dl[@class="metadata dl-horizontal"]/dt[contains(text(),"Datum")]/following-sibling::dd[1]/text()'
            )

            process_type = tree.xpath(
                './/dl[@class="metadata dl-horizontal"]/dt[contains(text(),"Prozesstyp")]/following-sibling::dd[1]//text()'
            )

            bus_nr = tree.xpath(
                './/dl[@class="metadata dl-horizontal"]/dt[contains(text(),"Geschäftsnr")]/following-sibling::dd[1]//text()'
            )
            actor = tree.xpath(
                './/dl[@class="metadata dl-horizontal"]/dt[contains(text(),"Akteure")]/following-sibling::dd[1]//span/text()'
            )
            author = tree.xpath('normalize-space(.//span[@class="author"]/text())')
            updated_at = tree.xpath(
                'normalize-space(.//span[@class="last_change_at"]/text())'
            )
            for src in sources:
                # unquoted src
                u_src = unquote(src)
                cleaned_src = urljoin(
                    self.ROOT_URL, u_src.replace("/pdfjs/minimal?file=", "")
                )
                fname, fcontent = await self.get_file(cleaned_src)
                attachments[fname] = fcontent

            entry = {
                "name": name,
                "summary": summary,
                "refer_links": refer_links,
                "topic": topic,
                "subtopic": subtopic,
                "catchwords": catchwords,
                "date": date,
                "sources": sources,
                "process_type": process_type,
                "business_nr": bus_nr,
                "actor": actor,
                "author": author,
                "updated_at": updated_at,
            }

            return entry, attachments
        except:
            logger.exception(url)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["name"]
            async with self.get_doc(collection, _id) as doc:
                doc.update(entry)

            for file_name, file_content in attachments.items():
                extension = mimetypes.guess_type(file_name)[0]
                if extension is not None:
                    await doc.attachment(file_name).save(file_content, extension)
                else:
                    logger.exception(file_name)

    async def get_file(self, dl_link):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return dl_link, await resp.read()


def main():
    scraper = AnneepolitiqueCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

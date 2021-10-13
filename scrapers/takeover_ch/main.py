from absl import app, flags
from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class Takeover_ch(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.takeover.ch"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 4
        num_results_workers = 1
        http_pause_seconds = 0.05

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/transactions/all")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//article[@class="transaction list-item"]//a/@href')
        for link in links:
            await self.enqueue_request(link)

    async def handle_request(self, request):
        request_url = urljoin(self.ROOT_URL, request)
        async with self.http_request(request_url) as response:
            parsed = await self.parse(request_url, await response.text())
            if parsed is not None:
                await self.enqueue_result(parsed)

    async def handle_results(self, results):
        collection = await self.get_db("takeover_ch")
        for entry, files in results:
            url = entry["url"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in files.items():
                # second argument of save() method is the media-type, see
                # https://en.wikipedia.org/wiki/Media_type for examples
                await doc.attachment(file_name).save(file_content, "application/pdf")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)
            transaction = tree.xpath("//h2/text()")[0]
            descriptions = tree.xpath('//div[@class="lead"]/p/text()')
            trx_properties = tree.xpath('//aside[@class="descriptors"]/text()')
            links = tree.xpath('//article[contains(@class,"list-item")]//a/@href')
            decisions_date = tree.xpath(
                '//article[contains(@class,"list-item")]/div[@class="inner"]/span[1]/text()'
            )

            entry = {
                "url": url,
                "transaction": transaction,
                "descriptions": descriptions,
                "transaction_properties": trx_properties,
            }
            files = {}

            for n, dl_link in enumerate(l for l in links if "contentelements" in l):
                name, content = await self.get_pdf(
                    dl_link, url, decisions_date[n]
                )
                files[name] = content

            return entry, files
        except:
            logger.exception(url)

    async def get_pdf(self, dl_link, url, date):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        trx_number = self.get_trx_number(url)
        file_lang = self.get_file_lang(dl_link)
        file_url = dl_link.replace("\\", "")
        filename = f"nr{trx_number}-{date}-{file_lang}.pdf"
        async with self.http_request(file_url) as response:
            return filename, await response.read()

    def get_trx_number(self, url):
        number = re.search(r"\/nr\/(\d+)", url)
        return number[1]

    def get_file_lang(self, dl_link):
        language = re.search(r"\/lang\/([a-zA-Z]+)", dl_link)
        return language[1]


def main(_):
    scraper = Takeover_ch()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class EntscheidsucheCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://entscheidsuche.ch"
    DB_NAME = "entscheidsuche_ch"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/docs/")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//a[contains(@href,"/docs")]/@href')
        for link in links:
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
                file_extension = (
                    re.search(r"\.*?\w+$", file_name).group().replace(".", "")
                )
                if file_extension == "pdf":
                    file_extension = "application/pdf"

                await doc.attachment(file_name).save(file_content, file_extension)

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)
            file_links = tree.xpath(
                '//a[contains(@href,"/docs") and text() != "Parent Directory"]/@href'
            )

            attachments = {}

            for file_link in file_links:
                fname, fcontent = await self.get_file(file_link)
                attachments[fname] = fcontent

            entry = {"url": url}
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    async def get_file(self, dl_link):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        filename = dl_link
        async with self.http_request(file_url) as resp:
            return filename, await resp.read()


def main(_):
    scraper = EntscheidsucheCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

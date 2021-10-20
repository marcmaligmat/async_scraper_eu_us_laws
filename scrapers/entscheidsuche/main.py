
import mimetypes
import re
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core

from lxml import html
from absl import app, flags


class EntscheidsucheCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://entscheidsuche.ch"
    DB_NAME = "entscheidsuche_ch"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/docs/")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//a[contains(@href,"/docs")]/@href')

        for link in links:
            if not link.endswith("/"):
                continue
            if link.endswith('/Sitemaps/'):
                continue
            if link.endswith('/Index/'):
                continue

            if "." in link:
                continue

            logger.info(f'initializing {link=}')
            request_url = urljoin(self.ROOT_URL, link)
            async with self.http_request(request_url) as response:
                response_text = await response.text()

            tree = html.fromstring(html=response_text)
            file_links = tree.xpath(
                '//a[contains(@href,"/docs") and text() != "Parent Directory"]/@href'
            )

            # get distinct links
            distinct_links = list(dict.fromkeys(
                map(self.remove_extension, file_links)))

            for distinct_link in distinct_links:
                await self.enqueue_request(distinct_link)

    async def handle_request(self, request):
        parsed = await self.parse(request)
        if parsed is not None:
            await self.enqueue_result(parsed)

    async def parse(self, url):
        try:
            _url = urljoin(self.ROOT_URL, url)
            folder = re.search(r"\/docs\/([^\/]+)", url).group(1)
            _id = re.search(r"\/([^\/]+)$", url).group(1)

            entry = {
                "url": _url,
                "folder": folder,
                "id": _id,
            }
            attachments = {}

            attchment_links = [
                urljoin(self.ROOT_URL, url + '.json'),
                urljoin(self.ROOT_URL, url + '.html'),
                urljoin(self.ROOT_URL, url + '.pdf')
            ]

            for file_link in attchment_links:
                fname, fcontent = await self.get_file(file_link)
                attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["id"]
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

    def remove_extension(self, url):
        return re.sub(r'\.[^\.]+$', '', url)


def main(_):
    scraper = EntscheidsucheCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

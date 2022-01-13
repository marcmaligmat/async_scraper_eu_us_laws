import mimetypes
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core

from lxml import html


class GrundrechteCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://grundrechte.ch/"
    DB_NAME = "grundrechte_ch"
    START_URL = "https://grundrechte.ch/gerichtsurteile-titel.html"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()

        async with self.http_request(self.START_URL) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//li[contains(@class,"sibling")]/a/@href')

        for l in links:
            link = urljoin(self.ROOT_URL, l)
            await self.enqueue_request(link)

    async def handle_request(self, link):
        logger.info(f"initializing {link=}")

        async with self.http_request(link) as response:
            response_text = await response.text()

        tree = html.fromstring(html=response_text)
        parsed = await self.parse(link, tree)
        if parsed is not None:
            await self.enqueue_result(parsed)

    async def parse(self, url, tree):
        try:
            content = tree.xpath('//div[@class="box_F1CDCC"]//text()')
            reference = tree.xpath('//div[@class="ce_text last block"]/p/a/text()')
            r_url = tree.xpath('//div[@class="ce_text last block"]/p/a/@href')[0]
            reference_url = urljoin(self.ROOT_URL, r_url)
            r_content = await self.reference_text(reference_url)

            entry = {
                "url": url,
                "content": content,
                "reference": reference,
                "reference_url": reference_url,
                "reference_content": r_content,
            }
            attachments = {}

            # fname, fcontent = await self.get_file(file_link)
            # attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["url"]
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

    async def reference_text(self, link):
        async with self.http_request(link) as response:
            response_text = await response.text()

        _tree = html.fromstring(html=response_text)
        return _tree.xpath('//div[@class="box_F1CDCC"]//text()')


def main():
    scraper = GrundrechteCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

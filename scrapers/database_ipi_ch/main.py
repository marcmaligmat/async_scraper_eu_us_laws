from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

from post_data import post_data_from_oldest

import re
import json


class DatabaseIpiCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://database.ipi.ch"
    DB_NAME = "database_ipi_ch"
    PAGE_SIZE = 16

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        # changed pause second to 1.0 to avoid server disconnection default: 0.1
        http_pause_seconds = 0.3
        max_results_batch_size = 1

    async def initialize(self):
        self.cursor = "*"
        await super().initialize()
        start_url = urljoin(
            self.ROOT_URL, f"/database/resources/query/fetch?ps={self.PAGE_SIZE}"
        )
        await self.enqueue_request(start_url)

    async def handle_request(self, start_url):
        headers = {
            "content-type": "application/transit+json",
            "X-IPI-VERSION": "2.2.3",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        }

        while True:
            try:
                logger.info(f"Initializing {start_url=}")
                async with self.http_request(
                    start_url,
                    headers=headers,
                    json_data=post_data_from_oldest(self.PAGE_SIZE, self.cursor),
                ) as response:
                    resp = await response.json()
                    self.cursor = self.get_next_cursor(resp)
                    logger.info(
                        f"Initializing Cursor: {self.cursor} Page Size: {self.PAGE_SIZE}"
                    )
                    for result in resp["results"]:

                        parsed = await self.parse(result)
                        if parsed is not None:
                            await self.enqueue_result(parsed)

                    if not self.cursor:
                        logger.info("Cannot find next cursor, exiting scraper . . .")
                        break
            except:
                logger.exception(self.cursor, self.PAGE_SIZE)

    async def parse(self, result):
        attachments = {}
        entry = {}
        title = ""
        img_url = ""
        _db_id = result["markennummer__type_text_split_num"][0]

        try:
            # use ID if title is not available
            if "titel__type_text" in result:
                title = result["titel__type_text"][0]
            else:
                title = _db_id

            entry = {
                "id": result["markennummer__type_text_split_num"],
                "title": title,
                "cursor": self.cursor,
                "page_size": self.PAGE_SIZE,
                "result": result,
            }

            if "bild_screen_hash__type_string_mv" in result:
                img_url = urljoin(
                    self.ROOT_URL,
                    "database/resources/image/"
                    + result["bild_screen_hash__type_string_mv"][0],
                )

            fcontent = await self.get_file(img_url)
            attachments[title] = fcontent

        except Exception as e:
            logger.exception(e)

        return entry, attachments

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            _id = entry["title"]
            async with self.get_doc(collection, _id) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():
                await doc.attachment(file_name).save(file_content, "image/jpeg")

    async def get_file(self, dl_link):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return await resp.read()

    def get_next_cursor(self, response):
        cursor_result = response["metadataAsTransit"]
        cursor = cursor_result.replace("\\", "")
        return json.loads(cursor)["~#resultmeta"]["~:cursor"]["~#opt"]


def main(_):
    scraper = DatabaseIpiCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

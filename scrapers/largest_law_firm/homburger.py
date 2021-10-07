from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import aiohttp
import aiofiles

import base64
import os
import re


class Takeover_ch(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://homburger.ch/"
    NAME = "homburger_ch"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en/team")
        async with await self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath(
            '//a[@class="lawyers__lawyer__link"]/@href')
        for link in links:
            await self.enqueue_request(link)
            break

    async def handle_request(self, request):
        request_url = urljoin(self.ROOT_URL, request)
        async with await self.http_request(request_url) as response:
            parsed = await self.parse(request_url, await response.text())
            if parsed is not None:
                await self.enqueue_result(parsed)

    async def handle_results(self, results):
        collection = await self.get_db(self.NAME)
        for entry, files in results:
            url = entry["url"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in files.items():
                await doc.attachment(file_name).save(file_content, "application/pdf")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)

            # entries
            person = re.search(r"team\/(.+)", url).group(1)
            portrait = tree.xpath(
                '//div[contains(@class,"lawyer__portrait--screen")]//text()'
            )[0]

            career = tree.xpath('//div[@data-print="Career"]//text()')
            career = [" ".join(x) for x in zip(career[0::2], career[1::2])]

            area_of_expertise = tree.xpath(
                '(//div[contains(@class,"lawyer__expertise")])[1]//a/text()'
            )

            image_url = urljoin(
                self.ROOT_URL, tree.xpath("//picture/source/@srcset")[0]
            )
            bulletin_links = tree.xpath(
                '//div[@class="bulletin-teaser__content"]/a/@href'
            )

            bulletin_links = [urljoin(self.ROOT_URL, ele)
                              for ele in bulletin_links]

            bulletins = []
            for link in bulletin_links:
                response = await self.enqueue_request(link)
                tree = html.fromstring(html=await response.text)
                article = tree.xpath(
                    '//section[@class="bulletin__content"]//text()'
                )
                bulletins.append(article)

            entry = {
                "url": url,
                "person": person,
                "portrait": portrait,
                "career": career,
                "area_of_expertise": area_of_expertise,
                "bulletins": bulletins,
            }

            files = {"image": person}
            await self.save_image(image_url, person)

            return entry, files
        except:
            logger.exception(url)

    async def save_image(self, image_url, person):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f'{person}.jpg', mode='wb')
                    await f.write(await resp.read())
                    await f.close()


def main(_):
    scraper = Takeover_ch()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

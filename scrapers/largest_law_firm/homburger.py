from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class HomburgerPeople(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://homburger.ch/"
    DB_NAME = "homburger_people"

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

    async def handle_request(self, request):
        request_url = urljoin(self.ROOT_URL, request)
        async with await self.http_request(request_url) as response:
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
                await doc.attachment(file_name).save(file_content, "image/jpg")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)

            # entries
            person = self.get_name(url)

            img_link = tree.xpath("//picture/source/@srcset")[0]

            portrait = tree.xpath(
                '//div[contains(@class,"lawyer__portrait--screen")]//text()'
            )[0]

            career = tree.xpath('//div[@data-print="Career"]//text()')
            career = [x for x in zip(career[0::2], career[1::2])]

            area_of_expertise = tree.xpath(
                '(//div[contains(@class,"lawyer__expertise")])[1]//a/text()'
            )

            bulletin_links = tree.xpath(
                '//div[@class="bulletin-teaser__content"]/a/@href'
            )

            bulletins = []
            if bulletin_links:
                for link in bulletin_links:
                    content = await self.get_bulletin(link)
                    bulletins.append(content)

            entry = {
                "url": url,
                "person": person,
                "portrait": portrait,
                "career": career,
                "area_of_expertise": area_of_expertise,
                "bulletins": bulletins,
            }
            attachments = {}

            fname, fcontent = await self.get_img(img_link, url)
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    def get_name(self, url):
        name = re.search(r"team\/([\w-]+)", url)
        return name.group(1)

    async def get_img(self, dl_link, url):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        filename = self.get_name(url)
        async with await self.http_request(file_url) as resp:
            return filename, await resp.read()

    async def get_bulletin(self, dl_link):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        dl_url = dl_link.replace("\\", "")
        async with await self.http_request(dl_url) as resp:
            resp_text = await resp.text()
            try:
                tree = html.fromstring(html=resp_text)
                content = " ".join(
                    tree.xpath(
                        '//section[@class="bulletin__content"]//text()'
                    )
                )
                return content
            except:
                logger.exception(dl_url)


def main(_):
    scraper = HomburgerPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

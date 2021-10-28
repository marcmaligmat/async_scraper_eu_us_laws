import json
import mimetypes

from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class KellerhalsCarrardPeople(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.kellerhals-carrard.ch/"
    DB_NAME = "kellerhals_carrard_people"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en/people/index.php")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath(
            '//section[@class="people overview"]//span[@class="highlight-mark"]//a[contains(@href,"people")]/@href'
        )
        for link in links:
            logger.info(f"Initializing {link=}")
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
                extension = mimetypes.guess_type(file_name)[0]
                if extension is not None:
                    await doc.attachment(file_name).save(file_content, extension)

                elif "cv.php" in file_name:
                    await doc.attachment(file_name).save(
                        file_content, "application/pdf"
                    )
                else:
                    logger.debug(f"No file extension {file_name}")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)

            person = tree.xpath('(//span[@class="highlight-mark"])[1]/text()')[0]

            about = tree.xpath('(//span[@class="highlight-mark"])[2]/text()')[0]
            practice_areas = tree.xpath(
                '//a[contains(text(),"Practice areas")]/../../div//li/text()'
            )
            education = tree.xpath(
                '//a[contains(text(),"Education")]/../../div//li/text()'
            )
            experience = tree.xpath(
                '//a[contains(text(),"Experience / Career")]/../../div//li/text()'
            )
            further_activities = tree.xpath(
                '//a[contains(text(),"Further activities")]/../../div//li/text()'
            )
            publications = tree.xpath(
                '//a[contains(text(),"Publications / Presentations")]/../../div//li/text()'
            )

            # entries
            entry = {
                "url": url,
                "person": person,
                "about": about,
                "practice_areas": practice_areas,
                "education": education,
                "experience": experience,
                "further_activities": further_activities,
                "publications": publications,
            }
            attachments = {}
            cv_link = tree.xpath('//li/a[contains(text(),"Download CV")]/@href')[0]
            fname, fcontent = await self.get_fcontent(cv_link, url)
            attachments[fname] = fcontent

            img_link = tree.xpath('//div[@class="people-image-container"]/img/@src')[0]
            fname, fcontent = await self.get_fcontent(img_link, url)
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    async def get_fcontent(self, dl_link, url):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return file_url, await resp.read()


def main(_):
    scraper = KellerhalsCarrardPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

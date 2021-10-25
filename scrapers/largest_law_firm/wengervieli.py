import json
import mimetypes

import requests

from absl import app, flags

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class WengervieliPeople(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://wengervieli.ch/"
    DB_NAME = "wengervieli_people"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en-us/team")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())

        links = tree.xpath(
            '//section[@class="team"]//div[@class="card person "]//a/@href')

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

                try:
                    if 'getattachment' in file_name:
                        await doc.attachment(file_name).save(file_content, 'image/jpeg')
                    else:
                        await doc.attachment(file_name).save(file_content, 'application/pdf')
                    logger.info(f"Downloading {file_name}")
                except:
                    logger.debug(f"Cannot download {file_name}")

    async def parse(self, url, response_text):
        try:
            tree = html.fromstring(html=response_text)

            name = ' '.join(tree.xpath(
                '//section[@class="details"]//h1/text()'))

            image_link = tree.xpath(
                '//section[@class="details"]//div[@class="right"]/img/@src')[0]

            description = tree.xpath('//div[@class="portrait"]//p/text()')
            career = tree.xpath(
                '//div[contains(@class,"resume")]//table[@class="werdegang"]//tr//td/text()')

            memberships = tree.xpath(
                '//div[contains(@class,"memberships")]//ul/li/text()')

            expertise = tree.xpath('//div[@class="expertise"]//a/text()')
            expertise_link = tree.xpath('//div[@class="expertise"]//a/@href')

            publications = tree.xpath(
                '//div[contains(@class,"journal")]/section[@class="publications"]//ul//li//h2/a/text()')

            publication_links = tree.xpath(
                '//div[contains(@class,"journal")]/section[@class="publications"]//ul//li//h2/a/@href')

            publications_with_link = dict(zip(publication_links, publications))

            expertise_entry = []
            for i, pub_link in enumerate(expertise_link):
                exp = {
                    "expertise": expertise[i],
                    "expertise_link": expertise_link[i],
                    "expertise_text": await self.get_expertise_texts(pub_link)
                }
                expertise_entry.append(exp)

            entry = {
                "url": url,
                "name": name,
                "description": description,
                "memberships": memberships,
                "career": career,
                "expertise": expertise_entry,
                "publications": publications_with_link

            }

            attachments = {}
            real_image_link = urljoin(
                'https://www.wengervieli.ch/getattachment/', image_link.replace('aspx', 'jpg'))
            fname, fcontent = await self.get_file(real_image_link)
            attachments[fname] = fcontent

            for link in publication_links:
                fname, fcontent = await self.get_publications_pdf(link)
                attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    async def get_expertise_texts(self, link):
        complete_link = urljoin(self.ROOT_URL, link)

        async with self.http_request(complete_link) as response:
            tree = html.fromstring(html=await response.text())
            return tree.xpath('//section[@class="content"]//text()')

    async def get_publications_pdf(self, link):
        try:
            true_url = urljoin(
                'https://www.wengervieli.ch/getattachment/', link)
            logger.info(f"DOWNLOADING . . . {true_url}")
            return await self.get_file(true_url)
        except:
            logger.info(f"{true_url} has no pdf file")

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""


def main(_):
    scraper = WengervieliPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

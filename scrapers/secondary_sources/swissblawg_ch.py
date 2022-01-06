import mimetypes
import re
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core

from lxml import html
from absl import app, flags

# issue is when different references
# https://swissblawg.ch/2021/11/ncsc-halbjahresbericht-meldet-zunahme-von-cyberbetrugsfaellen.html#more-12623
# https://www.ncsc.admin.ch/ncsc/de/home.html
class SwissblawgCH(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://swissblawg.ch/"
    DB_NAME = "swissblawg_ch"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        url = self.ROOT_URL
        await self.enqueue_request(url)

    async def handle_request(self, url):
        while True:
            try:
                logger.info(f"Scraping page number {url}")
                async with self.http_request(url) as response:
                    tree = html.fromstring(html=await response.text())
                links = tree.xpath('//a[contains(@class,"read-more")]/@href')
                has_next_page = tree.xpath("//a[contains(text(),'Nächster')]")
                current_page = int(
                    tree.xpath('//span[@class="page-numbers current"]/text()')[0]
                )

                if has_next_page:
                    next_page = current_page + 1
                    url = f"https://swissblawg.ch/page/{next_page}"
                else:
                    break

                for link in links:
                    async with self.http_request(link) as response:
                        response_text = await response.text()

                    tree = html.fromstring(html=response_text)
                    parsed = await self.parse(link, tree)
                    if parsed is not None:
                        await self.enqueue_result(parsed)

            except Exception as e:
                logger.debug(f"There was an error: {e}")

    async def parse(self, url, tree):
        attachments = {}
        try:

            try:
                # content for every paragraph
                p_content = tree.xpath('//div[@class="entry-content"]//p')
                content = []
                [content.append(c.xpath(".//text()")) for c in p_content]
                ref = p_content[0].xpath(".//a/@href")[0]
                ref_data = await self.reference_text(ref)
            except IndexError:
                logger.info(f"{url}: Cannot find a link in first Paragraph")
                ref = ""
                ref_data = ""
                links = tree.xpath('//div[@class="entry-content"]//p//a/@href')
                for l in links:
                    if "newsd" in l:
                        fname, fcontent = await self.get_file(l)
                        attachments[fname] = fcontent

            title = tree.xpath('//h1[@class="entry-title"]//text()')
            published_date = tree.xpath('//time[@class="entry-date published"]/text()')
            author = tree.xpath('//span[@class="author-name"]/text()')

            entry = {
                "url": url,
                "content": content,
                "title": title,
                "published_date": published_date,
                "author": author,
                "reference_url": ref,
                "reference": ref_data,
            }

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
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "cookie": 'PHPSESSID=5ntotortdm3pqikr90ctn9bsv4; visid_incap_734262=+fkz6XQvTCCHxc/+SuwsSjrinWEAAAAAQUIPAAAAAAD+obaAYmCigxgfAimHTn3t; _pk_testcookie..undefined=1; _pk_testcookie.1.cee3=1; incap_ses_936_734262=LYThbeL+fR8s9Z2QfFf9DF7tnWEAAAAAMnYHUM/kDV3gTqTna7hYOw==; JSESSIONID=C27859E1FB58BDDEDDA6E29544A93C71; _pk_ref.1.cee3=["","",1637739872,"https://github.com/"]; _pk_ses.1.cee3=1; _JSESSIONID=9288FDEAB658757A795394B537512EDE; _pk_id.1.cee3=068792152fb7fc8d.1637737025.2.1637740578.1637739872.',
        }
        async with self.http_request(link, headers=headers) as response:
            response_text = await response.text()

        _tree = html.fromstring(html=response_text)
        return _tree.xpath('//div[@class="middle"]/div/div[@class="content"]//text()')


def main(_):
    scraper = SwissblawgCH()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

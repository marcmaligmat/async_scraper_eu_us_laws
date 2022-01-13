import mimetypes

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

import re


class WalderwyssPeople(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://www.walderwyss.com/"
    DB_NAME = "walderwyss_people"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.1
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en/lawyers")
        async with self.http_request(start_url) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//a[@class="lawyers__overview-name"]/@href')

        # good example is https://www.walderwyss.com/en/lawyers/roger.ammann [3:4]
        for link in links:
            logger.info(f"Initializing {link=}")
            await self.enqueue_request(link)

    async def handle_request(self, request):
        request_url = urljoin(self.ROOT_URL, request)
        name = re.search("\/([^\/]+)$", request).group(1)

        parsed = await self.parse(request_url, name)
        if parsed is not None:
            await self.enqueue_result(parsed)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["EN"]["url"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():
                extension = mimetypes.guess_type(file_name)[0]
                if extension is not None:
                    await doc.attachment(file_name).save(file_content, extension)
                else:
                    logger.debug(f"No file extension {file_name}")

    async def parse(self, url, name):
        """
        A list of different URL on different languages, including news and publications button text
        Change text on news/publications button according to language
        """
        languages = {
            "EN": {
                "link": "/en/lawyers/",
                "news_btn": "More News",
                "pub_btn": "Publications",
            },
            "DE": {
                "link": "/de/anwaelte/",
                "news_btn": "Mehr News",
                "pub_btn": "Publikationen",
            },
            "FR": {
                "link": "/fr/avocats/",
                "news_btn": "Plus News",
                "pub_btn": "Plus Publications",
            },
            "IT": {
                "link": "/it/avvocati/",
                "news_btn": "Di più News",
                "pub_btn": "Pubblicazioni",
            },
        }
        attachments = {}
        entry = {}
        for lang, val in languages.items():

            try:
                url = urljoin(self.ROOT_URL, val["link"] + name)
                logger.info(f"Initializing Another Language Link {url}")
                async with self.http_request(url) as response:
                    response_text = await response.text()

                tree = html.fromstring(html=response_text)

                # entries
                person = tree.xpath(
                    '(//h1[@class="main__row__col__name main__row__col__name-lawyer"]/text())[1]'
                )[0]
                description = tree.xpath(
                    '(//div[@class="bodytext__richtext"])[1]//text()'
                )

                cv_link = tree.xpath('//div[@class="download__container"]/a/@href')[0]

                news = await self.get_news(tree, val["news_btn"])
                publications = await self.get_pub(tree, val["pub_btn"])

                entry.update(
                    {
                        lang: {
                            "url": url,
                            "person": person,
                            "description": description,
                            "news": news,
                            "publications": publications,
                        }
                    }
                )

                fname, fcontent = await self.get_file(cv_link)
                attachments[lang + " " + fname] = fcontent

                for pub in publications:
                    if len(pub["pdf_link"]) > 0:
                        fname, fcontent = await self.get_file(pub["pdf_link"][0])
                        attachments[lang + " " + fname] = fcontent

            except:
                logger.exception(url)

        return entry, attachments

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def get_news(self, tree, text):
        more_news_btn = tree.xpath(f'//a[text()="{text}"]')
        news_list = []
        if len(more_news_btn) > 0:
            all_news_url = tree.xpath(f'//a[text()="{text}"]/@href')[0]
            all_news_url = urljoin(self.ROOT_URL, all_news_url)
            async with self.http_request(all_news_url) as response:
                _tree = html.fromstring(html=await response.text())
            news_urls = _tree.xpath('//li[@class="news__list-item"]/a/@href')

            for news_url in news_urls:
                news_list.append(await self.parse_news(news_url))
        else:
            news_urls = tree.xpath('//li[@class="news__list-item"]/a/@href')
            for news_url in news_urls:
                news_list.append(await self.parse_news(news_url))
            news_list.append(self.parse_news(news_url))

        return news_list

    async def parse_news(self, news_url):
        """
        This will move to its specific link about news
        Returning the news body title and url as a Dictionary
        """

        async with self.http_request(news_url) as response:
            _tree = html.fromstring(html=await response.text())
            title = _tree.xpath('//h1[@class="main__row__col__name"]/text()')
            body = _tree.xpath(
                '//div[@class="main__row__col__text bodytext__richtext"]//text()[normalize-space()]'
            )
            news = {"url": news_url, "title": title, "body": body}
            return news

    async def get_pub(self, tree, text):
        """
        Get Publications
        If the scraper sees "more publications" button it will follow its link
        If there is no "more publications" button, it will just get the internal publication
        """
        pub_list = []
        more_pub = tree.xpath(
            f'//div[@class="teaser__box"]/a[contains(text(),"{text}")]'
        )

        if len(more_pub) > 0:
            pub_links = tree.xpath(
                f'//div[@class="teaser__box"]/a[contains(text(),"{text}")]/@href'
            )
            all_pub = urljoin(self.ROOT_URL, pub_links[0])
            async with self.http_request(all_pub) as response:
                _tree = html.fromstring(html=await response.text())

            pub_articles = _tree.xpath('//div[@class="overview__publications"]/article')

            for article in pub_articles:
                pub_list.append(await self.parse_pub_article(article))

        else:
            pub_li = tree.xpath(
                f'//h2[@class="teaser__box-title" and text()="{text}"]/../ul//li'
            )

            for li in pub_li:
                title = li.xpath('/div/a[@class="publ__list-item-title"]/text()')
                description = li.xpath('/div[@class="publ__list-item-meta"]//text()')
                pdf_link = li.xpath("/a/@href")

                pub_list.append(
                    {"title": title, "description": description, "pdf_link": pdf_link}
                )
        return pub_list

    async def parse_pub_article(self, article):
        title = article.xpath('./div/h2[@class="publications__card-text-title"]/text()')
        description = article.xpath("./div/div/p//text()")
        pdf_link = article.xpath("./a/@href")

        publication = {"title": title, "description": description, "pdf_link": pdf_link}
        return publication


def main():
    scraper = WalderwyssPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

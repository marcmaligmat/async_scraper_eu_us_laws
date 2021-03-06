import mimetypes

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
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        start_url = urljoin(self.ROOT_URL, "/en/team")
        await self.enqueue_request(start_url)

    async def handle_request(self, request):
        async with self.http_request(request) as response:
            tree = html.fromstring(html=await response.text())
        links = tree.xpath('//a[@class="lawyers__lawyer__link"]/@href')

        # added to get the german name of a person in case they are different
        de_start_url = urljoin(self.ROOT_URL, "/de/team")
        async with self.http_request(de_start_url) as response:
            tree = html.fromstring(html=await response.text())
        de_links = tree.xpath('//a[@class="lawyers__lawyer__link"]/@href')

        for i, link in enumerate(links):
            logger.info(f"Initializing {link=}")
            request_url = urljoin(self.ROOT_URL, request)
            async with self.http_request(request_url) as response:
                parsed = await self.parse(link, await response.text(), de_links[i])
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
                else:
                    logger.debug(f"No file extension {file_name}")

    async def parse(self, url, response_text, de_link):
        try:
            self.img_link = ""
            tree = html.fromstring(html=response_text)

            # entries
            self.person = self.get_name(url)
            de_name = self.get_name(de_link)

            # usually the actual name of the lawyer
            page_title = self.get_page_title(tree)

            english_entry = await self.profile_page_api("en", self.person, page_title)
            german_entry = await self.profile_page_api("de", de_name, page_title)

            img_ = english_entry["dd_person"]["acf"]["image_medium_shot"][
                "attachment_url"
            ]
            img_link = "https://cms.homburger.ch/wp-content/uploads/" + img_

            en_id = english_entry["dd_person"]["ID"]
            de_id = german_entry["dd_person"]["ID"]

            en_news = await self.query_news_api(en_id, "en")
            de_news = await self.query_news_api(de_id, "de")

            en_bulletins = await self.query_bulletin_api(en_id, "en")
            de_bulletins = await self.query_bulletin_api(de_id, "de")

            en_pub = await self.query_publications_api(en_id, "en")
            de_pub = await self.query_publications_api(de_id, "de")

            attachments = {}
            pub_attachment_en = await self.get_pub_attachment(en_pub, "EN")
            attachments.update(pub_attachment_en)

            pub_attachment_de = await self.get_pub_attachment(de_pub, "DE")
            attachments.update(pub_attachment_de)

            entry = {
                "url": url,
                "EN_id": en_id,
                "DE_id": de_id,
                "person": self.person,
                "en_bulletins": en_bulletins,
                "de_bulletins": de_bulletins,
                "en_news": en_news,
                "de_news": de_news,
                "en_publications": en_pub,
                "de": de_pub,
                "EN_profile_page": english_entry,
                "DE_profile_page": german_entry,
            }

            fname, fcontent = await self.get_img(img_link, url)
            attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(url)

    def get_name(self, url):
        name = re.search(r"team\/([\w-]+)", url)
        return name.group(1)

    def get_page_title(self, tree):
        """Get actual name of the person"""
        name = tree.xpath("//title/text()")[0]
        return name.replace(" ", "-").lower()

    def has_numbers(self, input_str):
        return any(char.isdigit() for char in input_str)

    async def profile_page_api(self, lang, name, page_title):
        if lang == "de" and self.has_numbers(name):
            name = page_title
            self.person = page_title
        url = f"https://homburger.ch/_next/data/gZN3UKFUOQtdEV_C9Z7tM/{lang}/team/{name}.json?lang={lang}&path=team&path={name}"

        async with self.http_request(url) as resp:
            res = await resp.json()
            result = res["pageProps"]["page"]
            try:
                del result["dd_bulletins_list"]
                del result["dd_deals_cases_news_list"]
                del result["dd_publications_list"]
            except:
                logger.exception(url)

            return result

    async def query_news_api(self, person_id, lang):
        payload = {
            "operationName": "deals_cases_news",
            "variables": {
                "lang": lang,
                "expertise": None,
                "author": [int(person_id)],
                "search": None,
                "cursor": "0",
            },
            "query": "fragment attachment on WpAttachment {\n  ID\n  post_title\n  post_content\n  post_excerpt\n  attachment_url\n  attachment_focal_point {\n    x\n    y\n    __typename\n  }\n  attachment_metadata {\n    alt_text\n    file\n    width\n    height\n    __typename\n  }\n  __typename\n}\n\nfragment newsDealsCases on NewsDealsCases {\n  ID\n  post_date\n  slug\n  translations {\n    de\n    en\n    __typename\n  }\n  post_date\n  acf {\n    title\n    text\n    type\n    teaser\n    expertise {\n      slug\n      acf {\n        title\n        icon {\n          ...attachment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    image {\n      ...attachment\n      __typename\n    }\n    authors {\n      ... on NewsDealsCases_Acf_authors_list_group_5f1812df4b8d3_authors_extern {\n        extern {\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on NewsDealsCases_Acf_authors_list_group_5f1812df4b8d3_authors_intern {\n        intern {\n          ref {\n            slug\n            acf {\n              name\n              surname\n              image_close_up {\n                ...attachment\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery deals_cases_news($lang: String!, $expertise: [Int!], $author: [Int!], $search: String, $cursor: String) {\n  dd_deals_cases_news_list(lang: $lang, pageSize: 1000, cursor: $cursor, search: $search, filterBy: {acf__expertise: {in: $expertise}, acf__authors__ref: {in: $author}}) {\n    cursor\n    hasMore\n    result {\n      ...newsDealsCases\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        async with self.http_request(
            "https://api.homburger.ch/", json_data=payload
        ) as resp:
            result = await resp.json()
            return result["data"]["dd_deals_cases_news_list"]["result"]

    async def query_bulletin_api(self, person_id, lang):
        payload = {
            "operationName": "bulletins",
            "variables": {
                "lang": lang,
                "expertise": None,
                "author": [int(person_id)],
                "search": None,
                "cursor": "0",
            },
            "query": "fragment attachment on WpAttachment {\n  ID\n  post_title\n  post_content\n  post_excerpt\n  attachment_url\n  attachment_focal_point {\n    x\n    y\n    __typename\n  }\n  attachment_metadata {\n    alt_text\n    file\n    width\n    height\n    __typename\n  }\n  __typename\n}\n\nfragment bulletin on Bulletins {\n  ID\n  slug\n  post_date\n  acf {\n    introduction\n    title\n    is_mini_series\n    thumbnail {\n      post_title\n      attachment_metadata {\n        alt_text\n        file\n        height\n        width\n        __typename\n      }\n      __typename\n    }\n    authors {\n      ... on Bulletins_Acf_authors_list_group_5f1812df4b8d3_authors_extern {\n        extern {\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on Bulletins_Acf_authors_list_group_5f1812df4b8d3_authors_intern {\n        intern {\n          ref {\n            slug\n            acf {\n              name\n              surname\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    block_list {\n      ... on Bulletins_Acf_block_list_quote_personal {\n        quote_personal {\n          name\n          quote\n          image {\n            ...attachment\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on Bulletins_Acf_block_list_rich_text {\n        rich_text {\n          rich_text\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery bulletins($lang: String!, $expertise: [Int!], $author: [Int!], $search: String, $cursor: String) {\n  dd_bulletins_list(lang: $lang, pageSize: 1000, cursor: $cursor, search: $search, filterBy: {acf__expertise: {in: $expertise}, acf__authors__ref: {in: $author}}) {\n    cursor\n    hasMore\n    result {\n      ...bulletin\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        async with self.http_request(
            "https://api.homburger.ch/", json_data=payload
        ) as resp:
            result = await resp.json()
            return result["data"]["dd_bulletins_list"]["result"]

    async def query_publications_api(self, person_id, lang):
        payload = {
            "operationName": "publications_filter",
            "variables": {
                "lang": lang,
                "expertise": None,
                "author": [int(person_id)],
                "search": None,
                "cursor": "0",
                "pageSize": 1000,
            },
            "query": "fragment publication on Publications {\n  ID\n  lang\n  slug\n  translations {\n    de\n    en\n    __typename\n  }\n  post_date\n  acf {\n    title\n    text\n    external_link {\n      target\n      title\n      url\n      __typename\n    }\n    document {\n      ID\n      post_title\n      attachment_url\n      __typename\n    }\n    authors {\n      ... on Publications_Acf_authors_list_group_5f1812df4b8d3_authors_extern {\n        extern {\n          name\n          __typename\n        }\n        __typename\n      }\n      ... on Publications_Acf_authors_list_group_5f1812df4b8d3_authors_intern {\n        intern {\n          ref {\n            slug\n            acf {\n              name\n              surname\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery publications_filter($lang: String!, $author: [Int!], $expertise: [Int!], $search: String, $cursor: String, $pageSize: Int) {\n  dd_publications_list(lang: $lang, pageSize: $pageSize, cursor: $cursor, search: $search, filterBy: {acf__expertise: {in: $expertise}, acf__authors__ref: {in: $author}}) {\n    cursor\n    hasMore\n    result {\n      ...publication\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        async with self.http_request(
            "https://api.homburger.ch/", json_data=payload
        ) as resp:
            result = await resp.json()
            return result["data"]["dd_publications_list"]["result"]

    async def get_pub_attachment(self, publications, lang):
        publication_attachment = {}
        for publication in publications:
            title = publication["acf"]["title"]
            try:
                pdf_url = publication["acf"]["document"]["attachment_url"]
                u = pdf_url.split("/")
                true_pdf_link = urljoin(
                    "https://homburger.ch/api/ms/", f"{u[0]}/{u[1]}/_/{u[-1]}"
                )
                dl_link, fcontent = await self.get_file(true_pdf_link)
                publication_attachment[lang + " " + dl_link] = fcontent
                logger.info(f"DOWNLOADING . . . {title}")
            except:
                logger.info(f"{title} has no pdf file for publications")

        return publication_attachment

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def get_img(self, dl_link, url):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return file_url, await resp.read()


def main():
    scraper = HomburgerPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

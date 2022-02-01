from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

# german eng french italian


class Curia_Europa(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    ROOT_URL = "https://curia.europa.eu/"
    START_URL = "https://curia.europa.eu/juris/documents.jsf?redirection=doc&oqp=&for=&mat=or&lgrec=en&jge=&ordreTri=dateDesc&td=%3B%24mode%3D8D%24from%3D2022.1.19%24to%3D2022.1.26%3B%3B%3BPUB1%2CPUB3%2CPUB4%3BNPUB1%3B%3BORDALL&jur=C&page=1&dates=&pcs=Oor&lg=&pro=&nat=or&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&language=en&avg=&cid=3092823"
    DB_NAME = "curia_europa"

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 4

    async def initialize(self):
        await super().initialize()
        await self.enqueue_request(self.START_URL)

    async def handle_request(self, request):
        try:
            logger.info(f"Going Page Link: {request}")
            async with self.http_request(request) as response:
                t = html.fromstring(html=await response.text())

                next_page = t.xpath('//img[@title="Show next document"]/../@href')[0]
                # table rows
                trows = t.xpath('//tr[@class="table_document_ligne"]')

                for trow in trows[:3]:
                    case = trow.xpath("./td[1]/text()")[0]

                    document = " ".join(
                        [i.strip() for i in trow.xpath("./td[2]//text()")]
                    )
                    date = trow.xpath("./td[3]/text()")[0]
                    name_of_parties = trow.xpath("./td[4]/text()")[0]

                    subjects = trow.xpath(
                        './td[5]/div[@id="matieres"]/span[@class="tooltipLink"]//text()'
                    )

                    try:
                        en_html = await self.get_html(
                            trow.xpath('.//li/a[contains(@href,"doclang=EN")]/@href')[0]
                        )
                    except:
                        en_html = ""

                    try:
                        de_html = await self.get_html(
                            trow.xpath('.//li/a[contains(@href,"doclang=DE")]/@href')[0]
                        )
                    except:
                        de_html = ""

                    try:
                        fr_html = await self.get_html(
                            trow.xpath('.//li/a[contains(@href,"doclang=FR")]/@href')[0]
                        )
                    except:
                        fr_html = ""

                    try:
                        it_html = await self.get_html(
                            trow.xpath('.//li/a[contains(@href,"doclang=IT")]/@href')[0]
                        )
                    except:
                        it_html = ""

                    subject_matter = " ".join([i.strip() for i in subjects])
                    entry = {
                        "case": case,
                        "document": document,
                        "date": date,
                        "name_of_parties": name_of_parties,
                        "subject_matter": subject_matter,
                        "en_html": en_html,
                        "de_html": de_html,
                        "fr_html": fr_html,
                        "it_html": it_html,
                    }

                    parsed = await self.parse(entry)
                    if parsed is not None:
                        await self.enqueue_result(parsed)

                if next_page:
                    await self.enqueue_request(next_page)
        except:
            logger.exception(request)

    async def parse(self, entry):
        try:
            attachments = {}
            # fname, fcontent = await self.get_file(entry["pdf_link"])
            # attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(entry["case"])

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            url = entry["case"]
            async with self.get_doc(collection, url) as doc:
                doc.update(entry)
            for file_name, file_content in attachments.items():

                try:
                    if "getattachment" in file_name:
                        await doc.attachment(file_name).save(file_content, "image/jpeg")
                    else:
                        await doc.attachment(file_name).save(
                            file_content, "application/pdf"
                        )
                    logger.info(f"Downloading {file_name}")
                except:
                    logger.debug(f"Cannot download {file_name}")

    async def get_file(self, dl_link):
        if dl_link is not None:
            file_url = dl_link.replace("\\", "")
            async with self.http_request(file_url) as resp:
                return dl_link, await resp.read()
        else:
            return "", ""

    async def get_html(self, link):
        if link:
            logger.info(f"Downloading HTML file of {link}")
            async with self.http_request(link) as response:
                t = html.fromstring(html=await response.text())

            return t.xpath('//div[@id="document_content"]//text()')


def main():
    scraper = Curia_Europa()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

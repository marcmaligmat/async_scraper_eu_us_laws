import mimetypes

from lxml import html

import dj_scrape.core

from loguru import logger

from urllib.parse import urljoin

HEADERS = {
    "content-type": "text/html",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
}


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

        async with self.http_request(
            start_url,
            headers=HEADERS,
        ) as response:
            tree = html.fromstring(html=await response.text())

        links = tree.xpath(
            '//section[@class="people overview"]//span[@class="highlight-mark"]//a[contains(@href,"people")]/@href'
        )
        if not links:
            logger.warning("No initial links found, please check xpath expression")

        for link in links:
            logger.info(f"Initializing {link=}")
            await self.enqueue_request(link)

    async def handle_request(self, request):
        parsed = await self.parse(request)
        if parsed is not None:
            await self.enqueue_result(parsed)

    async def handle_results(self, results):
        collection = await self.get_db(self.DB_NAME)
        for entry, attachments in results:
            # print(entry)
            url = entry["EN"]["url"]

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

    async def parse(self, url):
        person_url = url.split("/")[-1]
        languages = {
            "EN": {
                "link": "/en/people/",
                "practice_area": "tigkeitsgebiete",
                "education": "Education",
                "experience": "Experience / Career",
                "activities": "Further activities",
                "publications": "Publications / Presentations",
            },
            "DE": {
                "link": "/de/personen/",
                "practice_area": "Practice areas",
                "education": "Ausbildung",
                "experience": "Werdegang / Karriere",
                "activities": "tigkeiten",
                "publications": "Publikationen",
            },
            "FR": {
                "link": "/fr/personnes/",
                "practice_area": "Domaines d'activités",
                "education": "Formation",
                "experience": "Affiliations",
                "activities": "Autres activités",
                "publications": "Publications / exposés",
            },
            "IT": {
                "link": "/it/persone/",
                "practice_area": "Aree di attività",
                "education": "Formazione",
                "experience": "Esperienze professionali",
                "activities": "Altre attività",
                "publications": "Pubblicazioni / Presentazioni",
            },
        }
        attachments = {}
        entry = {}
        for lang, val in languages.items():

            url = urljoin(self.ROOT_URL, val["link"] + person_url)
            async with self.http_request(url, headers=HEADERS) as response:
                response_text = await response.text()
            try:
                tree = html.fromstring(html=response_text)

                person = tree.xpath('(//span[@class="highlight-mark"])[1]/text()')[0]

                about = tree.xpath('(//span[@class="highlight-mark"])[2]/text()')[0]

                practice_areas = self.remove_empty(
                    tree.xpath(
                        '//a[contains(text(),"%s")]/../../div//li//text()'
                        % val["practice_area"]
                    )
                )

                education = tree.xpath(
                    '//a[contains(text(),"%s")]/../../div//li//text()'
                    % val["education"]
                )

                experience = tree.xpath(
                    '//a[contains(text(),"%s")]/../../div//li//text()'
                    % val["experience"]
                )
                further_activities = tree.xpath(
                    '//a[contains(text(),"%s")]/../../div//li//text()'
                    % val["activities"]
                )
                publications = tree.xpath(
                    '//a[contains(text(),"%s")]/../../div//li//text()'
                    % val["publications"]
                )

                # entries
                entry.update(
                    {
                        lang: {
                            "url": url,
                            "person": person,
                            "about": about,
                            "practice_areas": practice_areas,
                            "education": education,
                            "experience": experience,
                            "further_activities": further_activities,
                            "publications": publications,
                            # has downloadble file in publications
                            # https://www.kellerhals-carrard.ch/en/people/thomas-baehler.php
                        }
                    }
                )

                cv_link = tree.xpath('//li/a[contains(text(),"CV")]/@href')[0]
                fname, fcontent = await self.get_fcontent(cv_link, url)
                attachments[lang + " " + fname] = fcontent

                img_link = tree.xpath(
                    '//div[@class="people-image-container"]/img/@src'
                )[0]
                fname, fcontent = await self.get_fcontent(img_link, url)
                attachments[lang + " " + fname] = fcontent

            except:
                logger.exception(url)

        return entry, attachments

    async def get_fcontent(self, dl_link, url):
        dl_link = urljoin(self.ROOT_URL, dl_link)
        file_url = dl_link.replace("\\", "")
        async with self.http_request(file_url) as resp:
            return file_url, await resp.read()

    def remove_empty(self, lines):
        new_lines = []
        for l in lines:
            if "\t" in l or "\n" in l:
                continue
            new_lines.append(l)
        return new_lines


def main():
    scraper = KellerhalsCarrardPeople()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    main()

import mimetypes
import re
from urllib.parse import urljoin

from loguru import logger

import dj_scrape.core

from lxml import html
from absl import app, flags
import json


class SwissLaw(dj_scrape.core.CouchDBMixin, dj_scrape.core.Scraper):
    # https://www.fedlex.admin.ch/en/search?collection=federal_sheet&itemsPerPage=10&currentPage=1&
    ROOT_URL = "https://www.fedlex.admin.ch/"
    ENDPOINT = "https://www.fedlex.admin.ch/elasticsearch/proxy/_search?index=data"
    DB_NAME = "swisslaw"
    SIZE = 10
    OFFSET = 0

    class ScraperSettings(dj_scrape.core.Scraper.ScraperSettings):
        num_request_workers = 1
        num_results_workers = 1
        http_pause_seconds = 0.5
        max_results_batch_size = 1

    async def initialize(self):
        await super().initialize()
        await self.enqueue_request(self.ENDPOINT)

    async def handle_request(self, link):
        logger.info(f"initializing {link=}")

        while True:
            async with self.http_request(
                link, json_data=self._payload(self.SIZE, self.OFFSET)
            ) as resp:
                response = await resp.json()

            if response["timed_out"] is False:
                for hit in response["hits"]["hits"]:
                    parsed = await self.parse(hit)
                    if parsed is not None:
                        await self.enqueue_result(parsed)

            else:
                logger.info(f"Timed out! size = {self.SIZE} offset = ")
            self.OFFSET += self.SIZE

    async def parse(self, hit):
        uri = hit["_source"]["data"]["uri"]
        files = hit["_source"]["included"]
        logger.info(f"Parsing {uri=}")
        try:
            entry = {
                "url": uri,
                "parse_size": self.SIZE,
                "parse_offset": self.OFFSET,
                "result": hit,
            }
            attachments = {}

            for f in files:
                if f["type"] == "Manifestation":
                    if "isExemplifiedBy" in f["attributes"].keys():
                        file_link = f["attributes"]["isExemplifiedBy"]["rdfs:Resource"]
                        fname, fcontent = await self.get_file(file_link)
                        attachments[fname] = fcontent

            return entry, attachments
        except:
            logger.exception(uri)

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

    def _payload(self, size, offset):
        return {
            "size": size,
            "from": offset,
            "aggs": {
                "results_language_ff": {
                    "filter": {"match_all": {}},
                    "aggs": {
                        "http://publications.europa.eu/resource/authority/language/DEU": {
                            "filter": {
                                "term": {
                                    "included.references.language.keyword": "http://publications.europa.eu/resource/authority/language/DEU"
                                }
                            }
                        },
                        "http://publications.europa.eu/resource/authority/language/FRA": {
                            "filter": {
                                "term": {
                                    "included.references.language.keyword": "http://publications.europa.eu/resource/authority/language/FRA"
                                }
                            }
                        },
                        "http://publications.europa.eu/resource/authority/language/ITA": {
                            "filter": {
                                "term": {
                                    "included.references.language.keyword": "http://publications.europa.eu/resource/authority/language/ITA"
                                }
                            }
                        },
                        "http://publications.europa.eu/resource/authority/language/ROH": {
                            "filter": {
                                "term": {
                                    "included.references.language.keyword": "http://publications.europa.eu/resource/authority/language/ROH"
                                }
                            }
                        },
                        "http://publications.europa.eu/resource/authority/language/ENG": {
                            "filter": {
                                "term": {
                                    "included.references.language.keyword": "http://publications.europa.eu/resource/authority/language/ENG"
                                }
                            }
                        },
                    },
                },
                "facets.typeDocumentBroader.keyword": {
                    "terms": {
                        "field": "facets.typeDocumentBroader.keyword",
                        "size": 500,
                    }
                },
                "data.attributes.typeDocument.rdfs:Resource.keyword": {
                    "terms": {
                        "field": "data.attributes.typeDocument.rdfs:Resource.keyword",
                        "size": 500,
                    }
                },
                "data.attributes.legalResourceGenre.rdfs:Resource.keyword": {
                    "terms": {
                        "field": "data.attributes.legalResourceGenre.rdfs:Resource.keyword",
                        "size": 500,
                    }
                },
                "data.references.legalResourcePublicationCompleteness.keyword": {
                    "terms": {
                        "field": "data.references.legalResourcePublicationCompleteness.keyword",
                        "size": 500,
                    }
                },
                "data.references.responsibilityOf.keyword": {
                    "terms": {
                        "field": "data.references.responsibilityOf.keyword",
                        "size": 500,
                    }
                },
                "facets.basicAct.responsibilityOf.keyword": {
                    "terms": {
                        "field": "facets.basicAct.responsibilityOf.keyword",
                        "size": 500,
                    }
                },
                "result_count": {"value_count": {"field": "data.uri.keyword"}},
            },
            "query": {
                "bool": {
                    "filter": [{"terms": {"data.type.keyword": ["Act"]}}],
                    "must": [
                        {"match_all": {}},
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match": {
                                            "included.attributes.memorialName.xsd:string.keyword": "FF"
                                        }
                                    },
                                    {
                                        "match": {
                                            "included.attributes.memorialName.xsd:string.keyword": "BBl"
                                        }
                                    },
                                    {
                                        "match": {
                                            "included.attributes.memorialName.xsd:string.keyword": "FF"
                                        }
                                    },
                                    {
                                        "match": {
                                            "included.attributes.memorialName.xsd:string.keyword": "FGA"
                                        }
                                    },
                                    {
                                        "match": {
                                            "included.attributes.memorialName.xsd:string.keyword": "FUF"
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        },
                    ],
                    "should": [],
                }
            },
        }


def main(_):
    scraper = SwissLaw()
    dj_scrape.core.run_scraper(scraper)


if __name__ == "__main__":
    app.run(main)

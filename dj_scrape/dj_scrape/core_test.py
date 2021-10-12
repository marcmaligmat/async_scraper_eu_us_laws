#!/usr/bin/env python3

from absl.testing import absltest

from contextlib import asynccontextmanager
from unittest.mock import patch, MagicMock

from dj_scrape.core import Scraper, run_scraper, CouchDBMixin

import pydantic
from aiocouch.document import Document

def mock_aio(text_response):
    async def _f(*args, **kwargs):
        mock = MagicMock()
        async def _text():
            return text_response
        mock.text = _text
        return mock
    return _f

class SimpleScraper(Scraper):
    class SimpleSettings(pydantic.BaseSettings):
        additional_setting = 'bla'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simple_settings = self.SimpleSettings()
        self.results = []
    async def initialize(self):
        await self.enqueue_request(dict(url='https://deepjudge.ai'))
        await super().initialize()
    async def handle_request(self, request):
        async with self.http_request(request['url']) as resp:
            await self.enqueue_result(await resp.text())
    async def handle_results(self, results):
        self.results.extend(results)


class CouchDBScraper(CouchDBMixin, SimpleScraper):
    class CouchDBSettings(CouchDBMixin.CouchDBSettings):
        couchdb_url: str = 'http://localhost:5984'
        couchdb_user: str = 'admin'
        couchdb_password: str = 'MDJhNjJmNTc1N2EyZDY4NDg2YTQ1YjY2OWVlMGE4NGY'
    async def handle_results(self, results):
        collection = await self.get_db('test_collection')
        for idx, r in enumerate(results):
            async with Document(collection, str(idx)) as doc:
                doc['greeting'] = r
    

class UnitTest(absltest.TestCase):

    def test_echo(self):
        pass
    
    def test_simple_scraper(self):
        scraper = SimpleScraper()
        self.assertEqual(scraper.simple_settings.additional_setting, 'bla')
        with patch('aiohttp.ClientSession.request', mock_aio('hello')):
            run_scraper(scraper)
        self.assertEqual(scraper.results[0], 'hello')

    def test_couchdb_scraper(self):
        # Note: ./run_couchdb.sh in scrapers/test_utils/couch_db needs to be running
        scraper = CouchDBScraper()
        run_scraper(scraper)

if __name__ == '__main__':
    absltest.main()

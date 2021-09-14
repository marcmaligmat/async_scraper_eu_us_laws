#!/usr/bin/env python3

from absl.testing import absltest

from contextlib import asynccontextmanager
from unittest.mock import patch, MagicMock

from dj_scrape.core import Scraper, run_scraper, MongoMixin

import mongomock

def mock_aio(text_response):
    @asynccontextmanager
    async def _f(*args, **kwargs):
        mock = MagicMock()
        async def _text():
            return text_response
        mock.text = _text
        yield mock
    return _f

class SimpleScraper(Scraper):
    class Settings(Scraper.Settings):
        additional_setting = 'bla'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = []
    async def initialize(self, context):
        await context.enqueue_request(dict(url='https://deepjudge.ai'))
    async def handle_request(self, request, context):
        async with await context.http_request(request['url']) as resp:
            await context.enqueue_result(await resp.text())
    async def handle_results(self, results, context):
        self.results.extend(results)


class MongoScraper(MongoMixin, SimpleScraper):
    class MongoSettings(MongoMixin.MongoSettings):
        mongodb_connection_string = 'mongodb://localhost:27017'
        mongodb_database_name = 'scrape'
    async def handle_results(self, results, context):
        await self.get_db().test_collection.insert_many({'greeting': r} for r in results)
    

class UnitTest(absltest.TestCase):

    def test_echo(self):
        pass
    
    def test_simple_scraper(self):
        scraper = SimpleScraper()
        self.assertEqual(scraper.settings.additional_setting, 'bla')
        with patch('aiohttp.ClientSession.get', mock_aio('hello')):
            run_scraper(scraper)
        self.assertEqual(scraper.results[0], 'hello')

    def test_mongo_scraper(self):
        scraper = MongoScraper()
        with patch('aiohttp.ClientSession.get', mock_aio('hello')):
            run_scraper(scraper)

if __name__ == '__main__':
    absltest.main()

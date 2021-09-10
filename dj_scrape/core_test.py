#!/usr/bin/env python3

from absl.testing import absltest

from core import Scraper, ScrapeRequest, run_scraper

class UnitTest(absltest.TestCase):

    def test_echo(self):
        pass
    
    def test_simple_scraper(self):
        class SimpleScraper(Scraper):
            async def initialize(self, context):
                await context.enqueue_request(ScrapeRequest(url='https://deepjudge.ai'))
            async def handle_request(self, request, context):
                async with context.web_session.get(request.url) as resp:
                    await context.enqueue_result(await resp.text())
            async def handle_results(self, results, context):
                print(results)


        run_scraper(SimpleScraper())

absltest.main()

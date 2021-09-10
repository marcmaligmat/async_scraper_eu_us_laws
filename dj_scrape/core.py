#!/usr/bin/env python3

from typing import Optional, Any

from absl import logging

import asyncio
import aiohttp
import pydantic

class ScrapeRequest(pydantic.BaseModel):
    url: str
    context: Optional[Any]

class ScrapeSettings(pydantic.BaseSettings):
    num_workers : int = 1
    requests_queue_type : str = 'fifo'
    max_results_batch_size : int = 64

class ScrapeContext:
    def __init__(self, settings: ScrapeSettings):
        self.settings = settings

    async def __aenter__(self):
        self.requests_queue = {
                'fifo': asyncio.Queue,
                'lifo': asyncio.LifoQueue,
                }[self.settings.requests_queue_type]()
        self.results_queue = asyncio.Queue()
        self.web_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_, tb):
        await self.web_session.close()

    async def enqueue_request(self, request: ScrapeRequest):
        return await self.requests_queue.put(request)

    async def enqueue_result(self, result: Any):
        return await self.results_queue.put(result)

    async def http_request(self, url: str, post_data: dict = None):
        if post_data is None:
            return await self.web_session.get(url=url)
        else:
            return await self.web_session.post(url=url, data=post_data)


class Scraper:
    def __init__(self, settings: ScrapeSettings = None):
        self.started = False
        self.settings = settings or ScrapeSettings()

    async def initialize(self, context: ScrapeContext):
        raise NotImplementedError()

    async def finalize(self, context: ScrapeContext):
        pass

    async def handle_request(self, request: ScrapeRequest, context: ScrapeContext):
        raise NotImplementedError()

    async def handle_results(self, results: list, context: ScrapeContext):
        raise NotImplementedError()


async def _requests_worker(scraper: Scraper, worker_id: int, context: ScrapeContext):
    logging.info(f'Starting worker {worker_id}')
    while True:
        request = await context.requests_queue.get()
        try:
            await scraper.handle_request(request, context)
        except:
            logging.exception(f'Failed to handle request: {request}')
        context.requests_queue.task_done()


async def _results_worker(scraper: Scraper, context: ScrapeContext):

    async def _handle_batch(results_batch):
        try:
            await scraper.handle_results(results_batch, context)
        except asyncio.CancelledError:
            logging.warning(f'Cancelled -- This should not happen')
            raise
        except:
            logging.exception(f'Failed to handle results')

    results_batch = []
    try:
        while True:
            result = await context.results_queue.get()
            results_batch.append(result)
            if len(results_batch) >= context.settings.max_results_batch_size:
                results = results_batch[:]
                results_batch = []
                await _handle_batch(results)
            context.results_queue.task_done()
    except asyncio.CancelledError:
        if len(results_batch) > 0:
            await _handle_batch(results_batch)
        raise


async def _run_scraper(scraper):
    async with ScrapeContext(scraper.settings) as context:
        await scraper.initialize(context)
        workers = [asyncio.create_task(_requests_worker(scraper, worker_id=i, context=context), name=f'worker_{i}') for i in range(context.settings.num_workers)]
        workers.append(asyncio.create_task(_results_worker(scraper, context=context), name='results_worker'))
        await context.requests_queue.join()
        await context.results_queue.join()
        await scraper.finalize(context)
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


def run_scraper(scraper: Scraper):
    if scraper.started:
        raise ValueError("Already started")
    scraper.started = True
    asyncio.run(_run_scraper(scraper))


#!/usr/bin/env python3

from typing import Optional, Any, Union

from loguru import logger

import asyncio
import aiohttp
import pydantic
import tempfile
from pathlib import Path
import shutil
import time

import motor.motor_asyncio

class ScrapeContext:
    def __init__(self, settings: 'Scraper.Settings'):
        self.settings = settings
        self._http_lock = asyncio.Lock()
        self._last_http_request = 0.

    async def __aenter__(self):
        self.requests_queue = {
                'fifo': asyncio.Queue,
                'lifo': asyncio.LifoQueue,
                }[self.settings.requests_queue_type]()
        self.results_queue = asyncio.Queue()
        self._web_session = aiohttp.ClientSession()
        self.tmp_dir = Path(tempfile.mkdtemp(prefix='scrape-'))
        return self

    async def __aexit__(self, exc_type, exc_, tb):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        await self._web_session.close()

    async def enqueue_request(self, request: Any):
        return await self.requests_queue.put(request)

    async def enqueue_result(self, result: Any):
        return await self.results_queue.put(result)

    async def http_request(self, url: str, query_params: Union[dict, str] = None, json_data: dict = None, post_data: Union[dict, str, bytes, aiohttp.FormData] = None, files: dict = None):
        async with self._http_lock:
            current_time = time.time()
            time_since_last_request = current_time - self._last_http_request
            time_to_pause = self.settings.http_pause_seconds - time_since_last_request
            if time_to_pause > 0:
                await asyncio.sleep(time_to_pause)
            self._last_http_request = time.time()
        if not any(d is not None for d in (json_data, post_data, files)):
            return self._web_session.get(url=url, params=query_params)
        else:
            return self._web_session.post(url=url, json=json_data, data=post_data, files=files, params=query_params)


class Scraper:
    class Settings(pydantic.BaseSettings):
        debug: bool = False
        num_workers : int = 1
        requests_queue_type : str = 'fifo'
        max_results_batch_size : int = 64
        http_pause_seconds: float = 0.

    def __init__(self, settings: Settings = None):
        self.started = False
        self.settings = settings or self.Settings()

    async def initialize(self, context: ScrapeContext):
        raise NotImplementedError()

    async def finalize(self, context: ScrapeContext):
        pass

    async def handle_request(self, request: Any, context: ScrapeContext):
        raise NotImplementedError()

    async def handle_results(self, results: list, context: ScrapeContext):
        raise NotImplementedError()

    def __repr__(self):
        return f'Scraper[{self.settings}]'


class MongoMixin(Scraper):
    class MongoSettings(pydantic.BaseSettings):
        mongodb_connection_string: str = 'mongodb://localhost:27017'
        mongodb_database_name: str = 'scrape'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_settings = self.MongoSettings()

    async def initialize(self, context):
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_settings.mongodb_connection_string)

    def get_db(self):
        return self.mongo_client[self.mongo_settings.mongodb_database_name]


async def _requests_worker(scraper: Scraper, worker_id: int, context: ScrapeContext):
    logger.info(f'Starting worker {worker_id}')
    while True:
        request = await context.requests_queue.get()
        try:
            await scraper.handle_request(request, context)
        except:
            logger.exception(f'Failed to handle request: {request}')
            if context.settings.debug:
                raise SystemExit(1)
        context.requests_queue.task_done()


async def _results_worker(scraper: Scraper, context: ScrapeContext):

    async def _handle_batch(results_batch):
        try:
            await scraper.handle_results(results_batch, context)
        except asyncio.CancelledError:
            logger.warning(f'Cancelled -- This should not happen')
            raise
        except:
            logger.exception(f'Failed to handle results')
            if context.settings.debug:
                raise SystemExit(1)

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
    logger.info(f'Running scraper: {scraper}')
    asyncio.run(_run_scraper(scraper), debug=scraper.settings.debug)


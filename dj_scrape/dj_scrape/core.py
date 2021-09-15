#!/usr/bin/env python3

from typing import Any, Union

from loguru import logger

import asyncio
import tempfile
from pathlib import Path
import shutil
import time
import contextlib

import aiohttp
import pydantic
import motor.motor_asyncio
import aiocouch


class Scraper:
    class ScraperSettings(pydantic.BaseSettings):
        debug: bool = False
        log_interval: int = 3
        num_request_workers: int = 1
        num_results_workers: int = 1
        request_queue_type: str = "fifo"
        max_results_batch_size: int = 64
        http_pause_seconds: float = 0.0

    def __init__(self, scraper_settings: ScraperSettings = None):
        self.started = False
        self.scraper_settings = scraper_settings or self.ScraperSettings()
        self._last_http_request = 0.0

    async def initialize(self):
        pass

    async def finalize(self):
        pass

    async def handle_request(self, request: Any):
        pass

    async def handle_results(self, results: list):
        pass

    def __repr__(self):
        return f"Scraper[{self.scraper_settings}]"

    async def __aenter__(self):
        self._request_queue = {
            "fifo": asyncio.Queue,
            "lifo": asyncio.LifoQueue,
        }[self.scraper_settings.request_queue_type]()
        self._results_queue = asyncio.Queue()
        self._web_session = aiohttp.ClientSession()
        self._http_lock = asyncio.Lock()
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="scrape-"))
        return self

    async def __aexit__(self, exc_type, exc_, tb):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)
        await self._web_session.close()

    async def enqueue_request(self, request: Any):
        return await self._request_queue.put(request)

    async def enqueue_result(self, result: Any):
        return await self._results_queue.put(result)

    async def http_request(
        self,
        url: str,
        query_params: Union[dict, str] = None,
        json_data: dict = None,
        post_data: Union[dict, str, bytes, aiohttp.FormData] = None,
        files: dict = None,
    ):
        async with self._http_lock:
            current_time = time.time()
            time_since_last_request = current_time - self._last_http_request
            time_to_pause = self.scraper_settings.http_pause_seconds - time_since_last_request
            if time_to_pause > 0:
                await asyncio.sleep(time_to_pause)
            self._last_http_request = time.time()
        if not any(d is not None for d in (json_data, post_data, files)):
            return self._web_session.get(url=url, params=query_params)
        else:
            return self._web_session.post(
                url=url,
                json=json_data,
                data=post_data,
                files=files,
                params=query_params,
            )



class MongoMixin(Scraper):
    class MongoSettings(pydantic.BaseSettings):
        mongodb_connection_string: str = "mongodb://localhost:27017"
        mongodb_database_name: str = "scrape"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_settings = self.MongoSettings()

    async def initialize(self):
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
            self.mongo_settings.mongodb_connection_string
        )

    def get_db(self):
        return self.mongo_client[self.mongo_settings.mongodb_database_name]


class CouchDBMixin(Scraper):
    class CouchDBSettings(pydantic.BaseSettings):
        couchdb_url: str = "http://localhost:5984"
        couchdb_user: str = "admin"
        couchdb_password: str = "MDJhNjJmNTc1N2EyZDY4NDg2YTQ1YjY2OWVlMGE4NGY"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.couchdb_settings = self.CouchDBSettings()

    async def initialize(self):
        self.couchdb_client = aiocouch.CouchDB(
            self.couchdb_settings.couchdb_url,
            self.couchdb_settings.couchdb_user,
            self.couchdb_settings.couchdb_password,
        )
        await self.couchdb_client.check_credentials()
        await super().initialize()

    async def finalize(self):
        await super().finalize()
        await self.couchdb_client.close()

    async def get_db(self, name):
        return await self.couchdb_client.create(name, exists_ok=True)

    @contextlib.asynccontextmanager
    async def get_doc(self, db, doc_id):
        async with aiocouch.document.Document(db, doc_id) as doc:
            yield doc



async def _request_worker(scraper: Scraper, worker_id: int):
    logger.info(f"Starting request worker {worker_id}")
    while True:
        request = await scraper._request_queue.get()
        try:
            await scraper.handle_request(request)
        except:
            logger.exception(f"Failed to handle request: {request}")
            if scraper.scraper_settings.debug:
                raise SystemExit(1)
        scraper._request_queue.task_done()


async def _results_worker(scraper: Scraper, worker_id: int):
    logger.info(f"Starting results worker {worker_id}")

    async def _handle_batch(results_batch):
        try:
            await scraper.handle_results(results_batch)
        except asyncio.CancelledError:
            logger.warning(f"Cancelled -- This should not happen")
            raise
        except:
            logger.exception(f"Failed to handle results")
            if scraper.scraper_settings.debug:
                raise SystemExit(1)

    results_batch = []
    try:
        while True:
            result = await scraper._results_queue.get()
            try:
                results_batch.append(result)
                if len(results_batch) >= scraper.scraper_settings.max_results_batch_size:
                    results = results_batch[:]
                    results_batch = []
                    await _handle_batch(results)
            finally:
                scraper._results_queue.task_done()
    except asyncio.CancelledError:
        logger.info(f"Handling last batch (size: {len(results_batch)})")
        if len(results_batch) > 0:
            await _handle_batch(results_batch)
        raise


async def _logging_worker(scraper: Scraper):
    while True:
        await asyncio.sleep(scraper.scraper_settings.log_interval)
        logger.info(
            f"Queue sizes:\nRequests: {scraper._request_queue.qsize()}\nResults: {scraper._results_queue.qsize()}"
        )


async def _run_scraper(scraper):
    async with scraper:
        await scraper.initialize()
        workers = []
        workers.append(
            asyncio.create_task(
                _logging_worker(scraper), name="logging_worker"
            )
        )
        workers.extend(
            [
                asyncio.create_task(
                    _request_worker(scraper, worker_id=i),
                    name=f"request_worker_{i}",
                )
                for i in range(scraper.scraper_settings.num_request_workers)
            ]
        )
        workers.extend(
            [
                asyncio.create_task(
                    _results_worker(scraper, worker_id=i),
                    name=f"results_worker_{i}",
                )
                for i in range(scraper.scraper_settings.num_results_workers)
            ]
        )
        logger.info("All workers running")
        await scraper._request_queue.join()
        logger.info("Request queue empty")
        await scraper._results_queue.join()
        logger.info("Results queue empty, cancelling workers...")
        for worker in workers:
            worker.cancel()
        try:
            logger.info("Workers instructed to cancel, gathering all workers...")
            await asyncio.gather(*workers, return_exceptions=True)
        except asyncio.CancelledError:
            logger.info("All workers done")
        logger.info("Finalizing scraper")
        await scraper.finalize()
        logger.info("Finalization complete.")


def run_scraper(scraper: Scraper):
    if scraper.started:
        raise ValueError("Already started")
    scraper.started = True
    logger.info(f"Running scraper: {scraper}")
    asyncio.run(_run_scraper(scraper), debug=scraper.scraper_settings.debug)

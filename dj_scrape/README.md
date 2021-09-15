# Core Scraping Library

Core DJ scraping library. This is going to be extended in the future.

## Installation
Install from this directory using
```bash
pip3 install -e .
```

## Developing
We are using [CouchDB](https://couchdb.apache.org/) to store documents.
To develop against a local couchdb instance, see `test_utils/couchdb` to spin up a local instance in a container.

## Usage
See `takeover_ch/main.py` for an example implementation.

Scrapers subclass from `dj_scrape.core.Scraper` as well as mixins (e.g. `dj_scrape.core.CouchDBMixin`).
Every scraper is required to implement `initialize`, where initial requests are created and enqueued, `handle_request` where an enqueued request is being performed (typically using a web request), and `handle_results` where you get a *entire batch* of results. There we typically save the results to couchdb.

The scraper object has methods to enqueue new requests, or enqueue results, and also to do web request. Do not use the `_web_session` directly.


## Web requests
Are built upon `aiohttp` which is very similar to `requests`, just async.


## Database
Is build upon `aiocouch`, an async library to interface with couchdb.


## Settings
Are done using pydantic BaseSettings, which means that we can provide all values from the command line. Scrapers can also optionally add more settings classes or override settings from the parents.


## TODO
- All requests use the same session, we might want to provide some options around that
- Re-trying web requests with backoff
- Rotating proxies
- more?

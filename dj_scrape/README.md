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

Here is the core workflow:
- in `initialize`, enqueue the initial requests. Requests in the queue (and results in the results queue) can be any object type, for example strings, or dicts, or complex objects.
- in `handle_request`, you get one request (whatever you put into the queue). The goal here is to make web requests to get all data necessary. Multiple web requests can be made here. Also, further requests can be enqueued. For example, if the request just points to a page that lists documents, then in this function, we would make a web request to get the page, then parse it, then put each of the links to the documents back into the requests queue. However, if the request points to some piece of data we want to save, then we make web requests to get that data (maybe multiple), and then put the result into the results queue.
- in `handle_results`, you get a list of results (the framework automatically makes batches, but not guaranteed to be of the same size always) and the idea here is that we store them into the database.
- at any point, it's completely ok to make database calls to check, for example, if the document already exists, but it's not necessary.


## Web requests
Are built upon `aiohttp` which is very similar to `requests`, just async.
[aiohttp docs](https://docs.aiohttp.org/en/stable/)


## Database
Is build upon `aiocouch`, an async library to interface with couchdb.
[aiocouch docs](https://aiocouch.readthedocs.io/en/stable/index.html)


## Settings
Are done using pydantic BaseSettings, which means that we can provide all values from the command line. Scrapers can also optionally add more settings classes or override settings from the parents.


## TODO
- All requests use the same session, we might want to provide some options around that
- Re-trying web requests with backoff
- Rotating proxies
- more?

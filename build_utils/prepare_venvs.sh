#!/bin/bash

set -e
set -x

for scraper in `ls scrapers`
do 
    cd scrapers/$scraper
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -e ../../dj_scrape
    pip3 install -r requirements.txt
    deactivate
    cd ../..
done

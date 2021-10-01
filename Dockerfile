FROM python:3.8

COPY build_utils /src/
COPY dj_scrape /src/dj_scrape
COPY scrapers /src/scrapers
WORKDIR /src
RUN /bin/bash ./prepare_venvs.sh

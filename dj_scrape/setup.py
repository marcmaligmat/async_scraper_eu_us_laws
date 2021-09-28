#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='dj_scrape',
    version='0.0.1',
    packages=[
        'dj_scrape',
    ],
    options={'build': {
        'build_lib': 'tmp',
        'build_base': 'tmp',
    }},
    url='https://github.com/deepjudge-ai/scrapers',
    license='Proprietary',
    author='yk',
    author_email='',
    description='',
    install_requires=[
        'aiohttp',
        'motor',
        'aiocouch',
        'pydantic',
        'loguru',
        ],
)

from setuptools import setup, find_packages

setup(
    name="scrapers_shared",
    version="1.0.0",
    url="https://github.com/deepjudge-ai/scrapers.git",
    author="DJ",
    author_email="info@deepjudge.ai",
    description="Shared code for DJ scrapers",
    packages=find_packages(),
    install_requires=[
        "pydantic >= 1.8.2",
    ],
)

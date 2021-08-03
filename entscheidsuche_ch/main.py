from absl import app, flags
from lxml import html

from Logger import _logger
from time import sleep
from rich.live import Live
from rich.console import Console

from urllib.parse import urljoin

import os

from os import path

import requests
import re

console = Console()


FLAGS = flags.FLAGS
flags.DEFINE_boolean("debug", False, "Produces debugging output.")
flags.DEFINE_string("files_folder", "output", "Files Folder.")
flags.DEFINE_string("output_file", "./output.jsonl", "Name of the output file.")
flags.DEFINE_string("errorlog_file", "./error.log", "Name of the file.")
flags.DEFINE_integer("loop_timeout", 1, "Loop pause in seconds")


class Entscheidsuche_ch:
    def __init__(self):
        self.root_url = "https://entscheidsuche.ch"
        self.starting_url = "https://entscheidsuche.ch/docs/"
        self.files_folder = FLAGS.files_folder
        self.output_file = FLAGS.output_file
        self.logger = _logger(FLAGS.errorlog_file)
        self.loop_timeout = FLAGS.loop_timeout

    def scrape(self):
        response = requests.get(self.starting_url)
        tree = html.fromstring(html=response.text)
        self.links = tree.xpath('//a[contains(@href,"/docs")]/@href')
        self.parse_links()

    def parse_links(self):
        for link in self.links:
            print(link)
            self.folder_name = re.search(r"docs\/([^\/]+)", link)[1]
            self.check_downloaded_files()

            url = urljoin(self.root_url, link)
            response = requests.get(url)
            tree = html.fromstring(html=response.text)
            self.file_links = tree.xpath(
                '//a[contains(@href,"/docs") and text() != "Parent Directory"]/@href'
            )
            self.parse()
            sleep(self.loop_timeout)

    def parse(self):
        for file_link in self.file_links:
            try:
                url = urljoin(self.root_url, file_link)
                self.filename = re.search(r"[^\/]+$", url)[0]
                print(self.filename)

                if self.filename not in self.downloaded_files:
                    self.save_file(url)
                else:
                    self.logger.debug(
                        f"File: {self.filename} already exists, skipping."
                    )
            except:
                self.logger.exception(file_link)

    def save_file(self, url):
        r = requests.get(url, allow_redirects=True)
        filepath = f"{self.files_folder}/{self.folder_name}/{self.filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        open(filepath, "wb").write(r.content)

    def check_downloaded_files(self):
        _folder = f"{self.files_folder}/{self.folder_name}"
        self.downloaded_files = []
        if path.exists(_folder):
            self.downloaded_files = os.listdir(_folder)


def main(_):
    console.print("Initializing!", style="green on black")
    Entscheidsuche_ch().scrape()


if __name__ == "__main__":
    app.run(main)

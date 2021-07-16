from absl import app, flags
from lxml import html
from time import sleep

import requests

from rich.live import Live
from rich.console import Console
from urllib.parse import urljoin

from Logger import _logger
import json
import os
import re


console = Console()

FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_string('files_folder', 'output', 'Files Folder.')
flags.DEFINE_string('output_file', './output.jsonl', 'Name of the output file.')
flags.DEFINE_string('errorlog_file', './error.log', 'Name of the file.')


class Takeover_ch():
    def __init__(self):
        self.root_url = 'https://www.takeover.ch'
        self.files_folder = FLAGS.files_folder
        self.output_file = FLAGS.output_file
        self.logger = _logger(FLAGS.errorlog_file)

    def scrape(self):
        for links in list(self.get_links()[::-1]):
            url = urljoin(self.root_url,links)
            print(f"Scraping {url}")
            self.parse(url)
            sleep(1)
        
    def parse(self,url):
        try:
            response = requests.get(url)
            tree = html.fromstring(html=response.text)
            transaction = tree.xpath('//h2/text()')[0]
            descriptions = tree.xpath('//div[@class="lead"]/p/text()')
            trx_properties = tree.xpath('//aside[@class="descriptors"]/text()')
            links = tree.xpath('//article[contains(@class,"list-item")]//a/@href')
            decisions_date = tree.xpath('//article[contains(@class,"list-item")]/div[@class="inner"]/span[1]/text()')

            with open(self.output_file, 'a+') as f:
                results = {
                    'url': url,
                    'transaction':transaction,
                    'descriptions':descriptions,
                    'transaction_properties':trx_properties
                }
                #remove indent=4 when production
                f.write(json.dumps(results, indent=4, ensure_ascii=False) + '\n')
            
            n = 0
            for dl_link in links:
                if 'contentelements' in dl_link:
                    self.save_pdf(dl_link,url,decisions_date[n])
                    n+=1
        except:
            self.logger.exception(url)


    def save_pdf(self,dl_link,url,date):
        dl_link = urljoin(self.root_url,dl_link)
        trx_number = self.get_trx_number(url)
        file_lang = self.get_file_lang(dl_link)
        response = requests.get(dl_link.replace('\\',''))
        filepath = f"{self.files_folder}/nr{trx_number}/{date}-{file_lang}.pdf"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'wb') as f:
            f.write(response.content)
            f.close()

    def get_trx_number(self,url):
        number = re.search(r'\/nr\/(\d+)',url)
        return number[1]

    def get_file_lang(self,dl_link):
        language = re.search(r'\/lang\/([a-zA-Z]+)',dl_link)
        return language[1]

    def get_links(self):
        start_url = 'https://www.takeover.ch/transactions/all'
        response = requests.get(start_url)
        tree = html.fromstring(html=response.text)
        return tree.xpath('//article[@class="transaction list-item"]//a/@href')

def main(_):
    console.print("Initializing!", style="green on black")
    Takeover_ch().scrape()

if __name__ == '__main__':
    app.run(main)
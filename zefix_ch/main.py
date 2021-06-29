import json

from absl import app, flags

from rich import inspect, pretty
from rich.live import Live
from rich.console import Console

import requests

console = Console()
pretty.install()



FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_integer('page_size', 500, 'Number of results for each page.')
flags.DEFINE_string('output_file', 'output.jsonl', 'Name of the file.')


class Zefix_ch():
    def __init__(self):
        self.output_file = FLAGS.output_file
        self.page_size = FLAGS.page_size


    def scrape(self):
        self.session = requests.Session()
        self.set_zefix_config()
        self.send_post()
        self.parse_zefix_json()

        with open(self.output_file, 'a+') as f:
            f.write(self.results)


    def parse_zefix_json(self):
        self.results = ''
        for result in self.response.json()['list']:
            office_url = self.config[result['registerOfficeId']]['url2']
            external_link = self.get_link(result['uid'], office_url)
            result['external_link'] = external_link
            self.results += json.dumps(result) + '\n'
        

        # inspect(self.response.json())


    def get_link(self,uid,office_link):
        uid_formatted = f'{uid[0:3]}-{uid[3:6]}.{uid[6:9]}.{uid[9:12]}'
        return office_link.replace('#', uid_formatted)


    

    def send_post(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8'
        }

        post_body = {
            'name':'__',
            'languageKey':'en',
            'deletedFirms': 'true',
            'searchType':'exact',
            'maxEntries':self.page_size,
            'offset':0
        }

        self.response = self.session.post(
            'https://www.zefix.ch/ZefixREST/api/v1/firm/search.json',
            headers=headers,
            json=post_body)

    
    def set_zefix_config(self):
        with open('registry_offices.json', 'r') as f:
            ro = list(json.loads(f.read()))

        self.config = {}
        for result in ro:
            self.config[result['id']]=result



    def get_zefix_config():
        zefix_global = requests.get('https://www.zefix.ch/ZefixREST/api/v1/appConfigData.json').json()
        with open('output.json', 'w') as f:
            json.dump(zefix_global["registryOffices"], f, indent=4, ensure_ascii=False)
            


        

def main(_):
    console.print("Initializing!", style="green on black")
    Zefix_ch().scrape()

if __name__ == '__main__':
    app.run(main)
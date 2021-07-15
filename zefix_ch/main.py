from absl import app, flags

import Chregister
import Hrcintapp
from concurrent.futures import ThreadPoolExecutor




from rich import inspect, pretty
from rich.live import Live
from rich.console import Console


import json
import random
import requests
import re
import time

console = Console()
pretty.install()

FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_integer('page_size', 20, 'Number of results for each page.')
flags.DEFINE_integer('parallel_requests', 20, 'Name of the file.')
flags.DEFINE_string('output_file', './output.jsonl', 'Name of the file.')


class Zefix_ch():
    def __init__(self):
        self.output_file = FLAGS.output_file
        self.page_size = FLAGS.page_size
        self.parallel_requests = FLAGS.parallel_requests
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
        self.session = requests.Session()
        self.offset = 0
        self.wildcard = '__'

        self.headers = {
            'User-Agent':self.user_agent
        }

    def scrape(self):
        self.set_zefix_config()
        self.send_post()
        _next = self.response.json()['hasMoreResults']
        print(f"Has more results? {_next}")
        self.parse_zefix()

        with open(self.output_file, 'a+') as f:
            f.write(self.results)

        if self.response.json()['hasMoreResults'] == True:
            self.offset += self.page_size
            print(f'Scraping offset: {self.offset}')
            self.scrape()
        elif self.wildcard == '__':
            self.wildcard = '_ _'
            self.scrape()
        else:
            print('Finished Scraping')

    def parse_zefix(self):
        print('Start Loop')
        self.counter = 0
        start = time.time()
        self.results = ''
        with ThreadPoolExecutor(max_workers=self.parallel_requests) as executor:
            executor.map(self.transform,self.response.json()['list'])

        end = time.time()
        total_time = end - start
        print(f"It took {total_time} seconds to scrape")

    def transform(self,result):
        if len(result) > 0:
            self.counter += 1
            external_link = self.get_link(result)
            result['external_link'] = external_link
            result['table_results'] = self.follow_external_link(external_link)
        else:
            print(result)
        self.results += json.dumps(result, indent=4,ensure_ascii=False) + '\n'       

    def follow_external_link(self,url):
        try:
            if 'chregister.ch' in url:
                response = requests.get(url,headers = self.headers)
                return Chregister.Chregister(response).table_results
                
            elif 'hrcintapp/' in url:
                url = url.replace('externalCompanyReport','companyReport') + '&lang=EN'
                response = requests.get(url, headers = self.headers)
                return Hrcintapp.Hrcintapp(response).table_results

            elif 'prestations' in url:
                prestations_url = 'https://prestations.vd.ch/pub/101266/api/public/hrcexcerpts/'
                if 'CHE' not in url:
                    return 'No CHE in url'

                uid = re.search(r'(CHE.+)$', url)[1]
                
                headers = {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Content-Type': 'application/json',
                    'User-Agent': self.user_agent ,
                    # 'X-XSRF-TOKEN': 'bf16c53b-f1bc-4485-adfc-769be3f9a210'
                }
                body =  {"rcentId":"","lng":"EN","rad":True,
                        "companyOfsUid":uid,
                        "extraitTravail":True,
                        "admOrderDirection":"ASC",
                        "order":"R"}

                response = requests.post(
                    prestations_url,
                    headers=headers,
                    json=body,
                    allow_redirects=False,
                    
                )
                try:
                    data = response.json()
                except Exception as e:
                    data = 'There was a 302 problem'
                return data

            else:
                return 'Not in a scraper'
        except Exception as e:
            print(e ,url)
            return('Cannot find')
        
            

    def get_link(self,result):
        uid = result['uid']
        uid_formatted = f'{uid[0:3]}-{uid[3:6]}.{uid[6:9]}.{uid[9:12]}'
        if result['status'] == 'GELOESCHT':
            link = self.config[result['registerOfficeId']]['url4']
            link = link.replace('#', uid_formatted).replace('de','en')
            link = link.replace('NNNNNNNN',result['shabDate'].replace('-',''))
        else:
            link = self.config[result['registerOfficeId']]['url2']
            link = link.replace('#', uid_formatted)

        return link.replace('lang=FR','lang=EN')

    def send_post(self):
        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json;charset=UTF-8'
        }

        post_body = {
            'name':self.wildcard,
            'languageKey':'en',
            'deletedFirms': 'true',
            'searchType':'exact',
            'maxEntries':self.page_size,
            'offset':self.offset
        }

        self.response = self.session.post(
            'https://www.zefix.ch/ZefixREST/api/v1/firm/search.json',
            headers=headers,
            json=post_body
        )

    
    def set_zefix_config(self):
        with open('registry_offices.json', 'r') as f:
            registry_offices = list(json.loads(f.read()))

        self.config = {}
        for result in registry_offices:
            self.config[result['id']]=result



    def get_zefix_config():
        zefix_global = requests.get(
            'https://www.zefix.ch/ZefixREST/api/v1/appConfigData.json'
            ).json()

        with open('output.json', 'w') as f:
            json.dump(
                zefix_global["registryOffices"], f, 
                indent=4, 
                ensure_ascii=False
            )
            

def main(_):
    console.print("Initializing!", style="green on black")
    Zefix_ch().scrape()

if __name__ == '__main__':
    app.run(main)
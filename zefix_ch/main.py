from absl import app, flags
from lxml import html

from rich import inspect, pretty
from rich.live import Live
from rich.console import Console

import json
import requests

console = Console()
pretty.install()



FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_integer('page_size', 20, 'Number of results for each page.')
flags.DEFINE_string('output_file', 'output.jsonl', 'Name of the file.')


class Zefix_ch():
    def __init__(self):
        self.session = requests.Session()
        self.output_file = FLAGS.output_file
        self.page_size = FLAGS.page_size


    def scrape(self):
        self.set_zefix_config()
        self.send_post()
        self.parse_zefix()

        with open(self.output_file, 'a+') as f:
            f.write(self.results)


    def parse_zefix(self):
        self.results = ''
        for result in self.response.json()['list']:
            external_link = self.get_link(result)
            result['external_link'] = external_link
            result['table_results'] = self.follow_external_link(external_link)
            
            self.results += json.dumps(result, indent=4,ensure_ascii=False) + '\n'

    def follow_external_link(self,url):
        print(f'Following {url} . . .')
        if '.xhtml' in url:
            response = requests.get(url)
            nonces = response.headers['Content-Security-Policy']
            nonce = nonces.split(' ')[-1].replace('nonce-','')

            tree = html.fromstring(html=response.text)
            view_state = tree.xpath('//input[@type="hidden" and @name="javax.faces.ViewState"]/@value')

            form_data = {
                'javax.faces.partial.ajax': 'true',
                'javax.faces.source': 'idAuszugForm:auszugContentPanel',
                'primefaces.ignoreautoupdate': 'true',
                'javax.faces.partial.execute': 'idAuszugForm:auszugContentPanel',
                'javax.faces.partial.render': 'idAuszugForm:auszugContentPanel',
                'idAuszugForm:auszugContentPanel': 'idAuszugForm:auszugContentPanel',
                'idAuszugForm:auszugContentPanel_load': 'true',
                'idAuszugForm': 'idAuszugForm',
                'javax.faces.ViewState': view_state,
                'primefaces.nonce': nonce,
            }

            headers = {
                'Faces-Request': 'partial/ajax',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }

            resp = self.session.post(response.url.split('?')[0] + 
                                ';jsessionid=' + response.cookies['JSESSIONID'], 
                                data=form_data, 
                                headers=headers, 
                                cookies=response.cookies)



            tree = html.fromstring(resp.text.encode())
            tables = tree.xpath('//table')
            table_results = []
            for table in tables:
                theads = table.xpath('.//thead/tr/th')
                trs = table.xpath('.//tbody/tr')
                results = {}
                keys = []
                for th_val in theads:
                    texts = th_val.xpath('.//text()')
                    key = ''.join(texts).strip()
                    keys.append(key)
                    results[key] = []
                for tr in trs:
                    tds = tr.xpath('.//td')

                    for idx, td_val in enumerate(tds):
                        values = td_val.xpath('.//text()')
                        value = ''.join(values).strip()
                        results[keys[idx]].append(value)
                table_results.append(results)    
            return table_results


    def get_link(self,result):
        uid = result['uid']
        uid_formatted = f'{uid[0:3]}-{uid[3:6]}.{uid[6:9]}.{uid[9:12]}'
        if result['status'] == 'GELOESCHT':
            link = self.config[result['registerOfficeId']]['url4']
            link = link.replace('#', uid_formatted).replace('de','en')
            return link.replace('NNNNNNNN',result['shabDate'].replace('-',''))
        else:
            office_link = self.config[result['registerOfficeId']]['url2']
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
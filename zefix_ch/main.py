from absl import app, flags
from lxml import html

from rich import inspect, pretty
from rich.live import Live
from rich.console import Console

import json
import requests
import re

console = Console()
pretty.install()


FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_integer('page_size', 20, 'Number of results for each page.')
flags.DEFINE_string('output_file', 'output.jsonl', 'Name of the file.')


class Zefix_ch():
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
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
        if 'chregister.ch' in url:
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

        elif 'prestations' in url:
            prestations_url = 'https://prestations.vd.ch/pub/101266/api/public/hrcexcerpts/'
            uid = re.search(r'(CHE.+)$', url)[1]

            headers = {
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }
            body =  {"rcentId":"","lng":"EN","rad":True,
                    "companyOfsUid":uid,
                    "extraitTravail":True,
                    "admOrderDirection":"ASC",
                    "order":"R"}

            response =requests.post(prestations_url,headers=headers,json=body)
            return response.json()

        elif 'ge.ch' in url:
            # change url to companyReport
            url = url.replace('externalCompanyReport','companyReport') + '&lang=EN'
            response = requests.get(url)
            tree = html.fromstring(html=response.text)
            tables = tree.xpath('//table[@border=1]')
            
            table_results = []
            for table in tables:
                tr_with_th = table.xpath('.//tr[th]')
                tr_td_only = table.xpath('.//tr[td]')
                
                results = {}
                keys = []
                parent_keys = []
                
                if len(tr_with_th) == 2:
                    for value in tr_with_th[0]:
                        try:
                            colspan=int(value.xpath('@colspan')[0])
                        except:
                            colspan=1
                        if colspan > 0:
                            for n in range(colspan):
                                texts = value.xpath('.//text()')
                                key = ''.join(texts).strip() 
                                parent_keys.append(key)
                        else:
                            texts = value.xpath('.//text()')
                            key = ''.join(texts).strip() 
                            parent_keys.append(key)

                            
                    for value in tr_with_th[1]:
                        try:
                            colspan=int(value.xpath('@colspan')[0])
                        except:
                            colspan=1
                        if colspan > 0:
                            for n in range(colspan):
                                texts = value.xpath('.//text()')
                                key = ''.join(texts).strip() 
                                keys.append(key)
                        else:
                            texts = value.xpath('.//text()')
                            key = ''.join(texts).strip() 
                            keys.append(key)
                        results[key] = []
                            
                elif len(tr_with_th) == 1:
                    for value in tr_with_th[0]:
                        try:
                            colspan=int(value.xpath('@colspan')[0])
                        except:
                            colspan=1
                        if colspan > 0:
                            for n in range(colspan):
                                texts = value.xpath('.//text()')
                                key = ''.join(texts).strip() 
                                keys.append(key)
                        else:
                            texts = value.xpath('.//text()')
                            key = ''.join(texts).strip() 
                            keys.append(key)
                            
                        results[key] = []
                
                if len(parent_keys) > 0:
                    results = {}
                    for p_key in parent_keys:
                        results[p_key] = []
                    key_array = {}
                    for idx,key in enumerate(keys):
                        results[parent_keys[idx]].append({key})
                    
                    print(results)
                    for trs_with_td in tr_td_only:
                        n = 0
                        for idx, td_val in enumerate(trs_with_td):
                            values = td_val.xpath('.//text()')
                            value = ''.join(values).strip()
                            
                            if parent_keys[idx] == 'Capital shares':
                                results[parent_keys[idx]][n] = {keys[idx] : value}
                                n+=1
                            elif parent_keys[idx] == parent_keys[idx-1]:
                                results[parent_keys[idx]][1] = {keys[idx] : value}
                            else:
                                results[parent_keys[idx]][0] = {keys[idx] : value}
                                n=0
                    
                else:
                    for trs_with_td in tr_td_only:
                        for idx, td_val in enumerate(trs_with_td):
                            values = td_val.xpath('.//text()')
                            value = ''.join(values).strip()
                            results[keys[idx]].append(value)
                            
                return results
                


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
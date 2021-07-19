from lxml import html
import requests

from rich import inspect
import re

class Chregister():
    def __init__(self, response,text):
        self.scrape(response,text)

    def scrape(self,response,text):
        nonces = response.headers['Content-Security-Policy']
        nonce = nonces.split(' ')[-1].replace('nonce-','')
        response_url = str(response.url)
        response_cookies = str(response.cookies['JSESSIONID'])
        response_cookies = re.search(r'JSESSIONID=([^\;]+)', response_cookies)[1]
        inspect(response.cookies)
        post_url = response_url.split(';')[0] + ';jsessionid=' + response_cookies
        tree = html.fromstring(html=text)
        view_state = tree.xpath('//input[@type="hidden" and @name="javax.faces.ViewState"]/@value')[0]

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

        resp = requests.post(post_url, 
                            data=form_data, 
                            headers=headers, 
                            cookies=str(response.cookies))

        tree = html.fromstring(resp.text.encode())
        tables = tree.xpath('//table')
        self.table_results = []
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
            self.table_results.append(results)    
from lxml import html

class Hrcintapp():
    def __init__(self, response):
        self.scrape(response)
    def p_keys_and_values_map(self,colspan):
        for _ in range(colspan):
            td_text_value = self.get_td_text_value()
            self.parent_keys.append(td_text_value)
            
    def keys_and_values_map(self,colspan):
        for _ in range(colspan):
            td_text_value = self.get_td_text_value()
        self.keys.append(td_text_value)
            
    def get_td_text_value(self):
        texts = self.value.xpath('.//text()')
        value = ''.join(texts).strip()
        return value
    
    def get_colspan(self):
        try:
            colspan=int(self.value.xpath('@colspan')[0])
        except:
            colspan=1
        return colspan

    
    def scrape(self, response):
        tree = html.fromstring(response.text)
        self.tables = tree.xpath('//table[@border=1]')
        self.table_results = []
        
        for table in self.tables:
            tr_with_th = table.xpath('.//tr[th]')
            tr_td_only = table.xpath('.//tr[td]')
            results = {}
            self.parent_keys = []
            self.keys = []

            if len(tr_with_th) == 2:
                for self.value in tr_with_th[0]:
                    self.p_keys_and_values_map(self.get_colspan())
                for self.value in tr_with_th[1]:
                    self.keys_and_values_map(self.get_colspan())
                    
            elif len(tr_with_th) > 0:
                for self.value in tr_with_th[0]:
                    self.keys_and_values_map(self.get_colspan())
                    
            else:
                print('No TH found')
                
            # Parent_keys are the top level of two <tr> with <th>
            if len(self.parent_keys) > 0:
                for p_key in self.parent_keys:
                    results[p_key] = []
                for idx,key in enumerate(self.keys):
                    results[self.parent_keys[idx]].append({key})
                values = []
                for trs_with_td in tr_td_only:
                    for idx, self.value in enumerate(trs_with_td.xpath('.//td')):
                        values.append(self.get_td_text_value())

                n=0
                for idx, key in enumerate(self.keys):
                    lower_index = idx
                    upper_index = lower_index + len(self.keys)

                    v = ";".join([e for i, e in enumerate(values) 
                                    if i in [lower_index,upper_index]]
                            ).split(';')
                    results[self.parent_keys[idx]][n]= {key :v}
                    if idx == len(self.parent_keys)-1:
                        continue
                    elif self.parent_keys[idx] == self.parent_keys[idx+1]:
                        n+=1
                    else:
                        n=0

            else:
                for key in self.keys:
                    results[key] = []

                for trs_with_td in tr_td_only:
                    for idx, self.value in enumerate(trs_with_td):
                        value = self.get_td_text_value()
                        results[self.keys[idx]].append(value)
            self.table_results.append(results)
        
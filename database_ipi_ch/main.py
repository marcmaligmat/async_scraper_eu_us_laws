import base64
import json
from time import sleep

import re
import requests
from rich import inspect, pretty
from rich.progress import Progress
from rich.live import Live

from post_data import post_data_from_oldest
pretty.install()

# Results = PAGE_SIZE * LOOP
PAGE_SIZE = 64 #use 64 as default
LOOP = 500
OUTPUT_FILE = 'output.jsonl'
LAST_CURSOR_FILE = 'last_cursor.jsonl'





total = 100 
NUM = 0

def generate_string(num1):
    return f"Scraped {num1} / {PAGE_SIZE * LOOP} "


def print_scraped_number(num):
    with Live(generate_string(num), refresh_per_second=4) as live:
        live.update(generate_string(num))
        num += PAGE_SIZE


def run(session):
    cursor = {
        'last_cursor':'*',
        'page_number': 0,
        'expected_results': 0
    }
    num = 0
    # with Progress() as progress:
    #     task = progress.add_task(f"[cyan]Scraping...", total=LOOP)
        
    with Live(generate_string(num), refresh_per_second=4) as live:
        with open(OUTPUT_FILE, 'a+') as f:
        
            for _ in range(LOOP):
                try:
                    cursor = get_last_cursor_object()
                except:
                    save_last_cursor(cursor)

                response = send_post(session,cursor['last_cursor'])
                api_results = response.json()['results']

                results = '';
                for result in api_results:
                    
                    if "bild_screen_hash__type_string_mv" in result.keys():
                        result['base64_logo'] = [base64_decoded_utf8(result["bild_screen_hash__type_string_mv"][0])]
                    results += json.dumps(result) + '\n'
                    

                    num += 1
                    live.update(generate_string(num))
                f.write(results)

                cursor = {
                    'last_cursor':get_next_cursor(response),
                    'page_number': cursor['page_number'] + 1,
                    'expected_results': cursor['expected_results'] + PAGE_SIZE
                }
                save_last_cursor(cursor)

                # if not progress.finished:
                #     progress.update(task, advance = 1)
                f.close()




def send_post(session,cursor):
    headers = {
        'content-type': 'application/transit+json',
        'X-IPI-VERSION': '2.1.3',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    
    response = session.post(
        f'https://database.ipi.ch/database/resources/query/fetch?ps={PAGE_SIZE}', 
        headers=headers, 
        json=post_data_from_oldest(PAGE_SIZE,cursor))

    return response


def get_next_cursor(response):
    cursor_result = response.json()['metadataAsTransit']
    cursor = cursor_result.replace('\\', '')
    return json.loads(cursor)['~#resultmeta']['~:cursor']['~#opt']


def base64_decoded_utf8(image_slug):
    url = f"https://database.ipi.ch/database/resources/image/{image_slug}"
    base64_encoded_data = base64.b64encode(requests.get(url).content)
    return base64_encoded_data.decode('utf-8')


def transform_to_image(base64_img):
    base64_img_bytes = base64_img.encode('UTF-8') 
    with open('decoded_image.png', 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)


def save_last_cursor(last_cursor):
    handle_jsonl('w+',last_cursor, LAST_CURSOR_FILE)


def open_last_cursor():
    f = open("last_cursor.txt", "r")
    words = f.read()
    m = re.search(r'last_cursor:(.+)',words)
    return m.group(1)


def handle_jsonl(mode, json_data, output_file):
    """ Example mode: 'w+','a+' """
    with open(output_file, mode) as f:
        f.write(json.dumps(json_data) + '\n')
        # json.dump(json_data, outfile,ensure_ascii=False, indent=4)
        # outfile.write('\n')
        


def get_last_cursor_object():
    """Returns a dictionary from last_cursor.jsonl file"""
    with open('last_cursor.jsonl', 'r') as json_file:
        json_list = list(json_file)
        last_cursor_object = ''

        for _list in json_list:
            _dict = _list.splitlines()
            last_cursor_object += _dict[0]

        return json.loads(last_cursor_object)

if __name__ == '__main__':
    session = requests.Session()
    run(session)


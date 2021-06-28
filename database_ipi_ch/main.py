import base64
import json

from absl import app, flags
from math import ceil

from rich import pretty
from rich.live import Live
from rich.console import Console

from post_data import post_data_from_oldest

import re
import requests
import os

console = Console()
pretty.install()



FLAGS = flags.FLAGS
flags.DEFINE_boolean('debug', False, 'Produces debugging output.')
flags.DEFINE_integer('page_size', 64, 'Number of results for each page.')
flags.DEFINE_string('output_file', 'output.jsonl', 'Name of the file.')
flags.DEFINE_string('last_cursor_file', 'last_cursor.jsonl', 'Last cursor file')




class Database_ipi_ch():
    def __init__(self):
        console.print("Initializing!", style="green on black")
        app.run(self.main)

    def main(self, argv):
        self.session = requests.Session()
        if FLAGS.debug:
            print('non-flag arguments:', argv)
        self.page_size = FLAGS.page_size

        self.output_file = FLAGS.output_file
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        cursor = {
            'last_cursor': '*',
            'page_number': 0,
            'expected_results': 0
        }
        num = 0

        try:
            cursor = self.get_last_cursor_object()
            num = cursor['expected_results']
            original_expected_results = cursor['expected_results']
        except:
            self.save_last_cursor(cursor)

        self.send_post(cursor['last_cursor'])
        self.set_total_items()
        self.loop = ceil(
            (self.total_items-cursor['expected_results'])/self.page_size)

        with Live() as live:
            with open(self.output_file, 'a+') as f:

                for _ in range(self.loop):
                    self.send_post(cursor['last_cursor'])
                    api_results = self.response.json()['results']

                    results = ''
                    for result in api_results:
                        if "bild_screen_hash__type_string_mv" in result.keys():
                            result['base64_logo'] = [self.base64_decoded_utf8(
                                result["bild_screen_hash__type_string_mv"][0])]
                        results += json.dumps(result) + '\n'

                        num += 1
                        live.update(self.generate_string(num))
                    f.write(results)

                    cursor = {
                        'last_cursor': self.get_next_cursor(),
                        'page_number': cursor['page_number'] + 1,
                        'expected_results': cursor['expected_results'] + self.page_size
                    }
                    self.save_last_cursor(cursor)

            f.close()

    def generate_string(self, num1):
        return f"Scraped {num1} / {self.total_items} "

    def send_post(self, cursor):
        headers = {
            'content-type': 'application/transit+json',
            'X-IPI-VERSION': '2.1.3',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
        }

        self.response = self.session.post(
            f'https://database.ipi.ch/database/resources/query/fetch?ps={self.page_size}',
            headers=headers,
            json=post_data_from_oldest(self.page_size, cursor))

    def get_next_cursor(self):
        cursor_result = self.response.json()['metadataAsTransit']
        cursor = cursor_result.replace('\\', '')
        return json.loads(cursor)['~#resultmeta']['~:cursor']['~#opt']

    def get_total_items(self):
        cursor_result = self.response.json()['metadataAsTransit']
        cursor = cursor_result.replace('\\', '')
        return json.loads(cursor)['~#resultmeta']['~:total-items']

    def set_total_items(self):
        self.total_items = self.get_total_items()

    def base64_decoded_utf8(self, image_slug):
        url = f"https://database.ipi.ch/database/resources/image/{image_slug}"
        base64_encoded_data = base64.b64encode(requests.get(url).content)
        return base64_encoded_data.decode('utf-8')

    def transform_to_image(self, base64_img):
        base64_img_bytes = base64_img.encode('UTF-8')
        with open('decoded_image.png', 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)

    def save_last_cursor(self, last_cursor):
        self.handle_jsonl('w+', last_cursor, FLAGS.last_cursor_file)

    def open_last_cursor(self):
        f = open("last_cursor.txt", "r")
        words = f.read()
        m = re.search(r'last_cursor:(.+)', words)
        return m.group(1)

    def handle_jsonl(self, mode, json_data, output_file):
        """ Example mode: 'w+','a+' """
        with open(output_file, mode) as f:
            f.write(json.dumps(json_data) + '\n')
            # json.dump(json_data, outfile,ensure_ascii=False, indent=4)
            # outfile.write('\n')

    def get_last_cursor_object(self):
        """Returns a dictionary from last_cursor.jsonl file"""
        with open('last_cursor.jsonl', 'r') as json_file:
            json_list = list(json_file)
            last_cursor_object = ''

            for _list in json_list:
                _dict = _list.splitlines()
                last_cursor_object += _dict[0]

            return json.loads(last_cursor_object)


if __name__ == '__main__':
    Database_ipi_ch()

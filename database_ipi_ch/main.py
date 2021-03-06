import base64
import json

from settings import Settings

from math import ceil

from rich import pretty
from rich.live import Live
from rich.console import Console

from post_data import post_data_from_oldest

import re
import requests
from minio import Minio
import os

console = Console()
pretty.install()

from Logger import _logger


def upload_to_minio(bucket, destination, filename):
    client = Minio(
        os.getenv("s3_endpoint"),
        access_key=os.getenv("s3_access_key"),
        secret_key=os.getenv("s3_secret_key"),
    )

    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
    else:
        print(f"Bucket {bucket} already exists")

    client.fput_object(
        bucket,
        destination,
        filename,
    )
    print(
        f"'{destination}' is successfully uploaded as "
        f"object '{filename}' to bucket '{bucket}'."
    )


class Database_ipi_ch:
    def scrape(self):

        self.settings = Settings()
        self.session = requests.Session()
        self.logger = _logger(self.settings.error_file)
        self.output_file = self.settings.output_file

        self.bucket = self.settings.bucket
        self.destination_folder = self.settings.destination_folder
        self.last_cursor_destination = self.settings.last_cursor_destination
        self.output_file = self.settings.output_file

        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        cursor = {"last_cursor": "*", "page_number": 0, "expected_results": 0}
        num = 0

        try:
            cursor = self.get_last_cursor_object()
            num = cursor["expected_results"]
        except:
            self.save_last_cursor(cursor)

        self.send_post(cursor["last_cursor"])
        self.set_total_items()
        self.loop = ceil(
            (self.total_items - cursor["expected_results"]) / self.settings.page_size
        )

        with Live() as live:
            with open(self.output_file, "a+") as f:

                for _ in range(self.loop):
                    try:
                        self.send_post(cursor["last_cursor"])
                        api_results = self.response.json()["results"]

                        results = ""
                        for result in api_results:
                            if "bild_screen_hash__type_string_mv" in result.keys():
                                result["base64_logo"] = [
                                    self.base64_decoded_utf8(
                                        result["bild_screen_hash__type_string_mv"][0]
                                    )
                                ]
                            results += json.dumps(result) + "\n"

                            num += 1
                            live.update(self.generate_string(num))
                        f.write(results)

                        cursor = {
                            "last_cursor": self.get_next_cursor(),
                            "page_number": cursor["page_number"] + 1,
                            "expected_results": cursor["expected_results"]
                            + self.settings.page_size,
                        }
                        self.save_last_cursor(cursor)
                    except:
                        self.logger.exception(cursor["last_cursor"])

                    if self.settings.debug:
                        break

            try:

                upload_to_minio(self.bucket, self.destination_folder, self.output_file)

            except:
                self.logger.exception(self.output_file)

            try:
                upload_to_minio(
                    self.bucket,
                    self.last_cursor_destination,
                    self.settings.last_cursor_file,
                )
            except:
                self.logger.exception(self.settings.last_cursor_file)

    def generate_string(self, num1):
        return f"Scraped {num1} / {self.total_items} "

    def send_post(self, cursor):
        headers = {
            "content-type": "application/transit+json",
            "X-IPI-VERSION": "2.1.3",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        }

        self.response = self.session.post(
            f"https://database.ipi.ch/database/resources/query/fetch?ps={self.settings.page_size}",
            headers=headers,
            json=post_data_from_oldest(self.settings.page_size, cursor),
        )

    def get_next_cursor(self):
        cursor_result = self.response.json()["metadataAsTransit"]
        cursor = cursor_result.replace("\\", "")
        return json.loads(cursor)["~#resultmeta"]["~:cursor"]["~#opt"]

    def get_total_items(self):
        cursor_result = self.response.json()["metadataAsTransit"]
        cursor = cursor_result.replace("\\", "")
        return json.loads(cursor)["~#resultmeta"]["~:total-items"]

    def set_total_items(self):
        self.total_items = self.get_total_items()

    def base64_decoded_utf8(self, image_slug):
        url = f"https://database.ipi.ch/database/resources/image/{image_slug}"
        base64_encoded_data = base64.b64encode(requests.get(url).content)
        return base64_encoded_data.decode("utf-8")

    def transform_to_image(self, base64_img):
        base64_img_bytes = base64_img.encode("UTF-8")
        with open("decoded_image.png", "wb") as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)

    def save_last_cursor(self, last_cursor):
        with open(self.settings.last_cursor_file, "w") as f:
            json.dump(last_cursor, f)

    def get_last_cursor_object(self):
        """Returns a dictionary from last_cursor file"""
        with open(self.settings.last_cursor_file, "r") as json_file:
            cursor = json.load(json_file)
            return cursor


if __name__ == "__main__":
    console.print("Initializing!", style="green on black")
    Database_ipi_ch().scrape()

from scrapers_shared.shared_settings import SharedSettings
from minio import Minio
from minio.error import S3Error
import os


class Settings(SharedSettings):
    name = "database_ipi_ch"
    page_size: int = 8
    output_file: str = "./output.jsonl"
    last_cursor_file: str = "./last_cursor.json"

    cleaned_output_file = output_file.replace("./", "")
    cleaned_last_cursor_file = last_cursor_file.replace("./", "")
    destination_folder: str = f"{name}/{cleaned_output_file}"
    last_cursor_destination: str = f"{name}/{cleaned_last_cursor_file}"
    bucket: str = "marc-testing"
    error_file: str = "error.log"
    debug: bool = False

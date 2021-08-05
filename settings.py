from typing import Set

from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    s3_url: str = Field(..., env="s3_url")
    s3_access_key: str = Field(..., env="s3_access_key")
    s3_secret_key: str = Field(..., env="s3_secret_key")

    debug: bool = False
    page_size: int = 64
    output_file: str = "./output.jsonl"
    last_cursor_file: str = "./last_cursor.json"

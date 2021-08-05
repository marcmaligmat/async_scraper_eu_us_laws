from pydantic import (
    BaseSettings,
    Field,
)


class SharedSettings(BaseSettings):
    s3_url: str = Field(..., env="s3_url")
    s3_access_key: str = Field(..., env="s3_access_key")
    s3_secret_key: str = Field(..., env="s3_secret_key")

    debug: bool = False

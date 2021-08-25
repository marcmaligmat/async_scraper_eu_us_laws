from pydantic import (
    BaseSettings,
    Field,
)


class SharedSettings(BaseSettings):
    s3_endpoint: str = Field(..., env="s3_endpoint")
    s3_access_key: str = Field(..., env="s3_access_key")
    s3_secret_key: str = Field(..., env="s3_secret_key")

    debug: bool = False

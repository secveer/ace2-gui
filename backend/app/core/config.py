from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn


@lru_cache()
def get_settings():
    return Settings()

# CONFIG FILE

from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    env_name: str = 'Local'  # Name of the current environment
    base_url: str = 'http://localhost:8000'  # Domain of the app
    db_url: str = "sqlite:///./shortener.db"  # Database address

    class Config:
        env_file = "../.env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print('Loaded settings for', settings.env_name)
    return settings


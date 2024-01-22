from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    LOG_DIR: Path = Path('.logs')
    DEBUG: bool = True


config = Config()

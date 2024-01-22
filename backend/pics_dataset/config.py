from pathlib import Path

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    LOG_DIR: Path = Path('.logs')
    DEBUG: bool = True
    DB_DIR: Path = Path('.')

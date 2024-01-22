from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from pics_dataset.config import AppConfig


CONTROLLER: ContextVar[None] = ContextVar('main_controller', default=None)
engine: ContextVar[AsyncEngine | None] = ContextVar('engine', default=None)
async_session: ContextVar[async_sessionmaker | None] = ContextVar('async_session', default=None)
app_config: ContextVar[AppConfig] = ContextVar('app_config', default=AppConfig())

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from pics_dataset.config import AppConfig
from pics_dataset.context_vars import async_session, engine


log = logging.getLogger('db_utils')


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if session := async_session.get():
        async with session() as session:
            yield session
    else:
        raise RuntimeError('DB not initialized')


def get_connection_string(config: AppConfig, is_async=True):
    if is_async:
        return f'sqlite+aiosqlite:///{config.DB_DIR}/db.sqlite'
    return f'sqlite:///{config.DB_DIR}/db.sqlite'


def setup_engine(config: AppConfig):
    if engine.get() is not None:
        return engine.get()

    db_url = get_connection_string(config)
    log.info(f'DB path: {db_url}')
    created_engine = create_async_engine(db_url, query_cache_size=1200)
    created_async_session = async_sessionmaker(
        bind=created_engine, expire_on_commit=False, class_=AsyncSession
    )
    engine.set(created_engine)
    async_session.set(created_async_session)

    return created_engine

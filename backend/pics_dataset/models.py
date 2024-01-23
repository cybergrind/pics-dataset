import datetime
import logging

import sqlalchemy as db
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.main import SQLModel


Base = declarative_base(metadata=SQLModel.metadata)

log = logging.getLogger('models')


class DBBase:
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now(),
        onupdate=datetime.datetime.now(),
    )


class OriginalImage(Base, DBBase):
    __tablename__ = 'original_images'

    path = db.Column(db.String(1024), nullable=False, unique=True)
    backup_path = db.Column(db.String(1024), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False, index=True)
    sha1_hash = db.Column(db.String(40), nullable=True, index=True)


class Image(Base, DBBase):
    __tablename__ = 'images'

    path = db.Column(db.String(1024), nullable=False, unique=True)
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False, default=False, index=True)
    sha1_hash = db.Column(db.String(40), nullable=True, index=True)

    @classmethod
    async def get_top_n_query(cls, session: AsyncSession, n=10):
        count = (await session.exec(select(func.count(Image.id)).where(~Image.hidden))).all()[0]
        log.debug(f'{count=}')
        return (
            await session.exec(
                select(Image)
                .where(~Image.hidden)
                .order_by(Image.elo_rating.desc())
                .limit(int(count / 10))
            )
        ).all()

    @classmethod
    async def get_in_dir(cls, session: AsyncSession, path: str):
        return (await session.exec(select(Image).where(Image.path.startswith(path)))).all()

    @classmethod
    async def get_by_path(cls, session: AsyncSession, path: str) -> 'Image':
        return (await session.exec(select(Image).where(Image.path == path))).first()


class Bookmark(Base, DBBase):
    __tablename__ = 'bookmarks'

    name = db.Column(db.String(1024), nullable=False, unique=True)
    path = db.Column(db.String(1024), nullable=False, unique=True)

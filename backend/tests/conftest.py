import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from pics_dataset.app import get_app  # FastAPI


@pytest.fixture()
async def app() -> FastAPI:
    return get_app()


@pytest.fixture()
async def client(app):
    async with AsyncClient(app=app, base_url='http://test') as cli:
        yield cli

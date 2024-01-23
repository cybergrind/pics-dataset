import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request, WebSocket
from fastapi.responses import FileResponse
from prometheus_client import Gauge
from starlette_exporter import PrometheusMiddleware, handle_metrics

from pics_dataset.logs import setup_logging


setup_logging()
UP = Gauge('up', 'Pics Dataset Worker is up', ['app'])
UP.labels(app='pics_dataset').set(1)

STATIC = Path('./frontend/pics-dataset/build')
INDEX = STATIC / 'index.html'

log = logging.getLogger('app')

for name in ['aioboto3', 'aiobotocore', 'kubernetes_asyncio']:
    logging.getLogger(name).setLevel(logging.INFO)


root = APIRouter()
root.add_route('/metrics', handle_metrics)


@root.get('/')
async def index():
    return FileResponse(INDEX)


@root.get('/static/{file_path:path}')
async def get_static(file_path: str):
    path = STATIC / file_path
    path2 = STATIC / (file_path + '.html')
    if path.is_file() and path.is_relative_to(STATIC):
        return FileResponse(path)
    elif path2.is_file() and path2.is_relative_to(STATIC):
        return FileResponse(path2)
    return FileResponse(INDEX, media_type='text/html')


@root.websocket('/api/ws')
async def ws(sock: WebSocket):
    try:
        await sock.accept()
        await sock.send_json({'status': 'connected'})
        while True:
            msg = await sock.receive_json()
            log.debug(f'WS: {msg=}')
    except Exception as e:
        log.exception(f'WS error: {e}')


async def setup_controllers():
    pass


async def shutdown_controllers():
    pass


@asynccontextmanager
async def lifespan(app):
    await setup_controllers()
    try:
        yield
    finally:
        await shutdown_controllers()


async def errors_logging_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        log.exception(e)
        raise


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(root)
    app.add_middleware(
        PrometheusMiddleware,
        app_name='snapshot_manager',
        skip_paths=['/metrics'],
        filter_unhandled_paths=True,
    )
    app.middleware('http')(errors_logging_middleware)
    return app

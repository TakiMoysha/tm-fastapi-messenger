from contextlib import asynccontextmanager
from functools import partial
from logging import getLogger
from typing import AsyncGenerator
from weakref import WeakKeyDictionary

import fastapi
import httpx
from anyio import Event, create_task_group, sleep
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.lib.cache import ICache
from app.lib.utils.websockets import ws_heartbeat

from jwt_auth.exceptions import BaseJWTAuthError

logger = getLogger(__name__)


# ========================================================================================
@asynccontextmanager
async def ws_manager(websocket: WebSocket, cache: ICache) -> AsyncGenerator[WebSocket, None]:
    await websocket.accept()
    cache.set(websocket.scope["session"], websocket)

    async with create_task_group() as tg:
        tg.start_soon(partial(ws_heartbeat, websocket))

    try:
        yield websocket
    except WebSocketDisconnect as err:
        logger.info("WEBSOCKET DISCONNECT:", exc_info=err)
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)
    except Exception as err:
        logger.error("UNEXPECTED ERROR:", exc_info=err)
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        cache.delete(websocket.scope["session"])
        await websocket.close()


# ========================================================================================
client_cache: WeakKeyDictionary[fastapi.FastAPI, httpx.AsyncClient] = WeakKeyDictionary()


def client_for_app(app: fastapi.FastAPI) -> httpx.AsyncClient:
    if app in client_cache:
        return client_cache[app]

    transport = httpx.ASGITransport(app=app)
    client_cache[app] = httpx.AsyncClient(transport=transport)
    return client_cache[app]

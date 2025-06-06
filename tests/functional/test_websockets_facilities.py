from logging import getLogger
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import pytest

from app.dependencies import DepStateCache
from app.lib.utils.websockets import ws_heartbeat
from app.helpers import ws_manager

logger = getLogger(__name__)
pytestmark = pytest.mark.asyncio


# https://github.com/litestar-org/litestar/pull/4098/files
# =============================================================
class WebsocketManager:
    def __init__(self) -> None:
        pass

    def stream(self): ...

    def send_ping(self): ...


async def provide_websocket_manager(websocket: WebSocket, cache: DepStateCache):
    return await ws_manager(websocket, cache)


DepWebsocket = Annotated[WebSocket, Depends(provide_websocket_manager)]


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    yield await {"hello": "world"}


# =============================================================
def test_ws_heartbeat():
    client = TestClient(app)
    with client.websocket_connect("/ws") as ws:
        data = ws.receive_json()
        logger.info(data)

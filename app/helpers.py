from logging import getLogger

from contextlib import asynccontextmanager
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.lib.cache import ICache

logger = getLogger(__name__)


@asynccontextmanager
async def ws_manager(websocket: WebSocket, cache: ICache):
    await websocket.accept()
    cache.set(websocket.scope["session"], websocket)
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


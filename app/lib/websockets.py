import asyncio
from logging import getLogger

from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from app.config import get_config

logger = getLogger(__name__)
config = get_config()


async def ws_heartbeat(ws: WebSocket) -> bool | None:
    if not (ws.application_state == WebSocketState.CONNECTED and ws.client_state == WebSocketState.CONNECTED):
        return False

    try:
        _ = await asyncio.wait_for(ws.send_bytes(b"PING"), timeout=config.server.ws_heartbeat_timeout)
        r = await asyncio.wait_for(ws.receive_bytes(), timeout=config.server.ws_heartbeat_timeout)
        assert r == b"PONG"
    except (asyncio.TimeoutError, AssertionError) as err:
        err.add_note(f"stale ws connection <{repr(ws)}>")
        raise WebSocketDisconnect from err
    except Exception as err:
        err.add_note(f"UNEXPECTED ws connection error <{repr(ws)}>")
        raise WebSocketDisconnect from err

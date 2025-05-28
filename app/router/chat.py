import asyncio
from logging import getLogger

from fastapi import APIRouter, Path, Query, status
from fastapi.websockets import WebSocket

from app.dependencies import DepAlchemySession, DepAuthToken, DepStateCache
from app.helpers import ws_manager
from app.lib.utils.websockets import ws_heartbeat

logger = getLogger(__name__)
router = APIRouter(tags=["resources"])


@router.websocket("/ws/chats/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    auth_token: DepAuthToken,
    cache: DepStateCache,
    chat_id: int = Path(gt=0),
):
    async def _input_handler(ws):
        msg = await ws.recv()

    async def _stream_handler(ws):
        pass

    with ws_manager(websocket, cache) as ws:
        await asyncio.gather(
            _input_handler(websocket),
            _stream_handler(websocket),
            ws_heartbeat(websocket),  # !TODO: move to ws_manager
        )


@router.get(
    "/api/chats/{chat_id}/hisitory",
    status_code=status.HTTP_200_OK,
)
async def health_get(
    auth_token: DepAuthToken,
    session: DepAlchemySession,
    chat_id: int = Path(gt=0),
    limit: int = Query(default=10, gt=0),
    offset: int = Query(default=0, ge=0),
):
    return {"id": chat_id, "limit": limit, "offset": offset}

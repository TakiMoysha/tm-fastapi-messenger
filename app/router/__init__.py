from logging import getLogger

from fastapi import APIRouter, HTTPException, status

from app.dependencies import DepAlchemySession, DepAuthToken

from app.lib.health import check_database
from app.urls import URL_HEALTH

from .accounts import router as account_router
from .chat import router as chat_router
from .users import router as user_router

logger = getLogger(__name__)

root_router = APIRouter()

# ================================================================================================
support_router = APIRouter()


@support_router.get(URL_HEALTH, status_code=status.HTTP_200_OK, tags=["health"])
async def health_get(session: DepAlchemySession):
    detail = {
        "database": await check_database(session),
    }

    if all(value == "ok" for value in detail.values()):
        return {"status": "ok", "detail": detail}
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )


root_router.include_router(support_router)
root_router.include_router(account_router)
root_router.include_router(user_router)
root_router.include_router(chat_router)

from logging import getLogger

from fastapi import APIRouter, HTTPException, status
from fastapi.security import SecurityScopes

from app.dependencies import DepAlchemySession

from app.lib.health import check_database
from app.urls import URL_HEALTH

logger = getLogger(__name__)
router = APIRouter()


@router.get(URL_HEALTH, status_code=status.HTTP_200_OK, tags=["health"])
async def health_get(session: DepAlchemySession, scope: SecurityScopes):
    logger.info(f"health_get security_scope: <{scope.scopes}>")

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

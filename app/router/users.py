from logging import getLogger
from fastapi import APIRouter

from app.dependencies import (
    DepAccountService,
    DepAuthToken,
)

from advanced_alchemy.extensions.fastapi import filters

logger = getLogger(__name__)

router = APIRouter(tags=["resources"])


@router.get("/users")
async def list_users(
    accounts_service: DepAccountService,
):
    results, total = await accounts_service.list_and_count(filters.LimitOffset(limit=10, offset=0))

    logger.info(f"list_users: <{str(results), total}>")
    return results


@router.get("/users/me")
async def get_herself(
    accounts_service: DepAccountService,
    user: DepAccountService,
    auth_token: DepAuthToken,
):
    return user

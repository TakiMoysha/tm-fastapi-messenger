from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from pydantic.fields import Field
from pydantic.types import SecretStr


from advanced_alchemy.extensions.fastapi import filters

from app.dependencies import (
    DepAccountService,
    DepAuthToken,
    DepAlchemySession,
    DepAuthToken,
    DepAccountService,
)
from app.domain.accounts.services import AccountService
from app.lib.health import check_database
from app.domain.base.schemas import BaseSchema

from .chat import router as chat_router

logger = getLogger(__name__)

root_router = APIRouter()

# ================================================================================================
api_router = APIRouter()


@api_router.get("/healthz", status_code=status.HTTP_200_OK, tags=["health"])
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


@api_router.get(
    "/healthz/auth",
    status_code=status.HTTP_200_OK,
    tags=["health"],
)
async def authorization_healthz(session: DepAlchemySession, auth_token: DepAuthToken):
    return {"token": auth_token}


# ================================================================================================
router = APIRouter(tags=["accounts"])


class AccountRegistrionSchema(BaseSchema):
    email: EmailStr
    password: SecretStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "Vx2yj@example.com",
                "password": "secret",
            },
        }


@router.post(
    "/api/auth/sign-up",
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    input: AccountRegistrionSchema,
    accounts_service: DepAccountService,
):
    # res = await accounts_service.registration(email=input.email, password=input.password)
    res = await accounts_service.get_one_or_none(email=input.email)
    return {"done": "OK"}


class UserSchema(BaseSchema):
    email: EmailStr
    password: SecretStr


@router.get(
    "/users/me",
    response_model=UserSchema,
    tags=["accounts"],
)
async def get_herself(
    accounts_service: DepAccountService,
    user: DepAccountService,
    auth_token: DepAuthToken,
):
    return user


@router.get("/users", tags=["accounts"])
async def list_users(
    accounts_service: DepAccountService,
):
    results, total = await accounts_service.list_and_count(filters.LimitOffset(limit=10, offset=0))

    logger.info(f"list_users: <{str(results), total}>")
    return {
        "data": results,
    }


api_router.include_router(router)

root_router.include_router(api_router)
root_router.include_router(chat_router)

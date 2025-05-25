from logging import getLogger

from fastapi import APIRouter, status
from fastapi.background import BackgroundTasks
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from pydantic.types import SecretStr

from app import urls
from app import dependencies as deps
from app.domain.base.schemas import BaseSchema

logger = getLogger(__name__)

router = APIRouter(tags=["accounts"])

# ======================================= SCHEMAS


class AccountSignUpSchema(BaseSchema):
    email: EmailStr
    password: SecretStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "Vx2yj@example.com",
                "password": "secret",
            },
        }


class AccountSignInSchema(BaseSchema):
    email: EmailStr
    password: SecretStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "Vx2yj@example.com",
                "password": "secret",
            },
        }


class AccountSignInOutSchema(BaseSchema):
    class Config:
        json_schema_extra = {
            "example": {
                "email": "Vx2yj@example.com",
            },
        }


# ======================================= ENDPOINTS


@router.post(
    urls.URL_ACCOUNT_SIGN_UP,
    status_code=status.HTTP_201_CREATED,
)
async def account_sign_up(
    data: AccountSignUpSchema,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
    tasks: BackgroundTasks,
):
    res = await accounts_service.sign_up(
        email=data.email,
        password=data.password.get_secret_value(),
        strategy=authenticate_strategy,
    )
    tasks.add_task(lambda: logger.info(f"send email: <{res},>"))
    return res


@router.post(
    path=urls.URL_ACCOUNT_SIGN_IN,
    status_code=status.HTTP_200_OK,
)
async def account_sign_in(
    data: AccountSignInSchema,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
):
    res = await accounts_service.sign_in(
        email=data.email,
        password=data.password.get_secret_value(),
        strategy=authenticate_strategy,
    )

    return res


@router.post(
    path=urls.URL_ACCOUNT_SIGN_OUT,
    status_code=status.HTTP_200_OK,
)
async def account_sign_out(
    current_user: deps.DepCurrentUser,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
):
    if current_user is None:
        raise RedirectResponse(urls.URL_ACCOUNT_SIGN_IN)

    res = await accounts_service.sign_out(
        current_user=current_user,
        strategy=authenticate_strategy,
    )
    return res

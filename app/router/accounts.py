from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Form, status
from fastapi.background import BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from pydantic.types import SecretStr

from app import dependencies as deps
from app.domain.base.schemas import BaseSchema
from app.lib.jwt import JWTTokenSchema
from app.lib.security import AccountSignInForm
from app.router import urls

logger = getLogger(__name__)

router = APIRouter(tags=["accounts"])


@router.post(
    urls.URL_ACCOUNT_SIGN_UP,
    status_code=status.HTTP_201_CREATED,
)
async def account_sign_up(
    data: AccountSignInForm,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
    authorization_strategy: deps.DepAuthorizationDefaultStrategy,
    tasks: BackgroundTasks,
):
    res = await accounts_service.sign_up(
        email=data.email,
        password=data.password.get_secret_value(),
        authenticate_strategy=authenticate_strategy,
    )
    tasks.add_task(lambda: logger.info(f"smtp send: <{res},>"))
    return res


class ExtraOAuth2Pass(OAuth2PasswordRequestForm):
    def __init(self, email: Annotated[EmailStr, Form()], *args, **kwargs):
        self.email = email
        super().__init__(*args, **kwargs)


@router.post(
    path=urls.URL_ACCOUNT_SIGN_IN,
    status_code=status.HTTP_200_OK,
)
async def account_sign_in(
    data: AccountSignInForm,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
    authorization_strategy: deps.DepAuthorizationDefaultStrategy,
):
    user = await accounts_service.sign_in(
        email=data.email,
        password=data.password.get_secret_value(),
        authenticate_strategy=authenticate_strategy,
    )

    credentials = await authenticate_strategy.authenticate(user)

    return credentials


@router.post(
    path=urls.URL_ACCOUNT_SIGN_OUT,
    status_code=status.HTTP_200_OK,
)
async def account_sign_out(
    current_user: deps.DepCurrentUser,
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
    authorization_strategy: deps.DepAuthorizationDefaultStrategy,
):
    if current_user is None:
        raise RedirectResponse(urls.URL_ACCOUNT_SIGN_IN)

    res = await accounts_service.sign_out(
        current_user=current_user,
        authenticate_strategy=authenticate_strategy,
    )
    return res


@router.post(
    path=urls.URL_ACCOUNT_TOKEN_REFRESH,
    status_code=status.HTTP_200_OK,
)
async def account_refresh_token(
    accounts_service: deps.DepAccountService,
    authenticate_strategy: deps.DepAuthenticationDefaultStrategy,
    authorization_strategy: deps.DepAuthorizationDefaultStrategy,
):
    return None

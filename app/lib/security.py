from logging import getLogger
from typing import Annotated

from fastapi import Form
from fastapi.security import OAuth2PasswordBearer
from app.config.base import get_config
from app.urls import URL_ACCOUNT_SIGN_IN

config = get_config()
logger = getLogger(__name__)


class OAuth2SignInRequestForm:
    def __init__(
        self,
        *,
        grant_type: Annotated[str | None, Form(pattern="^password$")] = None,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[str | None, Form()] = None,
        client_secret: Annotated[str | None, Form()] = None,
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


oauth2_default_security = OAuth2PasswordBearer(
    tokenUrl=URL_ACCOUNT_SIGN_IN,
    scopes={"client": "", "admin": ""},
)

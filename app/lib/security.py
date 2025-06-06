from logging import getLogger
from pydoc import Doc
from typing import Annotated, Optional

from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import EmailStr, SecretStr
from app.config.base import get_config
from app.domain.base.schemas import BaseSchema
from app.exceptions import UnauthorizedError
from app.lib.jwt import verify_token

config = get_config()
logger = getLogger(__name__)


class AccountSignInForm(BaseSchema):
    email: EmailStr
    password: SecretStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "Vx2yj@example.com",
                "password": "secret",
            },
        }


class JWTAuthorizationCredentialsSchema(BaseSchema):
    scheme: Annotated[str, Doc()]
    access_token: Annotated[str, Doc()]
    refresh_token: Annotated[str | None, Doc()]
    revoke_token: Annotated[str | None, Doc()]


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[JWTAuthorizationCredentialsSchema]:
        authorization = request.headers.get("Authorization")
        scheme, access_token = get_authorization_scheme_param(authorization)
        _ = verify_token(access_token)
        if not (authorization and scheme and access_token):
            if self.auto_error:
                raise UnauthorizedError()
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedError(detail="Invalid authentication credentials")
            else:
                return None

        refresh_token = request.cookies.get("refresh_token", None)
        revoke_token = request.cookies.get("revoke_token", None)
        return JWTAuthorizationCredentialsSchema(
            scheme=scheme,
            access_token=access_token,
            refresh_token=refresh_token,
            revoke_token=revoke_token,
        )

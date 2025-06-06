from logging import getLogger
from typing import Annotated

from fastapi import Form, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import EmailStr, SecretStr
from starlette import status
from app.config.base import get_config
from app.domain.base.schemas import BaseSchema
from app.exceptions import BaseAppError
from app.lib.jwt import JWTTokenPayloadSchema, JWTTokenSchema, create_jwt_token, verify_token

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

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, credentials: HTTPAuthorizationCredentials) -> JWTTokenSchema:
        return verify_token(credentials.credentials)

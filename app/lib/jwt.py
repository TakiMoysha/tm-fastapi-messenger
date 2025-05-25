from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID

from fastapi import Cookie, Depends
from fastapi.security import HTTPBearer
from starlette import status
from app.domain.base.schemas import BaseSchema
from app.exceptions import BaseAppError

token_security = HTTPBearer(auto_error=False)

# =========================================================


# =========================================================
class JWTAuthenticateTokenSchema(BaseSchema):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class JWTAuthenticateTokenPayloadSchema(BaseSchema):
    sub: str
    aud: str
    exp: datetime
    jti: UUID


# =========================================================


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenRequired:
    def __init__(self, token_type: TokenType):
        self._token_type = token_type

    def __call__(
        self,
        credentials=Depends(token_security),
        access_token: str | None = Cookie(None),
        refresh_token: str | None = Cookie(None),
    ):
        if credentials:
            return credentials.credentials

        if access_token and self._token_type == TokenType.ACCESS:
            return access_token

        if refresh_token and self._token_type == TokenType.REFRESH:
            return refresh_token

        raise BaseAppError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


access_token_required = TokenRequired(TokenType.ACCESS)
refresh_token_required = TokenRequired(TokenType.REFRESH)

from datetime import UTC, datetime, timedelta
from logging import getLogger
from typing import Literal, Self
from uuid import UUID

import jwt
from pydantic import field_serializer
from app.config.base import get_config
from app.config.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from app.domain.base.schemas import BaseSchema
from app.exceptions import PermissionDeniedError

config = get_config()
logger = getLogger(__name__)


class JWTTokenSchema(BaseSchema):
    access_token: str
    refresh_token: str
    revoke_token: str | None
    type_token: Literal["bearer"] = "bearer"


class JWTTokenPayloadSchema(BaseSchema):
    jti: UUID  # user_id
    exp: datetime  # expiration time
    sub: str | None = None  # email - sensitive info
    iss: str | None = None  # issuer
    aud: str | None = None  # audience
    nbf: datetime | None = None  # not before
    iat: datetime | None = None  # issued at

    @field_serializer("exp")
    def serialize_exp(self, value: datetime) -> int:
        return int(value.timestamp())

    @classmethod
    def from_dict(
        cls,
        jti: UUID,
        sub: str | None = None,
        exp: datetime | None = None,
        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    ) -> Self:
        if exp is not None:
            expire_time = exp
        else:
            expire_time = datetime.now(UTC) + expires_delta

        return cls(sub=sub, exp=expire_time, jti=jti)


def create_jwt_token(
    payload: JWTTokenPayloadSchema,
    *,
    secret: str = config.server.secret_key,
    algorithm: str = config.server.token_algorithm,
):
    return jwt.encode(
        payload.model_dump(mode="json", exclude_unset=True, exclude_none=True),
        secret,
        algorithm=algorithm,
    )


def verify_token(
    token: str,
    *,
    secret: str = config.server.secret_key,
    algorithm: str = config.server.token_algorithm,
):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError as err:
        raise PermissionDeniedError(detail="Token expired") from err
    except jwt.InvalidTokenError as err:
        raise PermissionDeniedError(detail="Invalid token") from err

    logger.debug(f"{payload=}")
    return JWTTokenPayloadSchema.model_validate(payload)

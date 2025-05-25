from datetime import UTC, datetime, timedelta
from logging import getLogger

import jwt
from fastapi import Request, Response

from app.config import get_config
from app.config.consts import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.models.user import UserModel
from app.domain.accounts.schemas import TokenData
from app.domain.protocols import IAuthenticationStrategy
from app.exceptions import PermissionDeniedError
from app.lib.cache import ICache
from app.lib.jwt import JWTAuthenticateTokenSchema

logger = getLogger(__name__)
config = get_config()


def create_jwt_token(
    data: dict,
    *,
    secret: str = config.server.secret_key,
    algorithm: str = config.server.token_algorithm,
    expires_delta: timedelta = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES),
):
    expire = datetime.now(UTC) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)


def verify_token(
    token: str,
    *,
    secret: str = config.server.secret_key,
    algorithm: str = config.server.token_algorithm,
):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise PermissionDeniedError(detail="Token expired")
    except jwt.InvalidTokenError:
        raise PermissionDeniedError(detail="Invalid token")

    logger.warning(f"{payload=}")
    user_data = TokenData(**payload)
    return user_data


class JWTAuthenticationStrategy(IAuthenticationStrategy):
    def __init__(
        self,
        response: Response,
        storage: ICache,
        secret: str = config.server.secret_key,
    ) -> None:
        self._secret = secret
        self._algorithm = config.server.token_algorithm
        self._response = response
        self._user_agent = response.headers.get("User-Agent")
        self._user_ip = response.headers.get("X-Forwarded-For")
        self._fingerprint = ";".join([str(hash(self._user_ip)), str(hash(self._user_ip))])
        self._storage = storage

    async def authenticate(self, user: UserModel) -> JWTAuthenticateTokenSchema:
        access_token = create_jwt_token(data={"sub": user.email})
        refresh_token = create_jwt_token(data={"sub": user.email})
        self._response.set_cookie("access_token", access_token, httponly=True)
        self._response.set_cookie("refresh_token", refresh_token, httponly=True)

        # self._storage.set(f"{user.email}", access_token) # !TODO:[multiaccounts]

        return JWTAuthenticateTokenSchema(access_token=access_token, token_type="bearer")

    # ================================================= TODO: update processing
    async def sign_up(self, user: UserModel):
        raise NotImplementedError(f"sign_up is not supported in <{repr(self)}>")

    async def sign_out(self, user: UserModel):
        self._storage.delete(f"{user.email}")

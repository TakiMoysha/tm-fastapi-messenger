from datetime import UTC, datetime, timedelta
from logging import getLogger

from fastapi import Request, Response

from app.config import get_config
from app.database.models.user import UserModel
from app.domain.protocols import IAuthenticationStrategy
from app.lib.cache import ICache
from app.lib.jwt import JWTTokenPayloadSchema, create_jwt_token

logger = getLogger(__name__)
config = get_config()


class JWTAuthenticationStrategy(IAuthenticationStrategy):
    def __init__(
        self,
        request: Request,
        response: Response,
        storage: ICache,
        secret: str = config.server.secret_key,
    ) -> None:
        self._storage = storage
        self._secret = secret
        self._algorithm = config.server.token_algorithm
        self._request = request
        self._response = response
        self._fingerprint = ";".join(
            [
                str(hash(request.headers.get("User-Agent"))),
                str(hash(request.headers.get("X-Forwarded-For"))),
            ]
        )

    async def authenticate(self, user: UserModel) -> dict[str, str]:
        payload = JWTTokenPayloadSchema.from_dict(
            sub=user.email,
            jti=user.id,
        )
        access_token = create_jwt_token(payload=payload)

        payload.exp = datetime.now(UTC) + timedelta(days=30)
        refresh_token = create_jwt_token(payload=payload)
        self._response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=True,
            expires=payload.exp,
        )

        self._response.set_cookie(
            "fingerprint",
            self._fingerprint,
            httponly=True,
            secure=True,
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    # ================================================= TODO: update processing
    async def sign_up(self, user: UserModel):
        raise NotImplementedError(f"sign_up is not supported in <{repr(self)}>")

    async def sign_out(self, user: UserModel):
        """deleted refresh token from db and cache"""
        self._storage.delete(f"{user.email}")

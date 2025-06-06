from typing import Annotated

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from fastapi import Depends, Request, Response, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.base import get_config
from app.database.models.user import UserModel
from app.domain.accounts.services import AccountService
from app.domain.protocols import IAuthenticationStrategy, IPasswordHasher
from app.exceptions import PermissionDeniedError
from app.lib.password_hasher import Argon2PasswordHasher
from app.lib.security import JWTBearer
from app.lib.strategies import JWTAuthenticationStrategy
from app.server.plugins import alchemy

config = get_config()

# =====================================================================================================


def provide_password_hasher() -> IPasswordHasher:
    _algo = config.server.password_algorithm.lower()
    if _algo != "argon2":
        raise NotImplementedError(
            f"Algorithm {config.server.password_algorithm} is not supported, u can use: ['argon2']"
        )
    return Argon2PasswordHasher(salt=config.server.secret_key, algorithm=_algo)


DepPasswordHasher = Annotated[IPasswordHasher, Depends(provide_password_hasher)]


# =====================================================================================================


DepAuthenticateToken = Annotated[str, Depends(JWTBearer())]


# def get_current_active_user(fake_db):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(Depends(oauth2_scheme), SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_user(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
#     # Replace username with email in your authentication logic
#     user = await retrieve_user_by_email(form_data.username)
#     if not user or not verify_password(user.hashed_password, form_data.password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")j
#     return user


async def get_current_user(token: str = Depends(JWTBearer())) -> UserModel | None:
    if token != "1":
        raise PermissionDeniedError

    return None


DepCurrentUser = Annotated[UserModel | None, Depends(get_current_user)]


# =====================================================================================================


def provide_alchemy(request: Request) -> AdvancedAlchemy:
    if request.app.state.alchemy is None:
        raise RuntimeError("Alchemy is not initialized")

    return request.app.state.alchemy


DepAlchemy = Annotated[AdvancedAlchemy, Depends(provide_alchemy)]


def provide_async_session(alchemy: DepAlchemy, request: Request) -> AsyncSession:
    return alchemy.get_async_session(request)


DepAlchemySession = Annotated[AsyncSession, Depends(provide_async_session)]

# =====================================================================================================

DepAccountService = Annotated[
    AccountService,
    Depends(alchemy.provide_service(AccountService)),
]


def provide_jwt_authentication_strategy(
    request: Request,
    response: Response,
) -> JWTAuthenticationStrategy:
    return JWTAuthenticationStrategy(request=request, response=response)


DepAuthenticationDefaultStrategy = Annotated[
    IAuthenticationStrategy,
    Depends(provide_jwt_authentication_strategy),
]


def provide_authorization_strategy(request: Request, response: Response) -> None:
    pass


DepAuthorizationDefaultStrategy = Annotated[None, Depends(provide_authorization_strategy)]

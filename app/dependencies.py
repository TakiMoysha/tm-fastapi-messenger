from typing import Annotated

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession


from app.exceptions import PermissionDeniedException
from app.lib.cache import ICache
from app.server.plugins import alchemy, oauth2_schema
from app.domain.accounts.services import AccountService

# =====================================================================================================


# =====================================================================================================


async def get_protect_current_user(token: str = Depends(oauth2_schema)):
    if token != "demo-token":
        raise PermissionDeniedException

    return {"user": None, "token": token}


DepAuthToken = Annotated[OAuth2PasswordBearer, Depends(oauth2_schema)]
DepProtectUserAccess = Annotated[str, Depends(get_protect_current_user)]

# =====================================================================================================


def provide_state_cache(request: Request) -> ICache:
    if request.app.state.cache is None:
        raise RuntimeError("Cache is not initialized")

    return request.app.state.cache


DepStateCache = Annotated[ICache, Depends(provide_state_cache)]


def provide_alchemy(request: Request) -> AdvancedAlchemy:
    if request.app.state.alchemy is None:
        raise RuntimeError("Alchemy is not initialized")

    return request.app.state.alchemy


DepAlchemy = Annotated[AdvancedAlchemy, Depends(provide_alchemy)]


def provide_async_session(alchemy: DepAlchemy, request: Request) -> AsyncSession:
    return alchemy.get_async_session(request)


DepAlchemySession = Annotated[AsyncSession, Depends(provide_async_session)]

# =====================================================================================================

# from typing import AsyncGenerator

# from app.domain.accounts.services import AccountService


# async def provide_accounts_service(db_session: DepsAlchemySession) -> AsyncGenerator[AccountService, None]:
#     async with AccountService.new(session=db_session) as service:
#         yield service


DepAccountService = Annotated[AccountService, Depends(alchemy.provide_service(AccountService))]

# DatabaseSession = Annotated[AsyncSession, Depends(get_alchemy().get_async_session())]

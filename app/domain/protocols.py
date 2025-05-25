from typing import Any, Protocol, runtime_checkable

from advanced_alchemy.base import ModelProtocol


@runtime_checkable
class IPasswordHasher(Protocol):
    def __init__(self, *args, **kwargs) -> None: ...
    def verify(self, password: str, hashed_password: str) -> bool: ...
    def hash(self, password: str) -> str: ...


type TAuthResult = dict[str, Any]


@runtime_checkable
class IAuthenticationStrategy(Protocol):
    def __init__(self, *args, **kwargs) -> None: ...
    async def authenticate(self, user: ModelProtocol, *args, **kwargs) -> TAuthResult: ...

    # ============================================================================== TODO:
    async def sign_up(self, user: ModelProtocol, *args, **kwargs) -> TAuthResult:
        """Called with the user's successive registration"""
        ...

    async def sign_out(self, user: ModelProtocol, *args, **kwargs) -> TAuthResult:
        """Called when the user signs out"""
        ...

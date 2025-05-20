from logging import getLogger
from typing import Protocol

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from starlette import status

from app.database.models.user import UserModel
from app.domain.protocols import IPasswordHasher
from app.exceptions import PermissionDeniedException

EXC_PREVENT_LOGIN = "User not found or credentials are wrong"

logger = getLogger(__name__)

__all__ = ("AccountService",)


class ISignUpServiceOptions(Protocol):
    algorithm: str
    secret_key: str


class AccountService(SQLAlchemyAsyncRepositoryService[UserModel]):
    class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
        model_type = UserModel

    repository_type = UserRepository
    match_fields = ["id", "email"]

    async def check_email(self, email: str) -> bool:
        logger.info(f"check_email: <{email}>")
        return await self.repository.exists(email=email)

    async def sign_in(self, email: str, password: str, *, hasher: IPasswordHasher) -> UserModel:
        logger.debug(f"sign_in: <{email}, {password}>")
        logger.info(f"sign_in: <{email}>")
        obj = await self.get_one_or_none(email=email)

        if obj is None:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        if obj.hashed_password is None:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)

        if not hasher.verify(password, obj.hashed_password):
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)

        return obj

    async def sign_up(self, email: str, password: str, *, hasher: IPasswordHasher) -> UserModel:
        logger.debug(f"sign_up: <{email}, {password}>")
        logger.info(f"sign_up: <{email}>")
        obj = await self.get_one_or_none(email=email)

        if obj is not None:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)

        user_data = {"email": email, "hashed_password": hasher.hash(password)}
        logger.debug(f"new_user: <{user_data}>")
        obj = await self.create(user_data)
        return obj

    async def is_superuser(self, user: UserModel) -> bool:
        logger.info(f"is_superuser: <{user}>")
        is_have_superuser_role = any([False])
        return bool(user.is_superuser or is_have_superuser_role)

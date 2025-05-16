from logging import getLogger

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from fastapi import status

from app.database.models.user import UserModel
from app.exceptions import PermissionDeniedException, WorkInProgressException

EXC_PREVENT_LOGIN = "User not found or credentials are wrong"
EXC_INACTIVE_ACCOUNT = "User account is inactive"

logger = getLogger(__name__)

__all__ = ("AccountService",)


class AccountService(SQLAlchemyAsyncRepositoryService[UserModel]):
    class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
        model_type = UserModel

    repository_type = UserRepository
    match_fields = ["email"]

    async def check_email(self, email: str) -> bool:
        logger.info(f"check_email: <{email}>")
        return await self.repository.exists(email=email)

    async def registration(self, email: str, password: str) -> UserModel:
        logger.debug(f"registration: <{email}, {password}>")
        logger.info(f"registration: <{email}>")
        obj = await self.get_one_or_none(email=email)
        password_conditions = {}

        raise WorkInProgressException

    async def authenticate(self, email: str, password: str) -> UserModel:
        logger.info(f"authenticate: <{email}>")
        obj = await self.get_one_or_none(email=email)

        if obj is None:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        if obj.hashed_password is None:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        # if not await crypt(password, obj.hashed_password):  # TODO:
        # raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        if not obj.is_active:
            raise PermissionDeniedException(status.HTTP_403_FORBIDDEN, EXC_INACTIVE_ACCOUNT)

        return obj

    async def is_superuser(self, user: UserModel) -> bool:
        logger.info(f"is_superuser: <{user}>")
        is_have_superuser_role = any(
            assigned_role.role.name
            for assigned_role in user.roles
            # if assigned_role.role.name == SUPERUSER_ROLE_NAME  # fmt: ignore
        )
        return bool(user.is_superuser or is_have_superuser_role)

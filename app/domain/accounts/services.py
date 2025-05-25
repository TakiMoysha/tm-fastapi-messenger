from logging import getLogger

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from starlette import status

from app.database.models.user import UserModel
from app.domain.protocols import IAuthenticationStrategy, IPasswordHasher
from app.exceptions import PermissionDeniedError
from app.lib.password_hasher import Argon2PasswordHasher

EXC_PREVENT_LOGIN = "User not found or credentials are wrong"
EXC_USER_ALREADY_EXISTS = "User already exists"

logger = getLogger(__name__)

__all__ = ("AccountService",)


class AccountService(SQLAlchemyAsyncRepositoryService[UserModel]):
    class UserRepository(SQLAlchemyAsyncRepository[UserModel]):
        model_type = UserModel

    repository_type = UserRepository
    match_fields = ["id", "email"]
    # ==============================================
    hasher: IPasswordHasher = Argon2PasswordHasher()
    # ==============================================

    async def sign_in(
        self,
        email: str,
        password: str,
        *,
        auth_strategy: IAuthenticationStrategy,
    ) -> dict:
        """"""
        logger.info(f"sign_in: <{email}>")
        obj = await self.get_one_or_none(email=email)

        if obj is None:
            raise PermissionDeniedError(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        if obj.hashed_password is None:
            raise PermissionDeniedError(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)
        if not self.hasher.verify(password, obj.hashed_password):
            raise PermissionDeniedError(status.HTTP_403_FORBIDDEN, EXC_PREVENT_LOGIN)

        logger.info(f"sign_in authenticate: <{obj}>")
        auth_result = await auth_strategy.authenticate(user=obj)
        return { "user": obj, "authenticate": auth_result }

    async def sign_up(
        self,
        email: str,
        password: str,
        *,
        auth_strategy: IAuthenticationStrategy,
    ) -> UserModel:
        """Create new account for user."""
        obj = await self.get_one_or_none(email=email)

        if obj is not None:
            raise PermissionDeniedError(status.HTTP_403_FORBIDDEN, EXC_USER_ALREADY_EXISTS)

        user_data = {"email": email, "hashed_password": self.hasher.hash(password)}
        logger.debug(f"new_user: <{user_data}>")
        obj = await self.create(user_data)
        logger.info(f"sing_up success: <{obj}>")
        return obj

    async def sign_out(
        self,
        current_user: UserModel,
        *,
        auth_strategy: IAuthenticationStrategy,
    ):
        """"""
        raise NotImplementedError

    async def is_superuser(self, user: UserModel) -> bool:
        logger.info(f"is_superuser: <{user}>")
        is_have_superuser_role = any([False])
        return bool(user.is_superuser or is_have_superuser_role)

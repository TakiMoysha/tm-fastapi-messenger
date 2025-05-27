from logging import getLogger
from app.domain.protocols import IPasswordHasher

from typing import Literal
from passlib.context import CryptContext


logger = getLogger(__name__)


class Argon2PasswordHasher(IPasswordHasher):
    def __init__(self, salt: str | None = None, algorithm: Literal["argon2"] = "argon2", *args, **kwargs) -> None:
        logger.info(f"Argon2PasswordHasher: <{salt}, {algorithm}>")
        self._salt = salt if salt is not None else ""

        if algorithm.lower() != "argon2":
            raise NotImplementedError("Only 'argon2' is supported")
        self._algorithm = algorithm.lower()

        self._context = CryptContext(schemes=[self._algorithm])

    def hash(self, password: str) -> str:
        return self._context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._context.verify(password, hashed_password)

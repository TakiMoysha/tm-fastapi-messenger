from logging import getLogger
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from advanced_alchemy.base import orm_registry
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.asgi import create_asgi
from app.config.base import AppConfig
from app.database.models.chat import ChatModel
from app.database.models.user import UserModel
from app.domain.accounts.services import AccountService
from app.domain.chats.services import ChatService
from app.lib.password_hasher import Argon2PasswordHasher

logger = getLogger(__name__)


@pytest.fixture(name="client", scope="class")
def fx_app() -> Generator[TestClient, None, None]:
    with TestClient(create_asgi()) as client:
        yield client

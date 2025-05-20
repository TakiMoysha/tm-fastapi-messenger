from logging import getLogger
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from advanced_alchemy.base import orm_registry
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.asgi import create_asgi
from app.config.base import AppConfig
from app.database.models.chat import ChatModel
from app.database.models.user import UserModel
from app.domain.accounts.services import AccountService
from app.domain.chats.services import ChatService
from app.lib.password_hasher import Argon2PasswordHasher

logger = getLogger(__name__)


@pytest.fixture(name="engine", scope="package")
def fx_engine(config: AppConfig) -> AsyncEngine:
    return config.database.get_engine()


@pytest.fixture(name="sessionmaker", scope="package")
def fx_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(name="session", scope="function")
async def fx_session(sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as s:
        yield s


@pytest_asyncio.fixture(autouse=True, scope="package")
async def _seed_db(
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    raw_users: list[dict],
    raw_chats: list[dict],
    raw_groups: list[dict],
) -> AsyncGenerator[None, None]:
    metadata = orm_registry.metadata
    logger.info(metadata)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    async with sessionmaker() as s, AccountService.new(s, load=[UserModel.chats, UserModel.groups]) as service:
        hasher = Argon2PasswordHasher()
        for user in raw_users:
            if user.get("_password"):
                user["hashed_password"] = hasher.hash(user["_password"])
                del user["_password"]

        _ = await service.create_many(raw_users, auto_commit=True)

    async with sessionmaker() as s, ChatService.new(s, load=[ChatModel.group, ChatModel.creator]) as service:
        _ = await service.create_many(raw_chats, auto_commit=True)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

    await engine.dispose()


@pytest.fixture(name="client")
def fx_client() -> Generator[TestClient, None, None]:
    with TestClient(create_asgi()) as client:
        yield client

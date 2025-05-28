from logging import getLogger

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import UserModel
from app.domain.accounts.services import AccountService
from app.lib.password_hasher import Argon2PasswordHasher
from app.urls import URL_HEALTH

_hasher = Argon2PasswordHasher()
_faker = Faker()
logger = getLogger(__name__)

pytestmark = pytest.mark.asyncio


async def test_health(client: TestClient) -> None:
    response = client.get(URL_HEALTH)
    assert response.status_code == 200

    expected = {"status": "ok", "detail": {"database": "ok"}}
    assert response.json() == expected


@pytest.mark.parametrize(
    ("email, password"),
    [
        (_faker.email(), _faker.password()),
        (_faker.email(), _faker.password()),
        (_faker.email(), _faker.password()),
    ],
)
async def test_account_service(session: AsyncSession, email: str, password: str):
    as_ = AccountService(session)
    hasher = Argon2PasswordHasher()
    hashed_pass = hasher.hash(password)
    logger.debug(f"{email=}:{password=}:{hashed_pass=}")

    user = UserModel(email=email, hashed_password=hashed_pass)
    logger.debug(f"MODEL: {user.id=}, {user.email=}, {user.hashed_password=}")

    res = await as_.create(user)
    logger.debug(f"SERVICE: {res.id=}, {res.email=}, {res.hashed_password=}")

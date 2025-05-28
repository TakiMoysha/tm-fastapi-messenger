from logging import getLogger

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from starlette import status

from app.database.models.user import UserModel
from app.urls import URL_ACCOUNT_SIGN_IN, URL_ACCOUNT_SIGN_UP
from tests.user_fixtures import TTestUser

_faker = Faker()

logger = getLogger(__name__)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("credentials"),
    [{"email": _faker.email(), "password": _faker.password()} for _ in range(3)],
)
class TestAuth:
    async def test_should_create_user_account_by_sing_up(self, credentials: dict, client: TestClient, faker: Faker):
        r = client.post(URL_ACCOUNT_SIGN_UP, json=credentials)
        logger.debug(r.headers)
        assert r.status_code == status.HTTP_201_CREATED, r.json()

    async def test_should_authenticate_user_by_sing_in(self, credentials: dict, client: TestClient, faker: Faker):
        r = client.post(URL_ACCOUNT_SIGN_IN, json=credentials)
        logger.debug(r.headers)
        assert r.status_code == status.HTTP_200_OK, r.json()

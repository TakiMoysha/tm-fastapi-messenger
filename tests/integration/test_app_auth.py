import pytest

from faker import Faker
from logging import getLogger

from fastapi.testclient import TestClient
from starlette import status

from app.urls import URL_ACCOUNT_SIGN_UP, URL_ACCOUNT_SIGN_IN

_faker = Faker()

logger = getLogger(__name__)

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("user_credentials"),
    [{"email": _faker.email(), "password": _faker.password()} for _ in range(3)],
)
class TestAuth:
    async def test_account_sign_up(self, client: TestClient, faker: Faker, user_credentials: dict):
        r = client.post(URL_ACCOUNT_SIGN_UP, json=user_credentials)
        assert r.status_code == status.HTTP_201_CREATED, r.json()

    async def test_account_sign_in(self, client: TestClient, faker: Faker, user_credentials: dict):
        r = client.post(URL_ACCOUNT_SIGN_IN, json=user_credentials)
        logger.info(r.headers)
        assert r.status_code == status.HTTP_200_OK, r.json()

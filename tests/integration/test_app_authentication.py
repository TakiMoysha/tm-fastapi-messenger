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


async def test_should_return_valid_tokens_on_sign_in(
    client: TestClient,
    auth_user: TTestUser,
):
    if isinstance(auth_user, UserModel):
        raise NotImplementedError
    else:
        credentials = {
            "email": auth_user.get("email"),
            "password": auth_user.get("_password"),
        }

    r = client.post(URL_ACCOUNT_SIGN_IN, json=credentials)
    assert r.status_code == status.HTTP_200_OK, r.json()


# @pytest.mark.parametrize(
#     ("user_credentials"),
#     [{"email": _faker.email(), "password": _faker.password()} for _ in range(3)],
# )
# class TestAuth:
#     async def test_account_sign_up(self, client: TestClient, faker: Faker, user_credentials: dict):
#         r = client.post(URL_ACCOUNT_SIGN_UP, json=user_credentials)
#         assert r.status_code == status.HTTP_201_CREATED, r.json()
#
#     async def test_account_sign_in(self, client: TestClient, faker: Faker, user_credentials: dict):
#         r = client.post(URL_ACCOUNT_SIGN_IN, json=user_credentials)
#         logger.info(r.headers)
#         assert r.status_code == status.HTTP_200_OK, r.json()

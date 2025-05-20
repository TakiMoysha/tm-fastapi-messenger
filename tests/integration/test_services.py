from faker import Faker
import pytest
from logging import getLogger


from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.asgi import create_asgi
from app.database.models.user import UserModel
from app.domain.accounts.services import AccountService
from app.domain.consts import URL_ACCOUNT_SIGN_UP, URL_HEALTH

logger = getLogger(__name__)


def test_health(client: TestClient) -> None:
    response = client.get(URL_HEALTH)
    assert response.status_code == 200

    expected = {"status": "ok", "detail": {"database": "ok"}}
    assert response.json() == expected


# @pytest.mark.asyncio
# async def test_account_sign_up(client: TestClient, faker: Faker):
#     with TestClient(create_asgi()) as client:
#         user_credentials = {"email": faker.email(), "password": faker.password()}
#         r = client.post(URL_ACCOUNT_SIGN_UP, json=user_credentials)
#         assert r.status_code == 201


@pytest.mark.asyncio
async def test_account_service(session: AsyncSession):
    _as: AccountService = AccountService(session)
    user = UserModel(email="email", hashed_password="hashed_password")
    logger.warning(f"{user.id}, {user.email}, {user.hashed_password}")

    # async with session.begin():
    #     res = await session.execute(
    #         text("""
    #         SELECT (user_accounts.email, user_accounts.hashed_password, user_accounts.is_superuser,
    #                 user_accounts.id, user_accounts.sa_orm_sentinel, user_accounts.created_at, user_accounts.updated_at,
    #                 chats_1.title, chats_1.kind, chats_1.creator_id, chats_1.id AS id_1,
    #                 chats_1.created_at AS created_at_1, chats_1.updated_at AS updated_at_1 
    #         FROM user_accounts JOIN chats AS chats_1 ON user_accounts.id = chats_1.creator_id 
    #         WHERE user_accounts.id = ?
    #     """)
    #     )
    #     logger.info(res.all())

    await _as.create({"email": "email", "hashed_password": "hashed_password"})
    await session.commit()

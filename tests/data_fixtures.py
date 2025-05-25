import pytest
from faker import Faker

from app.database.models.chat_group import ChatGroupModel

from app.database.models import (
    UserModel,
    ChatModel,
)


pytestmark = pytest.mark.asyncio

type TUser = UserModel | dict


@pytest.fixture(name="auth_user", scope="package")
def fx_auth_user(faker: Faker) -> TUser:
    return {
        "id": faker.uuid4(),
        "email": faker.email(),
        "_password": faker.password(),
        "hashed_password": None,
        "is_superuser": False,
        "created_at": faker.date_time().astimezone(),
        "updated_at": faker.date_time().astimezone(),
    }


@pytest.fixture(name="auth_superuser", scope="package")
def fx_auth_superuser(faker: Faker) -> TUser:
    return {
        "id": faker.uuid4(),
        "email": faker.email(),
        "_password": faker.password(),
        "hashed_password": None,
        "is_superuser": True,
        "created_at": faker.date_time().astimezone(),
        "updated_at": faker.date_time().astimezone(),
    }


@pytest.fixture(name="raw_users", scope="package")
def fx_raw_users(faker: Faker, auth_user: UserModel, auth_superuser: UserModel) -> list[TUser]:
    return [
        auth_user,
        auth_superuser,
        {
            "id": "ddae0eb3-81ab-4fed-aa08-4fc98554d399",
            "email": "lisamoses@example.net",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
        {
            "id": "592c3b6e-3879-4de7-9481-f953e6ca8a08",
            "email": "antonio30@example.net",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
        {
            "id": "ac1f5e38-7301-4a3c-beef-f7cba29560d7",
            "email": "adamsandrew@example.org",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
    ]


@pytest.fixture(name="raw_chats", scope="package")
def fx_raw_chats(faker: Faker, auth_user: TUser, auth_superuser: TUser) -> list[ChatModel | dict]:
    return [
        # {
        #     "id": faker.uuid4(),
        #     "creator_id": auth_user["id"] if isinstance(auth_user, dict) else getattr(auth_user, "id"),
        #     "group_id": faker.uuid4(),
        #     "created_at": faker.date_time().astimezone(),
        #     "updated_at": faker.date_time().astimezone(),
        # }
    ]


@pytest.fixture(name="raw_groups", scope="package")
def fx_raw_groups(faker: Faker, auth_user: TUser, auth_superuser: TUser) -> list[ChatGroupModel | dict]:
    return []

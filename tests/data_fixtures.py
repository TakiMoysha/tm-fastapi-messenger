import pytest
from faker import Faker

from app.database.models.chat_group import ChatGroupModel

from app.database.models import (
    UserModel,
    ChatModel,
)


pytestmark = pytest.mark.asyncio


@pytest.fixture(name="raw_users", scope="package")
def fx_raw_users(faker: Faker) -> list[UserModel | dict]:
    return [
        {
            "id": "5f950b68-204e-4dc8-bc1d-3d29d90f7050",
            "email": "samuelgarcia@example.org",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
        {
            "id": "5f2635b4-6890-43de-ad9e-46d52ea9237a",
            "email": "jonedwards@example.org",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
        {
            "id": "c50f8da6-3197-41d4-8283-bb49fc1a05ef",
            "email": "hayeschristina@example.net",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
        {
            "id": "cc904e60-a40f-4594-aee6-01aee5bb26e3",
            "email": "patrickwest@example.com",
            "_password": "test_1",
            "hashed_password": None,
            "is_superuser": False,
            "created_at": faker.date_time().astimezone(),
            "updated_at": faker.date_time().astimezone(),
        },
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


# dump data
@pytest.fixture(name="raw_chats", scope="package")
def fx_raw_chats(faker: Faker) -> list[ChatModel | dict]:
    return [
        # {
        #     "title": "test chat 1",
        #     "creator_id": "ac1f5e38-7301-4a3c-beef-f7cba29560d7",
        # }
    ]


@pytest.fixture(name="raw_groups", scope="package")
def fx_raw_groups(faker: Faker) -> list[ChatGroupModel | dict]:
    return []

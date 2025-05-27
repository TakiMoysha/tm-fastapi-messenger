from datetime import UTC, datetime, timedelta
from logging import getLogger

import pytest
from faker import Faker

from app.config import get_config
from app.lib.jwt import JWTTokenPayloadSchema, create_jwt_token, verify_token

logger = getLogger(__name__)
config = get_config()
pytestmark = pytest.mark.asyncio
faker = Faker()


@pytest.mark.parametrize(
    "raw_payload",
    [
        {
            "sub": faker.email(),
            "jti": faker.uuid4(),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        {
            "sub": faker.email(),
            "jti": faker.uuid4(),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        {
            "sub": faker.email(),
            "jti": faker.uuid4(),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
    ],
)
async def test_should_return_valid_tokens(raw_payload: dict):
    payload = JWTTokenPayloadSchema.from_dict(**raw_payload)
    token = create_jwt_token(payload)
    _ = verify_token(token)

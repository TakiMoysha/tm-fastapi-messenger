import pytest

from fastapi.testclient import TestClient

from app.asgi import create_asgi
from app.lib.strategies import JWTAuthenticationStrategy


pytestmark = pytest.mark.asyncio


async def test_jwt_authentication_strategy_sign_in():
    pass

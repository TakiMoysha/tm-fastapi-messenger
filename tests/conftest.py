import pytest

from fastapi.testclient import TestClient

from app.asgi import create_asgi


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow to run",
    )


@pytest.fixture(scope="module")
async def client():
    async with TestClient(create_asgi()) as client:
        yield client

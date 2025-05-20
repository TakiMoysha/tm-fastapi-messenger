import pytest
from faker import Faker

from app.config.base import get_config

pytest_plugins = ("tests.data_fixtures",)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow to run",
    )
    config.addinivalue_line(
        "markers",
        "require_local_db: mark test requires local database",
    )


@pytest.fixture(name="faker", scope="session")
def fx_faker():
    return Faker()


@pytest.fixture(name="config", scope="package")
def fx_config():
    config = get_config()
    if not config.server.testing:
        pytest.skip("TESTING env is not enabled")

    return config

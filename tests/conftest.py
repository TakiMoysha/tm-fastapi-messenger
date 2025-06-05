import logging
import os
from os import getenv

import pytest
from faker import Faker

from app.config.base import get_config

pytest_plugins = ("tests.user_fixtures", "tests.hypothesis_fixtures")
logger = logging.getLogger(__name__)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow to run",
    )
    config.addinivalue_line(
        "markers",
        "tdd: test for development",
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

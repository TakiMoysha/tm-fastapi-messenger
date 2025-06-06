from logging import Logger, getLogger

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from advanced_alchemy.types.file_object import storages
from fastapi import FastAPI

from app.config.base import get_config
from app.config.plugins import SQLALCHEMY_CONFIG
from app.lib.cache import CacheBoxCache

config = get_config()
logger = getLogger(__name__)

# ================================================= ALCHEMY

alchemy = AdvancedAlchemy(config=SQLALCHEMY_CONFIG)


def setup_alchemy(app: FastAPI):
    logger.info("Plugin:AdvancedAlchemy")
    alchemy.init_app(app)
    app.state.alchemy = alchemy
    return alchemy


# ================================================= LOGGING


def setup_logging(app: FastAPI):
    import logging.config

    from app.config.plugins import LOGGING_CONFIG

    logger.info("Plugin:Logging")
    logging.config.dictConfig(LOGGING_CONFIG)


# =================================================


def setup_cache(app: FastAPI):
    logger.info("Plugin:Cache")
    app.state.cache = CacheBoxCache.default()
    return app.state.cache


# =================================================


def setup_file_storage(app: FastAPI):
    storages.register_backend(config.storage.get_default_storage())

    return None

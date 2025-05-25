from logging import Logger, getLogger

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from fastapi import FastAPI

from app.config.plugins import SQLALCHEMY_CONFIG

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
    from app.lib.cache import OnlyDevInMemoryCache

    logger.info("Plugin:Cache")
    app.state.cache = OnlyDevInMemoryCache()
    return app.state.cache

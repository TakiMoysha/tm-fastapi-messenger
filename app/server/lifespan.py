from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.config.base import get_config

from .plugins import alchemy
from .plugins import setup_cache

config = get_config()
logger = getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info(f"Lifespan:Server: <{str(config.server)}>")
    logger.info(f"Lifespan:Database: <{str(config.database)}>")
    app.state.alchemy = alchemy
    logger.info(f"Lifespan:Cache: <{str()}>")
    app.state.cache = setup_cache()
    logger.info("Lifespan:Done: <>")
    yield

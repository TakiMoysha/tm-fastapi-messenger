from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.config.base import get_config

config = get_config()
logger = getLogger(__name__)


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info(f"Lifespan:Server: <{str(config.server)}>")
    logger.info(f"Lifespan:DB:Config: <{str(config.database)}>")
    logger.info(f"Lifespan:DB:Instance: <{app.state.alchemy}>")
    logger.info(f"Lifespan:Cache:Config: <{str()}>")
    logger.info(f"Lifespan:Cache:Instance: <{app.state.cache}>")
    logger.info("Lifespan:Done: <>")
    yield

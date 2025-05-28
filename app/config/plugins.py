from advanced_alchemy.extensions.fastapi import AsyncSessionConfig, SQLAlchemyAsyncConfig

from app.lib.utils.logging import get_logger_config

from .base import get_config

config = get_config()


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s <%(name)s>: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # stderr
        },
    },
    "loggers": {
        "sqlalchemy.engine": get_logger_config(level=config.logging.sqlalchemy_level),
        "uvicorn.error": get_logger_config(level=config.logging.uvicorn_error_level),
        "uvicorn.access": get_logger_config(level=config.logging.uvicorn_access_level),
        "aiosqlite": get_logger_config(level=config.logging.not_interesting),
        "watchfiles.main": get_logger_config(level=config.logging.not_interesting),
        "": get_logger_config(level=config.logging.level),
    },
}

SQLALCHEMY_CONFIG = SQLAlchemyAsyncConfig(
    connection_string=config.database.url,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=config.database.dev,
    commit_mode="autocommit",
)

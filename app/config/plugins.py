from advanced_alchemy.extensions.fastapi import AsyncSessionConfig, SQLAlchemyAsyncConfig

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
        "sqlalchemy.engine": config.logging.get_logger_conf(level=config.logging.sqlalchemy_level),
        "uvicorn.error": config.logging.get_logger_conf(level=config.logging.uvicorn_error_level),
        "uvicorn.access": config.logging.get_logger_conf(level=config.logging.uvicorn_access_level),
        "aiosqlite": config.logging.get_logger_conf(level=config.logging.not_interesting),
        "": config.logging.get_logger_conf(level=config.logging.level),
    },
}

SQLALCHEMY_CONFIG = SQLAlchemyAsyncConfig(
    connection_string=config.database.url,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=config.database.dev,
    commit_mode="autocommit",
)

from os import getenv
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Final

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.exceptions import ConfigException
from app.lib.upcast_env import get_upcast_env

APP_HOME: Final[Path] = Path(get_upcast_env("APP_HOME", "app")).absolute()


@dataclass
class ServerConfig:
    debug: bool = field(default_factory=lambda: get_upcast_env("SERVER_DEBUG", False))
    testing: bool = field(default_factory=lambda: get_upcast_env("SERVER_TESTING", False))

    secret_key: str = field(default_factory=lambda: get_upcast_env("SERVER_SECRET_KEY", "_dont_expose_me_"), repr=False, hash=False)  # fmt: skip
    algorithm: str = field(default_factory=lambda: get_upcast_env("SERVER_ALGORITHM", "HS256"), repr=False, hash=False)  # fmt: skip
    access_token_expire_minutes: int = field(default_factory=lambda: get_upcast_env("SERVER_ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # fmt: skip
    ws_heartbeat_timeout: int = field(default_factory=lambda: get_upcast_env("SERVER_WS_HEARTBEAT_TIMEOUT", 10))  # fmt: skip

    cors_origins: list[str] = field(
        default_factory=lambda: get_upcast_env(  # type: ignore
            "SERVER_CORS_ORIGINS_BOOTSTRAP",
            ["*"],  # type: ignore
        ),
    )
    cors_methods: list[str] = field(
        default_factory=lambda: get_upcast_env(  # type: ignore
            "SERVER_CORS_METHODS_BOOTSTRAP",
            ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # type: ignore
        ),
    )
    cors_headers: list[str] = field(
        default_factory=lambda: get_upcast_env(  # type: ignore
            "SERVER_CORS_HEADERS_BOOTSTRAP",
            ["*"],  # type: ignore
        ),
    )


@dataclass
class DatabaseConfig:
    dev: bool = field(default_factory=lambda: get_upcast_env("DB_DEV", False))

    driver: str = field(default_factory=lambda: get_upcast_env("DB_DRIVER", "postgresql+asyncpg"))
    host: str = field(default_factory=lambda: get_upcast_env("DB_HOST", "localhost"))
    port: int = field(default_factory=lambda: get_upcast_env("DB_PORT", 5432))
    database: str = field(default_factory=lambda: get_upcast_env("DB_NAME", "fastapimessenger"))
    user: str = field(default_factory=lambda: get_upcast_env("DB_USER", "fastapimessenger"))
    password: str = field(default_factory=lambda: get_upcast_env("DB_PASSWORD", "fastapimessenger"), repr=False, hash=False)  # fmt: skip

    _url: str | None = field(default_factory=lambda: getenv("DB_URL"), repr=False, hash=False)

    fixtures_path = Path(APP_HOME / "database" / "fixtures")

    def __post_init__(self):
        if not self.fixtures_path.exists():
            raise ConfigException(f"Fixtures path not found: {self.fixtures_path}")

    @property
    def url(self):
        if self._url:
            return self._url

        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance

        if self.url.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.url,
                future=True,
                pool_use_lifo=True,
            )
        else:
            engine = create_async_engine(
                url=self.url,
                future=True,
            )

        self._engine_instance = engine
        return self._engine_instance


@dataclass
class SAQConfig:
    processes: int = field(default_factory=lambda: get_upcast_env("SAQ_PROCESSES", 1))
    concurrency: int = field(default_factory=lambda: get_upcast_env("SAQ_CONCURRENCY", 10))
    web_enabled: bool = field(default_factory=lambda: get_upcast_env("SAQ_WEB_ENABLED", True))
    use_server_lifespan: bool = field(default_factory=lambda: get_upcast_env("SAQ_USE_SERVER_LIFESPAN", True))


@dataclass
class LoggingConfig:
    level: str = field(default_factory=lambda: get_upcast_env("LOGGING_APP_LEVEL", "INFO"))

    uvicorn_access_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ACCESS_LEVEL", "INFO"))
    uvicorn_error_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ERROR_LEVEL", "ERROR"))

    saq_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SAQ_LEVEL", "INFO"))

    sqlalchemy_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SQLALCHEMY_LEVEL", "INFO"))


@dataclass
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    saq: SAQConfig = field(default_factory=SAQConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


@lru_cache(maxsize=1)
def get_config():
    return AppConfig()

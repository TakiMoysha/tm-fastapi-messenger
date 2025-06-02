from dataclasses import dataclass, field
from functools import lru_cache
from os import getenv
from pathlib import Path
from typing import Final, Literal

import fsspec
from s3fs import S3FileSystem
from advanced_alchemy.types.file_object.backends.fsspec import FSSpecBackend
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.exceptions import ConfigException
from app.lib.utils.upcast_env import get_upcast_env

APP_HOME: Final[Path] = Path(get_upcast_env("APP_HOME", "app")).absolute()

_storage_backend_type = Literal["s3", "local_store"]


@dataclass
class ServerConfig:
    title: str = "messenger"

    debug: bool = field(default_factory=lambda: get_upcast_env("SERVER_DEBUG", False))
    testing: bool = field(default_factory=lambda: get_upcast_env("SERVER_TESTING", False))

    secret_key: str = field(default_factory=lambda: get_upcast_env("SERVER_SECRET_KEY", "_dont_expose_me_"), repr=False, hash=False)  # fmt: skip
    access_token_expire_minutes: int = field(default_factory=lambda: get_upcast_env("SERVER_ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # fmt: skip
    password_algorithm: str = field(default_factory=lambda: get_upcast_env("SERVER_PASSWORD_ALGORITHM", "argon2"), repr=False, hash=False)  # fmt: skip
    token_algorithm: str = field(default_factory=lambda: get_upcast_env("SERVER_TOKEN_ALGORITHM", "HS256"), repr=False, hash=False)  # fmt: skip

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

    _url: str | None = field(default_factory=lambda: getenv("DB_URL", None), repr=False, hash=False)
    _engine_instance: AsyncEngine | None = None

    fixtures_path = Path(APP_HOME / "database" / "fixtures")

    def __post_init__(self):
        if not self.fixtures_path.exists():
            raise ConfigException(f"Fixtures path not found: {self.fixtures_path}")

    @property
    def url(self):
        if self._url:
            return self._url

        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def get_engine(self, *, debug: bool = False) -> AsyncEngine:
        if self._engine_instance is not None:
            return self._engine_instance

        if self.url.startswith("postgresql+asyncpg"):
            engine = create_async_engine(
                url=self.url,
                future=True,
                pool_use_lifo=True,
            )
        elif self.url.startswith("sqltite+aiosqlite") and self.url.endswith(":memory:"):
            engine = create_async_engine(
                url=self.url,
                debug=debug,
                echo=debug,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        else:
            engine = create_async_engine(
                url=self.url,
                future=True,
            )

        self._engine_instance = engine
        return self._engine_instance


@dataclass
class StorageConfig:
    backend: _storage_backend_type = field(default_factory=lambda: get_upcast_env("STORAGE_BACKEND", "local_store"))  # type: ignore

    s3_endpoint_url: str | None = field(default_factory=lambda: get_upcast_env("STORAGE_S3_ENDPOINT_URL", None))
    s3_access_key: str | None = field(default_factory=lambda: get_upcast_env("STORAGE_S3_ACCESS_KEY", None), repr=False, hash=False)  # fmt: skip
    s3_secret_key: str | None = field(default_factory=lambda: get_upcast_env("STORAGE_S3_SECRET_KEY", None), repr=False, hash=False)  # fmt: skip

    @property
    def key(self):
        return f"key_{self.backend}"

    def get_file_system(self):
        match self.backend:
            case "s3":
                if self.s3_endpoint_url is None or self.s3_access_key is None or self.s3_secret_key is None:
                    msg = f"Invalid S3 storage config: {self=}"
                    raise ConfigException(msg)
                fs = S3FileSystem(
                    anon=False,
                    key=self.s3_secret_key,
                    secret=self.s3_secret_key,
                    endpoint_url=self.s3_endpoint_url,
                )
                return fs
            case "local_store":
                return fsspec.filesystem("file")
            case _:
                raise ConfigException(f"Undefined error: {self=}")

    def get_default_storage(self):
        if self.backend == "s3":
            fs = self.get_file_system()
            return FSSpecBackend(fs=fs, key=self.key, prefix="fs_messenger_bucket")

        if self.backend == "local_store":
            fs = self.get_file_system()
            return FSSpecBackend(fs=fs, key=self.key)

        raise ConfigException(f"Undefined error: {self=}")


@dataclass
class LoggingConfig:
    level: str = field(default_factory=lambda: get_upcast_env("LOGGING_APP_LEVEL", "INFO"))

    uvicorn_access_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ACCESS_LEVEL", "INFO"))
    uvicorn_error_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_UVICORN_ERROR_LEVEL", "ERROR"))

    saq_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SAQ_LEVEL", "INFO"))

    sqlalchemy_level: str = field(default_factory=lambda: get_upcast_env("LOGGING_SQLALCHEMY_LEVEL", "WARN"))

    not_interesting: str = field(default_factory=lambda: get_upcast_env("LOGGING_NOT_INTERESTING_LEVEL", "INFO"))


@dataclass
class AppConfig:
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


@lru_cache(maxsize=1)
def get_config():
    return AppConfig()

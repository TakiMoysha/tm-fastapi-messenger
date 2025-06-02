from logging import getLogger

from app.server.plugins import setup_cache


logger = getLogger(__name__)


def create_asgi():
    from fastapi import FastAPI
    from fastapi.middleware import Middleware
    from fastapi.middleware.cors import CORSMiddleware

    from app.__about__ import __version__
    from app.config import get_config
    from app.server.lifespan import app_lifespan

    config = get_config()

    app = FastAPI(
        title="FastAPI-Messenger",
        version=__version__,
        debug=config.server.debug,
        lifespan=app_lifespan,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_credentials=True,
                allow_origins=config.server.cors_origins,
                allow_methods=config.server.cors_methods,
                allow_headers=config.server.cors_headers,
            ),
        ],
    )

    from app.server.plugins import setup_logging
    from app.server.plugins import setup_alchemy
    from app.server.plugins import setup_file_storage

    setup_alchemy(app)
    setup_logging(app)
    setup_cache(app)
    setup_file_storage(app)

    from app.router import root_router

    app.include_router(root_router)

    return app

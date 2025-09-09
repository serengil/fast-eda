# built-in dependencies
import asyncio

# 3rd party dependencies
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# 3rd party dependencies - continue
# pylint: disable=wrong-import-position
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# project dependencies
from modules.core.routes import router
from modules.core.bus import faststream_app
from dependencies.variables import Variables
from dependencies.container import Container

container: Container  # global container for app-level usage


def create_app() -> FastAPI:
    app = FastAPI()
    # enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    variables = Variables()
    container = Container(variables=variables)

    # dependency injection to router directly
    router.container = container

    app.include_router(router)
    container.logger.info("router registered")

    # startup event for FastStream
    @app.on_event("startup")
    async def start_faststream():
        # FastStream is blocking; we are staring with background task
        asyncio.create_task(faststream_app.run())
        container.logger.info("FastStream broker started")

    return app


service = create_app()

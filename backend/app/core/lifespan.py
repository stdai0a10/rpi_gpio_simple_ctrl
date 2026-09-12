import logging
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.core.settings import Settings
from app.frontend import validate_frontend_bundle

logger = logging.getLogger(__name__)
Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_lifespan(
    settings: Settings | None,
    frontend_directory: Path,
) -> Lifespan:
    """Create an application lifespan with optional injected settings."""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        active_settings = settings if settings is not None else Settings()
        validate_frontend_bundle(frontend_directory)
        application.state.settings = active_settings
        logger.info("Application started")
        try:
            yield
        finally:
            logger.info("Application stopped")

    return lifespan

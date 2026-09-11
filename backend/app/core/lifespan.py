import logging
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.core.settings import Settings

logger = logging.getLogger(__name__)
Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_lifespan(settings: Settings | None = None) -> Lifespan:
    """Create an application lifespan with optional injected settings."""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        active_settings = settings if settings is not None else Settings()
        application.state.settings = active_settings
        logger.info("Application started")
        try:
            yield
        finally:
            logger.info("Application stopped")

    return lifespan

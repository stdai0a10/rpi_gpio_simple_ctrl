from pathlib import Path

from fastapi import FastAPI

from app.api.middleware.trusted_ip import TrustedIPMiddleware
from app.api.router import api_router
from app.core.lifespan import create_lifespan
from app.core.settings import Settings
from app.frontend import DEFAULT_FRONTEND_DIRECTORY, register_frontend


def create_app(
    settings: Settings | None = None,
    frontend_directory: Path | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    active_frontend_directory = frontend_directory or DEFAULT_FRONTEND_DIRECTORY
    application = FastAPI(
        title="Raspberry Pi GPIO Simple Controller",
        version="0.1.0",
        lifespan=create_lifespan(settings, active_frontend_directory),
    )
    application.add_middleware(TrustedIPMiddleware)
    application.include_router(api_router)
    register_frontend(
        application,
        active_frontend_directory,
    )

    return application


app = create_app()

from fastapi import FastAPI

from app.api.middleware.trusted_ip import TrustedIPMiddleware
from app.api.router import api_router
from app.core.lifespan import create_lifespan
from app.core.settings import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="Raspberry Pi GPIO Simple Control",
        version="0.1.0",
        lifespan=create_lifespan(settings),
    )
    application.add_middleware(TrustedIPMiddleware)
    application.include_router(api_router)
    return application


app = create_app()

from fastapi import APIRouter

from app.api.routes.api_namespace import router as api_namespace_router
from app.api.routes.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
# Keep this last so future /api routes retain normal route priority.
api_router.include_router(api_namespace_router)

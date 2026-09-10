from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Report that the ASGI application can serve requests."""
    return {"status": "ok"}

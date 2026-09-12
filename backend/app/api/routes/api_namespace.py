from fastapi import APIRouter, HTTPException

_API_METHODS = (
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "TRACE",
    "CONNECT",
)

router = APIRouter()


@router.api_route("/api", methods=_API_METHODS, include_in_schema=False)
@router.api_route("/api/{path:path}", methods=_API_METHODS, include_in_schema=False)
def api_namespace_not_found(path: str = "") -> None:
    raise HTTPException(status_code=404)

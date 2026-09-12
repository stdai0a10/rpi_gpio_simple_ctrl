from pathlib import Path

from fastapi import FastAPI

DEFAULT_FRONTEND_DIRECTORY = Path(__file__).resolve().parents[2] / "frontend" / "dist"


def validate_frontend_bundle(frontend_directory: Path) -> None:
    expected_directory = frontend_directory.resolve()
    if not expected_directory.is_dir():
        raise RuntimeError(
            f"Frontend bundle is missing at '{expected_directory}'. "
            "Run 'npm --prefix frontend run build' or copy a matching "
            "frontend/dist bundle to this location."
        )
    index_path = expected_directory / "index.html"
    if not index_path.is_file():
        raise RuntimeError(
            f"Frontend bundle is incomplete: expected entry file '{index_path}'. "
            "Run 'npm --prefix frontend run build' or copy a matching "
            "frontend/dist bundle to this location."
        )


def register_frontend(application: FastAPI, frontend_directory: Path) -> None:
    """Register the compiled Vue frontend as FastAPI low-priority routes."""
    application.frontend(
        "/",
        directory=frontend_directory,
        fallback="index.html",
        check_dir=False,
    )

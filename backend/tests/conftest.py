from collections.abc import Iterator
from ipaddress import ip_network
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import create_app


@pytest.fixture
def frontend_directory(tmp_path: Path) -> Path:
    """Provide an isolated compiled frontend bundle for application tests."""
    directory = tmp_path / "frontend-dist"
    directory.mkdir()
    (directory / "index.html").write_text("<!doctype html><title>Test frontend</title>")
    return directory


@pytest.fixture(autouse=True)
def use_temporary_frontend_directory(
    frontend_directory: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Keep tests independent from an ignored working-tree frontend build."""
    monkeypatch.setattr("app.main.DEFAULT_FRONTEND_DIRECTORY", frontend_directory)


@pytest.fixture
def loopback_settings() -> Settings:
    return Settings(
        trusted_ip_ranges=(
            ip_network("127.0.0.1/32"),
            ip_network("::1/128"),
        ),
        _env_file=None,
    )


@pytest.fixture
def application(loopback_settings: Settings) -> FastAPI:
    return create_app(loopback_settings)


@pytest.fixture
def client(application: FastAPI) -> Iterator[TestClient]:
    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as test_client:
        yield test_client

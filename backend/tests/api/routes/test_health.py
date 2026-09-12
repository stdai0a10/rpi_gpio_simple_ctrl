import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.settings import Settings
from app.main import create_app

REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def test_importing_main_does_not_load_settings() -> None:
    environment = os.environ.copy()
    environment["TRUSTED_IP_RANGES"] = "not-a-network"

    result = subprocess.run(
        [sys.executable, "-c", "import app.main"],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_application_metadata(application: FastAPI) -> None:
    assert application.title == "Raspberry Pi GPIO Simple Controller"
    assert application.version == "0.1.0"


def test_lifespan_stores_injected_settings(
    application: FastAPI,
    loopback_settings: Settings,
) -> None:
    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ):
        assert application.state.settings is loopback_settings


def test_lifespan_rejects_invalid_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", "not-a-network")
    application = create_app()

    with pytest.raises(ValidationError):
        with TestClient(
            application,
            client=("127.0.0.1", 50000),
        ):
            raise AssertionError("Invalid settings unexpectedly started the app")


def test_health_returns_exact_liveness_response(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("path", ["/api/v1", "/api/v1/health"])
def test_unplanned_routes_are_not_defined(
    client: TestClient,
    path: str,
) -> None:
    response = client.get(path)

    assert response.status_code == 404

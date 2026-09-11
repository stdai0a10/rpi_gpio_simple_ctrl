import os
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_application_logs_use_uvicorn_configuration() -> None:
    environment = os.environ.copy()
    environment["TRUSTED_IP_RANGES"] = "127.0.0.1/32,::1/128"
    script = """
from fastapi.testclient import TestClient
from uvicorn import Config

from app.core.settings import Settings
from app.main import create_app

Config(app="app.main:app", use_colors=False).configure_logging()

allowed_application = create_app(Settings(_env_file=None))
with TestClient(
    allowed_application,
    client=("127.0.0.1", 50000),
) as client:
    assert client.get("/health").status_code == 200

denied_application = create_app(
    Settings(trusted_ip_ranges="192.0.2.0/24", _env_file=None)
)
with TestClient(
    denied_application,
    client=("127.0.0.1", 50000),
) as client:
    response = client.get(
        "/health?token=super-secret",
        headers={"Authorization": "Bearer super-secret"},
    )
    assert response.status_code == 403
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "INFO:     Application started" in result.stderr
    assert "INFO:     Application stopped" in result.stderr
    assert "WARNING:  Blocked request from 127.0.0.1: GET /health" in result.stderr
    assert "super-secret" not in result.stderr

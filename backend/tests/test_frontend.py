from ipaddress import ip_network
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import create_app


def create_frontend_distribution(directory: Path) -> Path:
    """Create a minimal compiled frontend bundle for HTTP tests."""
    directory.mkdir()
    (directory / "index.html").write_text(
        '<!doctype html><title>Test frontend</title><div id="app">SPA</div>',
        encoding="utf-8",
    )
    assets_directory = directory / "assets"
    assets_directory.mkdir()
    (assets_directory / "app.js").write_text(
        'console.log("frontend");',
        encoding="utf-8",
    )
    return directory


def test_trusted_client_loads_spa_root(
    tmp_path: Path,
    loopback_settings: Settings,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert (
        response.text
        == '<!doctype html><title>Test frontend</title><div id="app">SPA</div>'
    )


def test_lifespan_rejects_missing_frontend_directory(
    tmp_path: Path,
    loopback_settings: Settings,
) -> None:
    application = create_app(
        loopback_settings,
        frontend_directory=tmp_path / "missing-dist",
    )

    with pytest.raises(RuntimeError, match="Frontend bundle is missing"):
        with TestClient(
            application,
            client=("127.0.0.1", 50000),
        ):
            raise AssertionError(
                "A missing frontend bundle unexpectedly started the app"
            )


def test_lifespan_rejects_frontend_directory_without_entry_html(
    tmp_path: Path,
    loopback_settings: Settings,
) -> None:
    frontend_directory = tmp_path / "dist"
    frontend_directory.mkdir()
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with pytest.raises(RuntimeError, match="index.html"):
        with TestClient(
            application,
            client=("127.0.0.1", 50000),
        ):
            raise AssertionError(
                "An incomplete frontend bundle unexpectedly started the app"
            )


@pytest.mark.parametrize(
    "method",
    ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "TRACE", "CONNECT"),
)
@pytest.mark.parametrize("path", ["/api", "/api/functions/open-door"])
def test_unknown_api_path_returns_default_json_not_found(
    tmp_path: Path,
    loopback_settings: Settings,
    method: str,
    path: str,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as client:
        response = client.request(method, path, headers={"Accept": "text/html"})

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
    if method != "HEAD":
        assert response.json() == {"detail": "Not Found"}


def test_trusted_client_loads_compiled_frontend_asset(
    tmp_path: Path,
    loopback_settings: Settings,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as client:
        response = client.get("/assets/app.js")

    assert response.status_code == 200
    assert response.text == 'console.log("frontend");'


def test_trusted_client_loads_history_mode_frontend_route(
    tmp_path: Path,
    loopback_settings: Settings,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as client:
        response = client.get("/functions/open-door", headers={"Accept": "text/html"})

    assert response.status_code == 200
    assert (
        response.text
        == '<!doctype html><title>Test frontend</title><div id="app">SPA</div>'
    )


@pytest.mark.parametrize(
    ("path", "accept"),
    [
        ("/assets/missing.js", "application/javascript"),
        ("/functions/open-door", "application/json"),
    ],
)
def test_non_navigation_frontend_request_does_not_receive_spa_shell(
    tmp_path: Path,
    loopback_settings: Settings,
    path: str,
    accept: str,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    application = create_app(
        loopback_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("127.0.0.1", 50000),
    ) as client:
        response = client.get(path, headers={"Accept": accept})

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/assets/app.js",
        "/functions/open-door",
        "/api/functions/open-door",
        "/docs",
        "/redoc",
        "/openapi.json",
    ],
)
def test_untrusted_client_is_denied_for_frontend_and_backend_paths(
    tmp_path: Path,
    path: str,
) -> None:
    frontend_directory = create_frontend_distribution(tmp_path / "dist")
    restricted_settings = Settings(
        trusted_ip_ranges=(ip_network("192.0.2.0/24"),),
        _env_file=None,
    )
    application = create_app(
        restricted_settings,
        frontend_directory=frontend_directory,
    )

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get(path, headers={"Accept": "text/html"})

    assert response.status_code == 403
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Forbidden"}

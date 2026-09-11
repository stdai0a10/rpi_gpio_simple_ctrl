import asyncio
import json
from ipaddress import ip_network
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from starlette.types import Message, Receive, Scope, Send

from app.api.middleware.trusted_ip import TrustedIPMiddleware
from app.core.settings import Settings
from app.main import create_app


def build_settings(*ranges: str) -> Settings:
    return Settings(
        trusted_ip_ranges=tuple(ip_network(value) for value in ranges),
        _env_file=None,
    )


def build_http_scope(client_address: object) -> Scope:
    application = SimpleNamespace(
        state=SimpleNamespace(
            settings=build_settings("127.0.0.1/32"),
        )
    )
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "http",
        "path": "/health",
        "raw_path": b"/health",
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "server": ("testserver", 80),
        "client": client_address,
        "state": {},
        "app": application,
    }


async def invoke_middleware(scope: Scope) -> tuple[bool, list[Message]]:
    downstream_called = False
    messages: list[Message] = []

    async def downstream(
        downstream_scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        nonlocal downstream_called
        downstream_called = True
        await send(
            {
                "type": "http.response.start",
                "status": 204,
                "headers": [],
            }
        )
        await send({"type": "http.response.body", "body": b""})

    async def receive() -> Message:
        return {
            "type": "http.request",
            "body": b"",
            "more_body": False,
        }

    async def send(message: Message) -> None:
        messages.append(message)

    middleware = TrustedIPMiddleware(downstream)
    await middleware(scope, receive, send)
    return downstream_called, messages


def assert_forbidden(messages: list[Message]) -> None:
    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 403
    assert messages[1]["type"] == "http.response.body"
    assert json.loads(messages[1]["body"]) == {"detail": "Forbidden"}


def test_allows_ipv4_socket_peer_inside_configured_network() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("192.0.2.10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_allows_ipv6_socket_peer_inside_configured_network() -> None:
    application = create_app(build_settings("2001:db8::/32"))

    with TestClient(
        application,
        client=("2001:db8::10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_denies_socket_peer_outside_configured_network() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get("/health")

    assert response.status_code == 403
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"detail": "Forbidden"}


def test_x_forwarded_for_cannot_override_socket_peer() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get(
            "/health",
            headers={"X-Forwarded-For": "192.0.2.10"},
        )

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_untrusted_peer_is_denied_before_routing() -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get("/route-that-does-not-exist")

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


def test_missing_client_address_is_denied() -> None:
    scope = build_http_scope(("127.0.0.1", 50000))
    scope.pop("client")

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is False
    assert_forbidden(messages)


@pytest.mark.parametrize(
    "client_address",
    [
        None,
        (),
        ("not-an-ip", 50000),
        ("127.0.0.1",),
        ("127.0.0.1", 50000, "extra"),
        ["127.0.0.1", 50000],
        (127001, 50000),
        ("127.0.0.1", "50000"),
        ("127.0.0.1", True),
        ("127.0.0.1", -1),
        ("127.0.0.1", 65536),
    ],
)
def test_invalid_client_address_is_denied(client_address: object) -> None:
    scope = build_http_scope(client_address)

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is False
    assert_forbidden(messages)


def test_non_http_scope_passes_through() -> None:
    scope: Scope = {
        "type": "lifespan",
        "asgi": {"version": "3.0"},
        "state": {},
    }

    downstream_called, messages = asyncio.run(invoke_middleware(scope))

    assert downstream_called is True
    assert messages[0]["status"] == 204


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_documentation_routes_are_denied_to_untrusted_peers(path: str) -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("198.51.100.10", 50000),
    ) as client:
        response = client.get(path)

    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_documentation_routes_are_available_to_trusted_peers(path: str) -> None:
    application = create_app(build_settings("192.0.2.0/24"))

    with TestClient(
        application,
        client=("192.0.2.10", 50000),
    ) as client:
        response = client.get(path)

    assert response.status_code == 200

from collections.abc import Iterator
from ipaddress import ip_network

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.settings import Settings
from app.main import create_app


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

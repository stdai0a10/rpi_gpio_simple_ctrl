from ipaddress import ip_network
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.settings import Settings

LOOPBACK_NETWORKS = (
    ip_network("127.0.0.1/32"),
    ip_network("::1/128"),
)


@pytest.fixture(autouse=True)
def clear_trusted_ip_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRUSTED_IP_RANGES", raising=False)
    monkeypatch.delenv("trusted_ip_ranges", raising=False)


def test_missing_trusted_ip_ranges_uses_loopback_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == LOOPBACK_NETWORKS


@pytest.mark.parametrize("value", ["", "   \t"])
def test_blank_trusted_ip_ranges_uses_loopback_defaults(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == LOOPBACK_NETWORKS


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("192.0.2.0/24", (ip_network("192.0.2.0/24"),)),
        ("2001:db8::/32", (ip_network("2001:db8::/32"),)),
        (
            "192.0.2.0/24, 2001:db8::/32",
            (ip_network("192.0.2.0/24"), ip_network("2001:db8::/32")),
        ),
    ],
)
def test_valid_trusted_ip_ranges_are_parsed(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
    expected: tuple[object, ...],
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == expected


@pytest.mark.parametrize("value", ["not-a-network", "192.0.2.0/24,"])
def test_invalid_nonblank_trusted_ip_ranges_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
    value: str,
) -> None:
    monkeypatch.setenv("TRUSTED_IP_RANGES", value)

    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_os_environment_overrides_dotenv(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "TRUSTED_IP_RANGES=192.0.2.0/24\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("TRUSTED_IP_RANGES", "198.51.100.0/24")

    settings = Settings(_env_file=env_file)

    assert settings.trusted_ip_ranges == (ip_network("198.51.100.0/24"),)


def test_dotenv_ignores_unknown_keys(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "UNRELATED_FRONTEND_VALUE=kept-outside-settings\n"
        "TRUSTED_IP_RANGES=192.0.2.0/24\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.trusted_ip_ranges == (ip_network("192.0.2.0/24"),)


def test_environment_name_is_case_insensitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("trusted_ip_ranges", "192.0.2.0/24")

    settings = Settings(_env_file=None)

    assert settings.trusted_ip_ranges == (ip_network("192.0.2.0/24"),)

from ipaddress import IPv4Network, IPv6Network, ip_network
from pathlib import Path
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

IpNetwork = IPv4Network | IPv6Network
ROOT_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"
DEFAULT_TRUSTED_IP_RANGES: tuple[IpNetwork, ...] = (
    ip_network("127.0.0.1/32"),
    ip_network("::1/128"),
)
TrustedIpRanges = Annotated[tuple[IpNetwork, ...], NoDecode]


class Settings(BaseSettings):
    """Validated application settings."""

    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    trusted_ip_ranges: TrustedIpRanges = DEFAULT_TRUSTED_IP_RANGES

    @field_validator("trusted_ip_ranges", mode="before")
    @classmethod
    def parse_trusted_ip_ranges(cls, value: object) -> object:
        """Parse a comma-separated list while treating a blank value as default."""
        if not isinstance(value, str):
            return value

        if not value.strip():
            return DEFAULT_TRUSTED_IP_RANGES

        return tuple(ip_network(item.strip()) for item in value.split(","))

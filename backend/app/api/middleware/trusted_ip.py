import logging
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import cast

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.settings import Settings

logger = logging.getLogger(__name__)
IpAddress = IPv4Address | IPv6Address


class TrustedIPMiddleware:
    """Allow HTTP requests only when the socket peer is in a trusted network."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        source_address = self._source_address(scope)
        application = cast(FastAPI, scope["app"])
        settings: Settings = application.state.settings

        if source_address is not None and self._is_trusted(
            source_address,
            settings,
        ):
            await self.app(scope, receive, send)
            return

        source_label = (
            str(source_address)
            if source_address is not None
            else "<missing-or-invalid>"
        )
        logger.warning(
            "Blocked request from %s: %s %r",
            source_label,
            scope.get("method", "UNKNOWN"),
            scope.get("path", ""),
        )
        response = JSONResponse(
            status_code=403,
            content={"detail": "Forbidden"},
        )
        await response(scope, receive, send)

    @staticmethod
    def _source_address(scope: Scope) -> IpAddress | None:
        client = scope.get("client")
        if not isinstance(client, tuple) or len(client) != 2:
            return None

        host, port = client
        if not isinstance(host, str) or type(port) is not int or not 0 <= port <= 65535:
            return None

        try:
            return ip_address(host)
        except ValueError:
            return None

    @staticmethod
    def _is_trusted(address: IpAddress, settings: Settings) -> bool:
        return any(
            address.version == network.version and address in network
            for network in settings.trusted_ip_ranges
        )

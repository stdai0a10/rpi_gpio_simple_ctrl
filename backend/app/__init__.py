"""Raspberry Pi GPIO Simple Controller backend."""

import logging

logger = logging.getLogger(__name__)
logger.parent = logging.getLogger("uvicorn.error")

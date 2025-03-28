"""Fixtures for aiontfy tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

from aiohttp import ClientSession, WSMsgType
from aiohttp.web_ws import WebSocketResponse
from aioresponses import aioresponses
import pytest

MSG = """{"id": "h6Y2hKA5sy0U", "time": 1743184726, "expires": 1743227926, "event": "message", "topic": "test1", "message": "Hello", "title": "Title", "tags": ["octopus"], "priority": 3, "click": "https://example.com/", "actions": [], "attachment": null}"""
MSG_2 = """{"id": "h6Y2hKA5sy0U", "time": 1743184726, "expires": 1743227926, "event": "message", "topic": "test2", "message": "World", "title": "Title", "tags": ["octopus"], "priority": 5, "click": "https://example.com/", "actions": [], "attachment": null}"""


@pytest.fixture(autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses() as m:
        yield m


@pytest.fixture
def mock_session() -> Generator[AsyncMock]:
    """Mock aiohttp ClientSession."""
    return AsyncMock(spec=ClientSession)


@pytest.fixture
def mock_ws(mock_session: AsyncMock) -> Generator[AsyncMock]:
    """Mock aiohttp websocket connection."""

    mock_ws = AsyncMock(spec=WebSocketResponse)
    mock_ws.__aiter__.return_value = [
        MagicMock(type=WSMsgType.TEXT, data=MSG),
        MagicMock(type=WSMsgType.CLOSED),
    ]
    mock_session.ws_connect.return_value.__aenter__.return_value = mock_ws
    return mock_session

"""Fixtures for aiontfy tests."""

from collections.abc import Generator
from functools import lru_cache
import pathlib
from unittest.mock import AsyncMock, MagicMock

from aiohttp import ClientResponse, ClientSession, WSMsgType
from aiohttp.web_ws import WebSocketResponse
import pytest

MSG = """{"id": "h6Y2hKA5sy0U", "time": 1743184726, "expires": 1743227926, "event": "message", "topic": "test1", "message": "Hello", "title": "Title", "tags": ["octopus"], "priority": 3, "click": "https://example.com/", "actions": [], "attachment": null}"""
MSG_2 = """{"id": "h6Y2hKA5sy0U", "time": 1743184726, "expires": 1743227926, "event": "message", "topic": "test2", "message": "World", "title": "Title", "tags": ["octopus"], "priority": 5, "click": "https://example.com/", "actions": [], "attachment": null}"""


@pytest.fixture
def mock_session() -> Generator[AsyncMock]:
    """Mock aiohttp ClientSession."""
    mock_session = AsyncMock(spec=ClientSession)
    mock_response = AsyncMock(spec=ClientResponse, status=200)

    mock_session.request.return_value.__aenter__.return_value = mock_response

    return mock_session


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


@lru_cache
def load_fixture(filename: str) -> str:
    """Load a fixture."""

    return (
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf-8")
    )

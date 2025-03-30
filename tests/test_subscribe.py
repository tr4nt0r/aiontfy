"""Tests for subscribe method."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

from aiohttp import ClientError, WSMsgType
import pytest
from yarl import URL

from aiontfy import Event, Notification, Ntfy
from aiontfy.exceptions import (
    NtfyConnectionError,
    NtfyForbiddenAccessError,
    NtfyTimeoutError,
)

from .conftest import MSG, MSG_2


async def test_subscribe_success(mock_ws: AsyncMock) -> None:
    """Test successful subscription to a topic."""

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    await ntfy.subscribe(["test1"], callback_mock)

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test1/ws"), params={}, headers=None
    )
    callback_mock.assert_called_once()
    callback_mock.assert_called_with(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test1",
            message="Hello",
            title="Title",
            tags=["octopus"],
            priority=3,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )


async def test_subscribe_forbidden(
    mock_ws: AsyncMock,
) -> None:
    """Test subscription to a topic is forbidden."""

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    mock_ws.request.return_value.__aenter__.return_value.status = 403
    mock_ws.request.return_value.__aenter__.return_value.json.return_value = {
        "code": 40301,
        "http": 403,
        "error": "forbidden",
        "link": "https://ntfy.sh/docs/publish/#authentication",
    }

    with pytest.raises(NtfyForbiddenAccessError):
        await ntfy.subscribe(["test1"], callback_mock)


async def test_subscribe_with_filters(mock_ws: AsyncMock) -> None:
    """Test subscription with filters."""

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    await ntfy.subscribe(
        ["test1"],
        callback_mock,
        title="My Title",
        message="My Message",
        tags=["tag1", "tag2"],
        priority=[3],
    )

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test1/ws"),
        params={
            "title": "My Title",
            "message": "My Message",
            "tags": "tag1,tag2",
            "priority": "3",
        },
        headers=None,
    )
    callback_mock.assert_called_once()
    callback_mock.assert_called_with(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test1",
            message="Hello",
            title="Title",
            tags=["octopus"],
            priority=3,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )


async def test_subscribe_multiple_topics(mock_ws: AsyncMock) -> None:
    """Test subscription to multiple topics."""

    mock_ws.ws_connect.return_value.__aenter__.return_value.__aiter__.return_value = [
        MagicMock(type=WSMsgType.TEXT, data=MSG),
        MagicMock(type=WSMsgType.TEXT, data=MSG_2),
        MagicMock(type=WSMsgType.CLOSED),
    ]

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    await ntfy.subscribe(["test1", "test2"], callback_mock)

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test1,test2/ws"), params={}, headers=None
    )
    assert callback_mock.call_count == 2
    callback_mock.assert_any_call(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test1",
            message="Hello",
            title="Title",
            tags=["octopus"],
            priority=3,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )
    callback_mock.assert_any_call(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test2",
            message="World",
            title="Title",
            tags=["octopus"],
            priority=5,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )


@pytest.mark.parametrize(
    ("exception", "expected_exception"),
    [(TimeoutError, NtfyTimeoutError), (ClientError, NtfyConnectionError)],
)
async def test_subscribe_exceptions(
    mock_ws: AsyncMock, exception: Exception, expected_exception: Exception
) -> None:
    """Test timeout error during subscription."""

    mock_ws.ws_connect.side_effect = exception

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    with pytest.raises(expected_exception):
        await ntfy.subscribe(["test"], callback_mock)


@pytest.mark.parametrize(
    "ws_msg_type",
    [WSMsgType.ERROR, WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED],
)
async def test_subscribe_ws_errors(mock_ws: AsyncMock, ws_msg_type: WSMsgType) -> None:
    """Test handling of websocket error messages."""

    mock_ws.ws_connect.return_value.__aenter__.return_value.__aiter__.return_value = [
        MagicMock(type=ws_msg_type),
        MagicMock(type=WSMsgType.CLOSED),
    ]

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws)

    await ntfy.subscribe(["test"], callback_mock)

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test/ws"), params={}, headers=None
    )
    callback_mock.assert_not_called()


async def test_subscribe_basic_auth(mock_ws: AsyncMock) -> None:
    """Test successful subscription to a topic with basic authentication."""

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws, username="user", password="pass")  # noqa: S106

    await ntfy.subscribe(["test1"], callback_mock)

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test1/ws"),
        params={},
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
    )
    callback_mock.assert_called_once()
    callback_mock.assert_called_with(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test1",
            message="Hello",
            title="Title",
            tags=["octopus"],
            priority=3,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )


async def test_subscribe_bearer_auth(mock_ws: AsyncMock) -> None:
    """Test successful subscription to a topic with bearer authentication."""

    callback_mock = MagicMock()

    ntfy = Ntfy("https://example.com", mock_ws, token="dXNlcjpwYXNz")  # noqa: S106

    await ntfy.subscribe(["test1"], callback_mock)

    mock_ws.ws_connect.assert_called_once_with(
        URL("wss://example.com/test1/ws"),
        params={},
        headers={"Authorization": "Bearer dXNlcjpwYXNz"},
    )
    callback_mock.assert_called_once()
    callback_mock.assert_called_with(
        Notification(
            id="h6Y2hKA5sy0U",
            time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
            expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
            event=Event.MESSAGE,
            topic="test1",
            message="Hello",
            title="Title",
            tags=["octopus"],
            priority=3,
            click=URL("https://example.com/"),
            actions=[],
            attachment=None,
        )
    )

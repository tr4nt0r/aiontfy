"""Tests for aiontfy."""

from unittest.mock import AsyncMock

from yarl import URL

from aiontfy import Message, Ntfy

from .conftest import MSG


async def test_publish_message(mock_session: AsyncMock) -> None:
    """Test publishing a message to ntfy."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = MSG

    message = Message(topic="mytopic", title="Test", message="This is a test message")
    ntfy = Ntfy("http://example.com", mock_session)

    await ntfy.publish(message)

    mock_session.request.assert_called_once_with(
        "POST",
        URL("http://example.com"),
        json={
            "topic": "mytopic",
            "message": "This is a test message",
            "title": "Test",
            "tags": [],
            "priority": None,
            "actions": [],
            "click": None,
            "attach": None,
            "markdown": False,
            "icon": None,
            "filename": None,
            "delay": None,
            "email": None,
            "call": None,
        },
    )


async def test_publish_basic_auth(mock_session: AsyncMock) -> None:
    """Test publishing a message to ntfy with basic authentication."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = MSG

    message = Message(topic="mytopic", title="Test", message="This is a test message")
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    await ntfy.publish(message)

    mock_session.request.assert_called_once_with(
        "POST",
        URL("http://example.com"),
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
        json={
            "topic": "mytopic",
            "message": "This is a test message",
            "title": "Test",
            "tags": [],
            "priority": None,
            "actions": [],
            "click": None,
            "attach": None,
            "markdown": False,
            "icon": None,
            "filename": None,
            "delay": None,
            "email": None,
            "call": None,
        },
    )


async def test_publish_bearer_auth(mock_session: AsyncMock) -> None:
    """Test publishing a message to ntfy with bearer authentication."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = MSG

    message = Message(topic="mytopic", title="Test", message="This is a test message")
    ntfy = Ntfy("http://example.com", mock_session, token="dXNlcjpwYXNz")  # noqa: S106

    await ntfy.publish(message)

    mock_session.request.assert_called_once_with(
        "POST",
        URL("http://example.com"),
        headers={"Authorization": "Bearer dXNlcjpwYXNz"},
        json={
            "topic": "mytopic",
            "message": "This is a test message",
            "title": "Test",
            "tags": [],
            "priority": None,
            "actions": [],
            "click": None,
            "attach": None,
            "markdown": False,
            "icon": None,
            "filename": None,
            "delay": None,
            "email": None,
            "call": None,
        },
    )

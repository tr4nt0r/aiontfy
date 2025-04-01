"""Tests for aiontfy."""

from unittest.mock import AsyncMock

import pytest
from yarl import URL

from aiontfy import Everyone, Ntfy
from aiontfy.exceptions import NtfyUnauthorizedAuthenticationError


async def test_reservation(mock_session: AsyncMock) -> None:
    """Test reservation success."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        """{"success": true}"""
    )
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    assert await ntfy.reservation("mytopic", Everyone.READ)

    mock_session.request.assert_called_once_with(
        "POST",
        URL("http://example.com/v1/account/reservation"),
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
        json={"topic": "mytopic", "everyone": "read-only"},
    )


async def test_reservation_unauthorized(mock_session: AsyncMock) -> None:
    """Test reservation unauthorized error."""

    mock_session.request.return_value.__aenter__.return_value.status = 401
    mock_session.request.return_value.__aenter__.return_value.json.return_value = {
        "code": 40101,
        "http": 401,
        "error": "unauthorized",
        "link": "https://ntfy.sh/docs/publish/#authentication",
    }
    ntfy = Ntfy("http://example.com", mock_session, token="dXNlcjpwYXNz")  # noqa: S106

    with pytest.raises(NtfyUnauthorizedAuthenticationError):
        await ntfy.reservation("mytopic", Everyone.READ)


async def test_delete_reservation(mock_session: AsyncMock) -> None:
    """Test delete reservation method."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        """{"success": true}"""
    )
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    assert await ntfy.delete_reservation("mytopic")

    mock_session.request.assert_called_once_with(
        "DELETE",
        URL("http://example.com/v1/account/reservation/mytopic"),
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
    )


async def test_delete_reservation_and_delete_messages(mock_session: AsyncMock) -> None:
    """Test delete reservation and clear cached messages."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        """{"success": true}"""
    )
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    assert await ntfy.delete_reservation("mytopic", delete_messages=True)

    mock_session.request.assert_called_once_with(
        "DELETE",
        URL("http://example.com/v1/account/reservation/mytopic"),
        headers={"X-Delete-Messages": "true", "Authorization": "Basic dXNlcjpwYXNz"},
    )


async def test_delete_reservation_unauthorized(mock_session: AsyncMock) -> None:
    """Test delete reservation unauthorized error."""

    mock_session.request.return_value.__aenter__.return_value.status = 401
    mock_session.request.return_value.__aenter__.return_value.json.return_value = {
        "code": 40101,
        "http": 401,
        "error": "unauthorized",
        "link": "https://ntfy.sh/docs/publish/#authentication",
    }
    ntfy = Ntfy("http://example.com", mock_session, token="dXNlcjpwYXNz")  # noqa: S106

    with pytest.raises(NtfyUnauthorizedAuthenticationError):
        await ntfy.delete_reservation("mytopic")

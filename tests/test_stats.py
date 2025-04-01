"""Tests for aiontfy."""

from unittest.mock import AsyncMock

import pytest
from yarl import URL

from aiontfy import Ntfy
from aiontfy.exceptions import NtfyNotFoundPageError


async def test_stats(mock_session: AsyncMock) -> None:
    """Test message statistics."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        """{"messages":18,"messages_rate":0.007407407407407408}"""
    )
    ntfy = Ntfy("http://example.com", mock_session)

    stats = await ntfy.stats()

    mock_session.request.assert_called_once_with(
        "GET",
        URL("http://example.com/v1/stats"),
    )

    assert stats.messages == 18
    assert stats.messages_rate == 0.007407407407407408


async def test_stats_exception(mock_session: AsyncMock) -> None:
    """Test message statistics error."""

    mock_session.request.return_value.__aenter__.return_value.status = 404
    mock_session.request.return_value.__aenter__.return_value.json.return_value = {
        "code": 40401,
        "http": 404,
        "error": "page not found",
    }
    ntfy = Ntfy("http://example.com", mock_session)

    with pytest.raises(NtfyNotFoundPageError):
        await ntfy.stats()

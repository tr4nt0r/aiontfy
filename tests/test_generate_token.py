"""Tests for aiontfy."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from yarl import URL

from aiontfy import AccountTokenResponse, Ntfy
from aiontfy.exceptions import NtfyUnauthorizedAuthenticationError

from .conftest import load_fixture


async def test_generate_token(mock_session: AsyncMock) -> None:
    """Test generate token method."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("token.json")
    )
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    account = await ntfy.generate_token("label", datetime(2025, 12, 31, tzinfo=UTC))

    mock_session.request.assert_called_once_with(
        "POST",
        URL("http://example.com/v1/account/token"),
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
        json={"label": "label", "expires": 1767139200},
    )

    assert account == AccountTokenResponse.from_json(load_fixture("token.json"))


async def test_account_unauthorized(mock_session: AsyncMock) -> None:
    """Test account unauthorized error."""

    mock_session.request.return_value.__aenter__.return_value.status = 401
    mock_session.request.return_value.__aenter__.return_value.json.return_value = {
        "code": 40101,
        "http": 401,
        "error": "unauthorized",
        "link": "https://ntfy.sh/docs/publish/#authentication",
    }
    ntfy = Ntfy("http://example.com", mock_session, token="dXNlcjpwYXNz")  # noqa: S106

    with pytest.raises(NtfyUnauthorizedAuthenticationError):
        await ntfy.generate_token()

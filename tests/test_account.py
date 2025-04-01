"""Tests for aiontfy."""

from unittest.mock import AsyncMock

import pytest
from yarl import URL

from aiontfy import Account, Ntfy
from aiontfy.exceptions import NtfyUnauthorizedAuthenticationError

from .conftest import load_fixture


async def test_account(mock_session: AsyncMock) -> None:
    """Test account information."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("account.json")
    )
    ntfy = Ntfy("http://example.com", mock_session, username="user", password="pass")  # noqa: S106

    account = await ntfy.account()

    mock_session.request.assert_called_once_with(
        "GET",
        URL("http://example.com/v1/account"),
        headers={"Authorization": "Basic dXNlcjpwYXNz"},
    )

    assert account == Account.from_json(load_fixture("account.json"))


async def test_account_unauthenticated(mock_session: AsyncMock) -> None:
    """Test unauthenticated account information."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("account_anonymous.json")
    )
    ntfy = Ntfy("http://example.com", mock_session)

    account = await ntfy.account()

    mock_session.request.assert_called_once_with(
        "GET",
        URL("http://example.com/v1/account"),
    )

    assert account == Account.from_json(load_fixture("account_anonymous.json"))


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
        await ntfy.stats()

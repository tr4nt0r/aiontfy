"""Tests for aiontfy."""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

from yarl import URL

from aiontfy import Event, Notification, Ntfy

from .conftest import MSG_DELETE


async def test_delete_message(mock_session: AsyncMock) -> None:
    """Test deleting a message to ntfy."""

    mock_session.request.return_value.__aenter__.return_value.status = 200
    mock_session.request.return_value.__aenter__.return_value.text.return_value = (
        MSG_DELETE
    )

    ntfy = Ntfy("http://example.com", mock_session)

    resp = await ntfy.delete("mytopic", "Mc3otamDNcpJ")

    assert resp == Notification(
        id="h6Y2hKA5sy0U",
        time=datetime(2025, 3, 28, 17, 58, 46, tzinfo=UTC),
        expires=datetime(2025, 3, 29, 5, 58, 46, tzinfo=UTC),
        event=Event.MESSAGE_DELETE,
        topic="test1",
        message="Hello",
        title="Title",
        tags=["octopus"],
        priority=3,
        click=URL("https://example.com/"),
        icon=URL("https://example.com/icon.png"),
        actions=[],
        attachment=None,
        sequence_id="Mc3otamDNcpJ",
    )

    mock_session.request.assert_called_once_with(
        "DELETE",
        URL("http://example.com/mytopic/Mc3otamDNcpJ"),
    )

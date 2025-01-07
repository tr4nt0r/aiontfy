"""Tests for aiontfy."""

from dataclasses import asdict

from aiohttp import ClientSession
from aioresponses import aioresponses

from aiontfy import Message, Ntfy


async def test_publish_message(aioclient_mock: aioresponses) -> None:
    """Test publishing a message to ntfy."""

    aioclient_mock.post(
        "http://example.com",
        status=200,
        payload={
            "id": "12345",
            "time": 1736288009,
            "expires": 1736331209,
            "event": "message",
            "topic": "mytopic",
            "title": "Title",
            "message": "This is a test message",
            "content_type": "text/markdown",
        },
    )
    async with ClientSession() as session:
        message = Message(
            topic="mytopic", title="Test", message="This is a test message"
        )
        ntfy = Ntfy("http://example.com", session)

        await ntfy.publish(message)

    aioclient_mock.assert_called_once_with(
        "http://example.com", method="POST", json=asdict(message)
    )

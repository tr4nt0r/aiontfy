"""Async ntfy client library."""

from dataclasses import asdict
from typing import Any, Self

from aiohttp import ClientSession
from yarl import URL

from .helpers import get_user_agent
from .types import Message


class Ntfy:
    """Ntfy client."""

    def __init__(self, url: str, session: ClientSession | None = None) -> None:
        """Initialize Ntfy client."""
        self.url = URL(url)

        if session is not None:
            self._session = session
        else:
            self._session = ClientSession(headers={"User-Agent": get_user_agent()})
            self._close_session = True

    async def publish(self, message: Message) -> dict[str, Any]:
        """Publish a message to ntfy."""

        async with self._session.post(self.url, json=asdict(message)) as resp:
            return await resp.json()

    async def close(self) -> None:
        """Close session."""
        await self._session.close()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        """Async exit."""
        if self._close_session:
            await self._session.close()

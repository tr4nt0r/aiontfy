"""Async ntfy client library."""

from collections.abc import Callable
from dataclasses import asdict
from http import HTTPStatus
from typing import Any, Self

from aiohttp import ClientError, ClientSession, WSMsgType
from yarl import URL

from .exceptions import NtfyConnectionError, NtfyTimeoutError, raise_http_error
from .helpers import get_user_agent
from .types import Message, Notification


class Ntfy:
    """Ntfy client."""

    def __init__(self, url: str, session: ClientSession | None = None) -> None:
        """Initialize Ntfy client.

        Parameters
        ----------
        url : str
            The base URL for the Ntfy service.
        session : ClientSession, optional
            An existing aiohttp ClientSession. If not provided, a new session will be created.
        """
        self.url = URL(url)

        if session is not None:
            self._session = session
        else:
            self._session = ClientSession(headers={"User-Agent": get_user_agent()})
            self._close_session = True

    async def _request(self, method: str, url: URL, **kwargs) -> dict[str, Any]:
        """Handle API request.

        Parameters
        ----------
        method : str
            HTTP method (e.g., 'GET', 'POST').
        url : URL
            The URL to send the request to.
        **kwargs : dict
            Additional arguments to pass to the request.

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.

        Raises
        ------
        NtfyTimeoutError
            If a timeout occurs during the request.
        NtfyConnectionError
            If a client error occurs during the request.
        """

        try:
            async with self._session.request(method, url, **kwargs) as r:
                data = await r.json()
                if r.status >= HTTPStatus.BAD_REQUEST:
                    raise_http_error(**data)
                return data
        except TimeoutError as e:
            raise NtfyTimeoutError from e
        except ClientError as e:
            raise NtfyConnectionError from e

    async def publish(self, message: Message) -> dict[str, Any]:
        """Publish a message to ntfy.

        Parameters
        ----------
        message : Message
            The message to be published.

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.
        """

        return await self._request("POST", self.url, json=asdict(message))

    async def subscribe(  # noqa: PLR0913
        self,
        topics: list[str],
        callback: Callable[[Notification], None],
        title: str | None = None,
        message: str | None = None,
        tags: list[str] | None = None,
        priority: list[int] | None = None,
    ) -> None:
        """Subscribe to one or more ntfy topics.

        Parameters
        ----------
        topics : list[str]
            A list of topic names to subscribe to.
        callback : Callable[[Notification], None]
            A callback function that will be called when a new notification is received.
            The callback function should accept a single argument of type `Notification`.
        title : str, optional
            Filter: Only return messages that match this exact message string, defaults to None.
        message : str, optional
            Filter: Only return messages that match this exact title string, defaults to None.
        tags : list[str], optional
            A list of tags to use for the subscription, by default None.
        priority : int, optional
            The priority to use for the subscription, by default None.

        Raises
        ------
        NtfyTimeoutError
            If a timeout occurs during the subscription.
        NtfyConnectionError
            If a client error occurs during the subscription.

        """

        url = (
            self.url.with_scheme("wss" if self.url.scheme == "https" else "ws")
            / ",".join(topics)
            / "ws"
        )
        params = {}
        if title is not None:
            params["title"] = title
        if message is not None:
            params["message"] = message
        if tags is not None:
            params["tags"] = ",".join(tags)
        if priority is not None:
            params["priority"] = ",".join(str(x) for x in priority)

        try:
            async with self._session.ws_connect(url, params=params) as ws:
                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        callback(Notification.from_json(msg.data))
                    elif msg.type in (
                        WSMsgType.CLOSE,
                        WSMsgType.CLOSING,
                        WSMsgType.CLOSED,
                    ):
                        break
                    elif msg.type == WSMsgType.ERROR:
                        continue
        except TimeoutError as e:
            raise NtfyTimeoutError from e
        except ClientError as e:
            raise NtfyConnectionError from e

    async def close(self) -> None:
        """Close session.

        Closes the aiohttp ClientSession if it is not already closed.
        """
        if not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
        Self
            The Ntfy client instance.
        """
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        """Async exit.

        Closes the aiohttp ClientSession if it was created by this instance.

        Parameters
        ----------
        *exc_info : object
            Exception information.
        """
        if self._close_session:
            await self.close()

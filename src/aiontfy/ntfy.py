"""Async ntfy client library."""

from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime
from http import HTTPStatus
from typing import Any, Self

from aiohttp import BasicAuth, ClientError, ClientSession, WSMsgType
from yarl import URL

from .exceptions import NtfyConnectionError, NtfyTimeoutError, raise_http_error
from .helpers import get_user_agent
from .types import (
    Account,
    AccountTokenResponse,
    Everyone,
    Message,
    Notification,
    Response,
    Stats,
)


class Ntfy:
    """Ntfy client."""

    def __init__(
        self,
        url: str,
        session: ClientSession | None = None,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
    ) -> None:
        """Initialize Ntfy client.

        Parameters
        ----------
        url : str
            The base URL for the Ntfy service.
        session : ClientSession, optional
            An existing aiohttp ClientSession. If not provided, a new session will be created.
        """
        self.url = URL(url)
        self._headers = None

        if username is not None and password is not None:
            self._headers = {"Authorization": BasicAuth(username, password).encode()}
        elif token is not None:
            self._headers = {"Authorization": f"Bearer {token}"}

        if session is not None:
            self._session = session
        else:
            self._session = ClientSession(headers={"User-Agent": get_user_agent()})
            self._close_session = True

    async def _request(self, method: str, url: URL, **kwargs: Any) -> str:  # noqa: ANN401
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

        if self._headers:
            kwargs.setdefault("headers", {}).update(self._headers)

        try:
            async with self._session.request(method, url, **kwargs) as r:
                if r.status >= HTTPStatus.BAD_REQUEST:
                    raise_http_error(**(await r.json()))
                return await r.text()
        except TimeoutError as e:
            raise NtfyTimeoutError from e
        except ClientError as e:
            raise NtfyConnectionError from e

    async def publish(self, message: Message) -> Notification:
        """Publish a message to an ntfy topic.

        Parameters
        ----------
        message : Message
            The message to be published, containing details such as topic, title, and content.

        Returns
        -------
        Notification
            A `Notification` object representing the response from the ntfy service.

        Raises
        ------
        NtfyTimeoutError
            If a timeout occurs during the request.
        NtfyConnectionError
            If a client error occurs during the request.
        """
        return Notification.from_json(
            await self._request("POST", self.url, json=asdict(message))
        )

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
            Filter: Only return messages that match all listed tags, defaults to None
        priority : int, optional
            Filter: Only return messages that match any priority listed, defaults to None.

        Raises
        ------
        NtfyTimeoutError
            If a timeout occurs during the subscription.
        NtfyConnectionError
            If a client error occurs during the subscription.

        """

        await self.can_subscribe(topics)

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
            async with self._session.ws_connect(
                url, params=params, headers=self._headers
            ) as ws:
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

    async def can_subscribe(self, topics: list[str]) -> bool:
        """Check if the client can subscribe to a topic.

        Parameters
        ----------
        topics : list of str
            A list of topic names to check subscription permissions for.

        Returns
        -------
        bool
            True if the client can subscribe to the given topics.

        Raises
        ------
        NtfyForbiddenAccessError
            If the client is not authorized to subscribe to the given topics.
        """

        await self._request("GET", self.url / ",".join(topics) / "auth")

        return True

    async def stats(self) -> Stats:
        """Get message statistics.

        Returns
        -------
        Stats
            An instance of the `Stats` class containing message statistics.


        """

        return Stats.from_json(await self._request("GET", self.url / "v1/stats"))

    async def account(self) -> Account:
        """Get account information.

        Returns
        -------
        Account
            An instance of the `Account` class containing account information.

        Raises
        ------
        NtfyUnauthorizedAuthenticationError
            If the client is not authorized to access the account information.
        """
        return Account.from_json(await self._request("GET", self.url / "v1/account"))

    async def generate_token(
        self,
        label: str | None = None,
        expires: datetime | None = None,
    ) -> AccountTokenResponse:
        """
        Generate a token for the account.

        Parameters
        ----------
        label : str, optional
            A label for the token, defaults to None.
        expires : datetime, optional
            The expiration date and time for the token. If not provided, the token will not expire.

        Returns
        -------
        AccountTokenResponse
            An instance of `AccountTokenResponse` containing the generated token details.

        Raises
        ------
        NtfyUnauthorizedAuthenticationError
            If the client is not authenticated.
        """
        payload = {
            "label": label,
            "expires": int(expires.timestamp()) if expires else 0,
        }

        return AccountTokenResponse.from_json(
            await self._request("POST", self.url / "v1/account/token", json=payload)
        )

    async def reservation(self, topic: str, everyone: Everyone) -> bool:
        """Reserve or change the reservation status of a topic.

        Parameters
        ----------
        topic : str
            The topic to reserve.
        everyone : str
            The reservation status to set for the topic.

        Returns
        -------
        bool
            True if successfull.

        """

        return Response.from_json(
            await self._request(
                "POST",
                self.url / "v1/account/reservation",
                json={"topic": topic, "everyone": everyone.value},
            )
        ).success

    async def delete_reservation(
        self, topic: str, *, delete_messages: bool = False
    ) -> bool:
        """Delete a topic reservation.

        Parameters
        ----------
        topic : str
            The name of the topic whose reservation is to be deleted.
        delete_messages : bool, optional
            If True, deletes all messages and attachments that are cached on the server
            otherwise they will become publicly available. Defaults to False.

        Returns
        -------
        bool
            True if the reservation was successfully deleted, False otherwise.

        Raises
        ------
        NtfyUnauthorizedAuthenticationError
            If the client is not authenticated or the reservation does not exist.
        """
        kwargs = {}

        if delete_messages:
            kwargs["headers"] = {"X-Delete-Messages": "true"}

        return Response.from_json(
            await self._request(
                "DELETE", self.url / "v1/account/reservation" / topic, **kwargs
            )
        ).success

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

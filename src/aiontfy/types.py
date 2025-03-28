"""Type definitions for aiontfy."""

from dataclasses import dataclass, field
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin
from yarl import URL

from .const import MAX_PRIORITY, MIN_PRIORITY


@dataclass(kw_only=True, frozen=True)
class HttpAction(DataClassORJSONMixin):
    """An Http ntfy action.

    Attributes
    ----------
    label : str
        Label of the action button in the notification.
    url : URL
        URL to which the HTTP request will be sent.
    method : str, optional
        HTTP method to use for request, default is POST.
    headers : dict[str, str] or None, optional
        HTTP headers to pass in request.
    body : str or None, optional
        HTTP body.
    clear : bool, optional
        Clear notification after HTTP request succeeds. If the request fails, the notification is not cleared.
    """

    action: str = field(default="http", init=False)
    label: str
    url: URL = field(metadata=field_options(serialize=str, deserialize=URL))
    method: str = "POST"
    headers: dict[str, str] | None = None
    body: str | None = None
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class BroadcastAction(DataClassORJSONMixin):
    """A broadcast ntfy action.

    Attributes
    ----------
    label : str
        Label of the action button in the notification.
    intent : str or None, optional
        Android intent name, default is io.heckel.ntfy.USER_ACTION.
    extras : dict[str, str] or None, optional
        Android intent extras. Currently, only string extras are supported.
    clear : bool, optional
        Clear notification after action button is tapped.
    """

    action: str = field(default="broadcast", init=False)
    label: str
    intent: str | None = None
    extras: dict[str, str] | None = None
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class ViewAction(DataClassORJSONMixin):
    """A view ntfy action.

    Attributes
    ----------
    label : str
        Label of the action button in the notification.
    url : URL
        URL to open when action is tapped.
    clear : bool, optional
        Clear notification after action button is tapped.
    """

    action: str = field(default="view", init=False)
    label: str
    url: URL = field(metadata=field_options(serialize=str, deserialize=URL))
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class Message:
    """A message to publish to ntfy.

    Attributes
    ----------
    topic : str
        Target topic name.
    message : str or None, optional
        Message body; set to triggered if empty or not passed.
    title : str or None, optional
        Message title. Defaults to the topic short URL (ntfy.sh/mytopic) if not set.
    tags : list[str], optional
        List of tags that may or not map to emojis (https://docs.ntfy.sh/emojis/).
    priority : int or None, optional
        Message priority with 1=min, 3=default and 5=max
    actions : list[ViewAction or BroadcastAction or HttpAction], optional
        Custom user action buttons for notifications.
    click : URL or None, optional
        Website opened when notification is clicked.
    attach : URL or None, optional
        URL of an attachment.
    markdown : bool, optional
        Set to true if the message is Markdown-formatted.
    icon : URL or None, optional
        URL to use as notification icon.
    filename : str or None, optional
        File name of the attachment.
    delay : str or None, optional
        Timestamp or duration for delayed delivery.
    email : str or None, optional
        E-mail address for e-mail notifications.
    call : str or None, optional
        Phone number to use for voice call.

    """

    topic: str
    message: str | None = None
    title: str | None = None
    tags: list[str] = field(default_factory=list)
    priority: int | None = None
    actions: list[ViewAction | BroadcastAction | HttpAction] = field(
        default_factory=list
    )
    click: URL | None = None
    attach: URL | None = None
    markdown: bool = True
    icon: URL | None = None
    filename: str | None = None
    delay: str | None = None
    email: str | None = None
    call: str | None = None

    def __post_init__(self) -> None:
        """Post-initialization processing to validate attributes.

        Raises
        ------
        ValueError
            If the priority is not between the minimum and maximum allowed values.

        """

        if self.priority is not None and (
            self.priority < MIN_PRIORITY or self.priority > MAX_PRIORITY
        ):
            msg = f"Priority must be between {MIN_PRIORITY} and {MAX_PRIORITY}"
            raise ValueError(msg)


class Event(StrEnum):
    """Message type."""

    OPEN = "open"
    KEEPALIVE = "keepalive"
    MESSAGE = "message"
    POLL_REQUEST = "poll_request"


@dataclass(kw_only=True, frozen=True)
class Attachment(DataClassORJSONMixin):
    """Details about an attachment."""

    name: str
    url: URL = field(metadata=field_options(serialize=str, deserialize=URL))
    type: str | None = None
    size: int | None = None
    expires: int | None = None


@dataclass(kw_only=True, frozen=True)
class Notification(DataClassORJSONMixin):
    """A notification received from a subscribed topic."""

    id: str
    time: int
    expires: int | None = None
    event: Event
    topic: str
    message: str | None = None
    title: str | None = None
    tags: list[str] = field(default_factory=list)
    priority: int | None = None
    click: URL | None = field(
        default=None, metadata=field_options(serialize=str, deserialize=URL)
    )
    actions: list[ViewAction | BroadcastAction | HttpAction] = field(
        default_factory=list
    )
    attachment: Attachment | None = None

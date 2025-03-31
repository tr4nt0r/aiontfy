"""Type definitions for aiontfy."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import IntEnum, StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin
from yarl import URL

from .const import MAX_PRIORITY, MIN_PRIORITY


class DeleteAfter(IntEnum):
    """Delete after periods."""

    NEVER = 0
    AFTER_THREE_HRS = 10800
    AFTER_ONE_DAY = 86400
    AFTER_ONE_WEEK = 604800
    AFTER_ONE_MONTH = 2592000


class Priority(IntEnum):
    """Message priority."""

    MIN = 1
    LOW = 2
    DEFAULT = 3
    HIGH = 4
    MAX = 5


class Sound(StrEnum):
    """Notification sound."""

    NO_SOUND = "none"
    DING = "ding"
    JUNTOS = "juntos"
    PRISTINE = "pristine"
    DADUM = "dadum"
    POP = "pop"
    POP_SWOOSH = "pop-swoosh"
    BEEP = "beep"


class Everyone(StrEnum):
    """Everyone access."""

    DENY = "deny-all"
    READ = "read-only"
    WRITE = "write-only"
    READ_WRITE = "read-write"


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
    markdown: bool = False
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


def timestamp(ts: int) -> datetime:
    """Serialize timestamp to datetime."""
    return datetime.fromtimestamp(ts, tz=UTC)


@dataclass(kw_only=True, frozen=True)
class Attachment(DataClassORJSONMixin):
    """Details about an attachment."""

    name: str
    url: URL = field(metadata=field_options(serialize=str, deserialize=URL))
    type: str | None = None
    size: int | None = None
    expires: datetime | None = field(
        default=None, metadata=field_options(deserialize=timestamp)
    )


@dataclass(kw_only=True, frozen=True)
class Notification(DataClassORJSONMixin):
    """A notification received from a subscribed topic."""

    id: str
    time: datetime = field(metadata=field_options(deserialize=timestamp))
    expires: datetime | None = field(
        default=None, metadata=field_options(deserialize=timestamp)
    )
    event: Event
    topic: str
    message: str | None = None
    title: str | None = None
    tags: list[str] = field(default_factory=list)
    priority: Priority | None = None
    click: URL | None = field(
        default=None, metadata=field_options(serialize=str, deserialize=URL)
    )
    actions: list[ViewAction | BroadcastAction | HttpAction] = field(
        default_factory=list
    )
    attachment: Attachment | None = None
    content_type: str | None = None


@dataclass(kw_only=True, frozen=True)
class Stats(DataClassORJSONMixin):
    """Stats response.

    Attributes
    ----------
    messages : int
        The total number of messages.
    messages_rate : float
        Average number of messages per second.
    """

    messages: int
    messages_rate: float


@dataclass(kw_only=True, frozen=True)
class Subscription(DataClassORJSONMixin):
    """Subscription information."""

    base_url: URL = field(metadata=field_options(serialize=str, deserialize=URL))
    topic: str
    display_name: str


@dataclass(kw_only=True, frozen=True)
class NotificationPrefs(DataClassORJSONMixin):
    """Notification preferences."""

    sound: Sound | None = None
    min_priority: Priority | None = None
    delete_after: DeleteAfter | None = None


@dataclass(kw_only=True, frozen=True)
class AccountTokenResponse(DataClassORJSONMixin):
    """Account token response."""

    token: str
    label: str | None = None
    last_access: datetime = field(metadata=field_options(deserialize=timestamp))
    last_origin: str | None = None
    expires: datetime | None = field(
        default=None, metadata=field_options(deserialize=timestamp)
    )


@dataclass(kw_only=True, frozen=True)
class AccountTier(DataClassORJSONMixin):
    """Account tear information."""

    code: str
    name: str


@dataclass(kw_only=True, frozen=True)
class AccountLimits(DataClassORJSONMixin):
    """Account limits information."""

    basis: str | None = None
    messages: int
    messages_expiry_duration: int
    emails: int
    reservations: int
    attachment_total_size: int
    attachment_file_size: int
    attachment_bandwidth: int


@dataclass(kw_only=True, frozen=True)
class AccountStats(DataClassORJSONMixin):
    """Account stats."""

    messages: int
    messages_remaining: int
    emails: int
    emails_remaining: int
    reservations: int
    reservations_remaining: int
    attachment_total_size: int
    attachment_total_size_remaining: int


@dataclass(kw_only=True, frozen=True)
class Reservation(DataClassORJSONMixin):
    """Topic reservation settings."""

    topic: str
    everyone: str


@dataclass(kw_only=True, frozen=True)
class AccountBilling(DataClassORJSONMixin):
    """Acount billing information."""

    customer: bool
    subscription: bool
    status: str | None = None
    interval: str | None = None
    paid_until: datetime = field(metadata=field_options(deserialize=timestamp))
    cancel_at: datetime = field(metadata=field_options(deserialize=timestamp))


@dataclass(kw_only=True, frozen=True)
class Account(DataClassORJSONMixin):
    """Account response."""

    username: str
    role: str | None = None
    sync_topic: str | None = None
    language: str | None = None
    notification: NotificationPrefs | None = None
    subscriptions: list[Subscription] = field(default_factory=list)
    reservations: list[Reservation] = field(default_factory=list)
    tokens: list[AccountTokenResponse] = field(default_factory=list)
    tier: AccountTier | None = None
    limits: AccountLimits | None = None
    stats: AccountStats
    billing: AccountBilling | None = None


@dataclass(kw_only=True, frozen=True)
class Response(DataClassORJSONMixin):
    """Success response."""

    success: bool

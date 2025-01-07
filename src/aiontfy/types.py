"""Type definitions for aiontfy."""

from dataclasses import dataclass, field

from yarl import URL


@dataclass(kw_only=True, frozen=True)
class HttpAction:
    """A Http ntfy action."""

    action: str = field(default="http", init=False)
    label: str
    url: URL
    method: str = "POST"
    headers: dict[str, str] | None = None
    body: str | None = None
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class BroadcastAction:
    """A broadcast ntfy action."""

    action: str = field(default="broadcast", init=False)
    label: str
    url: URL
    intent: str | None = None
    extras: dict[str, str] | None = None
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class ViewAction:
    """A view ntfy action."""

    action: str = field(default="view", init=False)
    label: str
    url: URL
    clear: bool = False


@dataclass(kw_only=True, frozen=True)
class Message:
    """A message to publish to ntfy."""

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

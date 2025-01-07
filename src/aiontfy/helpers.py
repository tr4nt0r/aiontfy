"""Helpers for the aiontfy package."""

import platform

from aiohttp import __version__ as aiohttp_version

from .const import __version__


def get_user_agent() -> str:
    """Generate User-Agent string.

    The User-Agent string contains details about the operating system,
    its version, architecture, the aiontfy version, aiohttp version,
    and Python version.

    Returns
    -------
    str
        A User-Agent string with OS details, library versions, and a project URL.

    Examples
    --------
    >>> client.get_user_agent()
    'aiontfy/0.0.0 (Windows 11 (10.0.22000); 64bit)
     aiohttp/3.10.9 Python/3.12.7  +https://github.com/tr4nt0r/aiontfy')'

    """
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    arch, _ = platform.architecture()
    os_info = f"{os_name} {os_release} ({os_version}); {arch}"

    return (
        f"aiontfy/{__version__} ({os_info}) "
        f"aiohttp/{aiohttp_version} Python/{platform.python_version()} "
        " +https://github.com/tr4nt0r/aiontfy)"
    )

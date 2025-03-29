# aiontfy

Asynchronous client library for the [ntfy](https://ntfy.sh/) pub-sub notification service

[![build](https://github.com/tr4nt0r/aiontfy/workflows/Build/badge.svg)](https://github.com/tr4nt0r/aiontfy/actions)
[![codecov](https://codecov.io/gh/tr4nt0r/aiontfy/graph/badge.svg?token=aqCYYmMC6i)](https://codecov.io/gh/tr4nt0r/aiontfy)
[![PyPI version](https://badge.fury.io/py/aiontfy.svg)](https://badge.fury.io/py/aiontfy)
[!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/tr4nt0r)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub-Sponsor-blue?logo=github)](https://github.com/sponsors/tr4nt0r)

---

## 📖 Documentation

- **Full Documentation**: [https://tr4nt0r.github.io/aiontfy](https://tr4nt0r.github.io/aiontfy)

- **Source Code**: [https://github.com/tr4nt0r/aiontfy](https://github.com/tr4nt0r/aiontfy)

---

## 📦 Installation

You can install aiontfy via pip:

```sh
pip install aiontfy
```

---

## 🚀 Usage

### Basic Examples

```python
"""Publish to a ntfy topic."""

from aiohttp import ClientSession

from aiontfy import Message, Ntfy

async with ClientSession() as session:

    ntfy = Ntfy("https://ntfy.sh", session)

    message = Message(
        topic="aiontfy",
        title="Hello",
        message="World",
        click="https://example.com/",
        delay="10s",
        priority=3,
        tags=["octopus"],
    )
    print(await ntfy.publish(message))


```

```python
"""Subscribe to ntfy topics."""

import asyncio

from aiohttp import ClientSession

from aiontfy import Event, Notification, Ntfy


def callback(message: Notification) -> None:
    """Process notifications callback function."""
    if message.event is Event.MESSAGE:
        print(message.to_dict())


async def main() -> None:
    async with ClientSession() as session:
        ntfy = Ntfy("https://ntfy.sh", session)

        await ntfy.subscribe(
            ["aiontfy", "test"],  # Subscribe to multiple topics
            callback,
            priority=[3, 4, 5],  # Only subscribe to priority >= 3
        )


asyncio.run(main())

For more advanced usage, refer to the [documentation](https://tr4nt0r.github.io/pynecil).

```

---

## 🛠 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request.

Make sure to follow the [contributing guidelines](CONTRIBUTING.md).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❤️ Support

If you find this project useful, consider [buying me a coffee ☕](https://www.buymeacoffee.com/tr4nt0r) or [sponsoring me on GitHub](https://github.com/sponsors/tr4nt0r)!

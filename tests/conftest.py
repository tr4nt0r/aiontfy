"""Fixtures for aiontfy tests."""

from collections.abc import Generator

from aioresponses import aioresponses
import pytest


@pytest.fixture(autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses() as m:
        yield m

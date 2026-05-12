"""Live-device smoke tests.

Skipped by default. To run against a real BSC200::

    LIGPSPORT_DEVICE_ADDRESS=AA:BB:CC:DD:EE:FF \\
      nix develop --command pytest -q -m bsc200 tests/test_bsc200_live.py

These tests only cover non-destructive read paths — see AGENTS.md §2.
"""

from __future__ import annotations

import os

import pytest

from ligpsport.ble import BleakTransport
from ligpsport.client import IgpsportClient
from ligpsport.commands import (
    DeviceStatus,
    DeviceVersion,
    RideList,
    SensorList,
    UserConfig,
    run_named,
)

pytestmark = pytest.mark.bsc200


def _addr() -> str:
    addr = os.environ.get("LIGPSPORT_DEVICE_ADDRESS")
    if not addr:
        pytest.skip("set LIGPSPORT_DEVICE_ADDRESS to run live-device tests")
    return addr


@pytest.fixture
async def client() -> IgpsportClient:
    addr = _addr()
    async with BleakTransport(addr) as transport, IgpsportClient(transport) as c:
        yield c


async def test_live_version(client: IgpsportClient) -> None:
    result = await run_named(client, "version", timeout=10.0)
    assert isinstance(result.value, DeviceVersion)
    # The BSC200 firmware in scope here is "May 14 2024 11:07:51" with
    # protocol_ver=101, BLE app=141, hardware=100. We don't assert exact
    # numbers — they're firmware-dependent — but a non-empty compile
    # time and a protocol >= 101 mean we parsed the response correctly.
    assert result.value.compile_time.strip()
    assert result.value.protocol_ver >= 101


async def test_live_status(client: IgpsportClient) -> None:
    result = await run_named(client, "status", timeout=10.0)
    assert isinstance(result.value, DeviceStatus)
    # No assertions about the actual values — the device may be in any
    # state. Just confirm the dataclass populated without error.


async def test_live_user(client: IgpsportClient) -> None:
    result = await run_named(client, "user", timeout=10.0)
    assert isinstance(result.value, UserConfig)


async def test_live_rides(client: IgpsportClient) -> None:
    result = await run_named(client, "rides", timeout=10.0)
    assert isinstance(result.value, RideList)


async def test_live_sensors(client: IgpsportClient) -> None:
    result = await run_named(client, "sensors", timeout=10.0)
    assert isinstance(result.value, SensorList)

"""Live-device smoke tests.

Skipped by default. To run against a real BSC200::

    LIGPSPORT_DEVICE_ADDRESS=AA:BB:CC:DD:EE:FF \\
      nix develop --command pytest -q -m bsc200 tests/test_bsc200_live.py

These tests cover **read-only paths only**. Destructive ops
(``sim-activity`` / ``del-activity`` / ``delete-all-rides``) are
deliberately excluded so the suite is safe to re-run repeatedly
without manual prep. The destructive paths are exercised against
the in-tree simulator in ``tests/test_activities.py`` and live-
verified once per release as part of the release-engineer's
checklist (PROTOCOL.md §7.5, the FILE_DEL retest); they are *not*
auto-runnable here because:

* Deleting the device's lone recorded activity wipes the test
  target for every subsequent live run, forcing the engineer to
  manually record a new ride before the suite can pass again.
* ``sim-activity`` acks ``status=0`` on BSC200 firmware
  2024-05-14 but silently no-ops, so it can't seed a replacement
  activity either (PROTOCOL.md §6.9). Until iGPSPORT firmware
  actually honours SIM_FIT_SET, the destructive cycle costs a
  human ride.

See AGENTS.md §2 for the broader destructive policy.
"""

from __future__ import annotations

import os

import pytest

from ligpsport.ble import BleakTransport
from ligpsport.client import IgpsportClient
from ligpsport.commands import (
    ActivityList,
    DeviceStatus,
    DeviceVersion,
    DownloadedFile,
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
    assert isinstance(result.value, ActivityList)


async def test_live_list_activities(client: IgpsportClient) -> None:
    """``list-activities`` succeeds — entries may be empty or non-empty."""
    result = await run_named(client, "list-activities", timeout=10.0)
    assert isinstance(result.value, ActivityList)


async def test_live_download_activity(client: IgpsportClient, tmp_path) -> None:
    """If at least one activity is present, downloading it produces FIT bytes.

    Read-only — uses the third UART RX (``…-7e``) + file_tag=0x55
    transmit-complete path documented in PROTOCOL.md §6.4. Skips if
    the device has no recorded activities to pull (test harness can't
    create one on its own).
    """
    listing = await run_named(client, "list-activities", timeout=10.0)
    activities = listing.value
    assert isinstance(activities, ActivityList)
    if not activities.files:
        pytest.skip("BSC200 has no recorded activities to download")
    target = activities.files[0]
    out = tmp_path / f"activity_{target.timestamp}.fit"
    result = await run_named(
        client,
        "download-activity",
        args=(str(target.timestamp), str(out)),
        timeout=30.0,
    )
    assert isinstance(result.value, DownloadedFile)
    assert result.value.size_bytes == target.file_size
    assert result.value.fit_magic is True


async def test_live_sensors(client: IgpsportClient) -> None:
    result = await run_named(client, "sensors", timeout=10.0)
    assert isinstance(result.value, SensorList)

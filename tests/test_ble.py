"""Smoke tests for BleakTransport's MTU handling.

The real verification of the MTU fix is manual — it only fires on a
live BLE connection where bleak's BlueZ backend would otherwise warn
"Using default MTU value" on every write. These tests assert the
two static guarantees we can check without a radio: the connect
path calls ``_acquire_mtu`` AND sets ``_mtu_size`` as a fallback.
"""

from __future__ import annotations

import inspect

from ligpsport.ble import BleakTransport


def test_open_acquires_mtu_and_sets_fallback_mtu_size() -> None:
    source = inspect.getsource(BleakTransport.open)
    assert "_acquire_mtu" in source, "open() must call bleak's _acquire_mtu()"
    assert "_mtu_size" in source, "open() must set _mtu_size as a fallback"


def test_fallback_mtu_matches_bsc200_negotiated_value() -> None:
    # PROTOCOL.md §1: BSC200 negotiates 247 with the Android app.
    assert BleakTransport._FALLBACK_MTU == 247

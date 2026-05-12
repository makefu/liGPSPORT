"""BLE device discovery for iGPSPORT cycling computers.

The scanner walks BLE advertising packets for a configurable window,
filters them to devices whose advertised name begins with one of
:data:`ligpsport.gatt.NAME_PREFIXES`, and returns them as
:class:`Device` records. The MAC address is incidental — the iGPSPORT
family advertises consistent name prefixes (``BSC``, ``iGS``,
``iGPSPORT``) which is what the scanner matches on.

Live BLE scanning needs a real Bluetooth adapter and ``bleak``;
the function isn't called by unit tests.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import AsyncIterator

from . import gatt

_LOG = logging.getLogger(__name__)


@dataclasses.dataclass(slots=True, frozen=True)
class Device:
    """One BLE device the scanner saw matching the iGPSPORT name pattern."""

    address: str
    name: str
    rssi: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {"address": self.address, "name": self.name, "rssi": self.rssi}


def _is_igpsport_name(name: str | None) -> bool:
    if not name:
        return False
    return name.startswith(gatt.NAME_PREFIXES)


async def discover(*, timeout: float = 6.0) -> list[Device]:
    """Scan for *timeout* seconds and return every iGPSPORT device seen.

    Each MAC address is reported once with the highest-quality
    advertising packet observed. Order is insertion (first-seen
    first).
    """
    # Lazy import so test environments without a BLE stack still load
    # this module.
    from bleak import BleakScanner  # type: ignore[import-not-found]

    seen: dict[str, Device] = {}

    def _callback(device: object, adv: object) -> None:
        try:
            name = getattr(adv, "local_name", None) or getattr(device, "name", None)
            address = device.address  # type: ignore[attr-defined]
            rssi = getattr(adv, "rssi", None)
        except AttributeError:
            return
        if not _is_igpsport_name(name):
            return
        existing = seen.get(address)
        if existing is None or (
            rssi is not None and (existing.rssi is None or rssi > existing.rssi)
        ):
            seen[address] = Device(address=address, name=str(name), rssi=rssi)

    scanner = BleakScanner(detection_callback=_callback)
    await scanner.start()
    try:
        import asyncio as _asyncio

        await _asyncio.sleep(timeout)
    finally:
        await scanner.stop()
    return list(seen.values())


async def watch(*, max_count: int | None = None) -> AsyncIterator[Device]:
    """Yield iGPSPORT devices as their advertisements arrive.

    Unlike :func:`discover` this is open-ended; the caller stops it by
    breaking out of the iteration or passing *max_count*. Useful for
    CLI ``--watch`` modes.
    """
    import asyncio as _asyncio

    from bleak import BleakScanner  # type: ignore[import-not-found]

    queue: _asyncio.Queue[Device] = _asyncio.Queue()
    seen: set[str] = set()

    def _callback(device: object, adv: object) -> None:
        try:
            address = device.address  # type: ignore[attr-defined]
            name = getattr(adv, "local_name", None) or getattr(device, "name", None)
            rssi = getattr(adv, "rssi", None)
        except AttributeError:
            return
        if address in seen or not _is_igpsport_name(name):
            return
        seen.add(address)
        queue.put_nowait(Device(address=address, name=str(name), rssi=rssi))

    scanner = BleakScanner(detection_callback=_callback)
    await scanner.start()
    try:
        count = 0
        while max_count is None or count < max_count:
            yield await queue.get()
            count += 1
    finally:
        await scanner.stop()

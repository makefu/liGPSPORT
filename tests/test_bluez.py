"""Module-level smoke test for the BlueZ-direct backend.

We can't open a real DBus connection in the unit suite (no adapter,
no D-Bus system bus), but we can exercise the reassembly buffer that
:class:`BluezTransport._on_chunk` shares with the rest of the
codebase. The actual connect path is covered by the live device
tests.
"""

from __future__ import annotations

import pytest

from ligpsport.bluez import BluezTransport
from ligpsport.framing import Frame, build_frame


def _split(data: bytes, chunk: int) -> list[bytes]:
    return [data[i : i + chunk] for i in range(0, len(data), chunk)]


def test_reassembly_single_chunk() -> None:
    transport = BluezTransport(address="00:11:22:33:44:55")
    wire = build_frame(Frame(service=10, operation=2, payload=b"hello"))
    transport._on_chunk(wire)
    # The reassembled frame ends up in the inbox without blocking.
    assert transport._inbox.qsize() == 1


def test_reassembly_multi_chunk() -> None:
    transport = BluezTransport(address="00:11:22:33:44:55")
    wire = build_frame(Frame(service=17, operation=2, payload=b"\x00" * 200))
    for chunk in _split(wire, chunk=64):
        transport._on_chunk(chunk)
    assert transport._inbox.qsize() == 1


def test_reassembly_two_frames() -> None:
    transport = BluezTransport(address="00:11:22:33:44:55")
    first = build_frame(Frame(service=10, operation=2, payload=b"first"))
    second = build_frame(Frame(service=17, operation=2, payload=b"second"))
    transport._on_chunk(first + second)
    assert transport._inbox.qsize() == 2


def test_send_before_open_raises() -> None:
    import asyncio

    from ligpsport.transport import TransportClosed

    transport = BluezTransport(address="00:11:22:33:44:55")
    with pytest.raises(TransportClosed):
        asyncio.run(transport.send(b"\x00" * 20))

"""Async transport abstraction shared by the BLE client and the simulator.

A transport delivers and receives **fully reassembled** logical frames
(20-byte header + protobuf payload as a single byte-string). The codec
in :mod:`ligpsport.framing` lives on top; the transport itself is
oblivious to header contents.

Two implementations:

* :class:`LoopbackTransport` — paired in-memory queues; used by the
  in-tree :mod:`ligpsport.simulator` and the test suite to exercise the
  client end-to-end without a BLE adapter.
* :class:`BleakTransport` — a real BLE/GATT transport built on
  `bleak <https://github.com/hbldh/bleak>`_. Subscribes to TX
  notifications, reassembles MTU-sized notification chunks back into
  whole logical frames using the ``totalSize`` field from the framing
  header, and writes RX bytes split into MTU-sized chunks. Defined in
  this module so the public surface stays in one place; concrete
  callers normally go through :class:`ligpsport.client.IgpsportClient`.

The ABC is intentionally minimal: ``send(frame)`` is "deliver one
logical frame" and ``receive()`` returns "the next fully-assembled
logical frame the peer sent". Higher layers pair them up into
request/response semantics.

The ``channel`` kwarg on :meth:`Transport.send` selects which BLE
characteristic the frame is written to. The iGPSPORT app uses four
parallel Nordic-UART channels; for the common case (every command in
this library except multi-channel file uploads) the default
``"control"`` channel — the ``…-8e`` UART — is correct. Multi-channel
file uploads (``ligpsport.file_transfer.upload_route_plan``) write
their bulk-data chunk to ``"data"`` (``…-9e``) or ``"fourth"``
(``…-6e``) depending on the device generation, then write a 20-byte
trailer back on ``"control"``.
"""

from __future__ import annotations

import abc
import asyncio
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Final, Literal

if TYPE_CHECKING:
    from types import TracebackType


Channel = Literal["control", "data", "fourth"]
"""Selects which BLE characteristic ``Transport.send`` writes to.

The names mirror the iGPSPORT app's smali (``mControlRxCharacteristic``,
``mRxCharacteristic``, ``mFourthRxCharacteristic``) and the UUID
suffixes from :mod:`ligpsport.gatt`:

* ``"control"`` — ``PRIMARY_RX_UUID`` (``…-8e``). All read commands
  and most writes go here.
* ``"data"`` — ``DATA_RX_UUID`` (``…-9e``). The data-bearing channel
  for generation-1/2 devices' file-upload chunks.
* ``"fourth"`` — ``FOURTH_RX_UUID`` (``…-6e``). The data-bearing
  channel for generation-3+ devices' file-upload chunks.
"""

CHANNELS: Final[tuple[Channel, ...]] = ("control", "data", "fourth")


class TransportClosed(RuntimeError):
    """Raised by :meth:`Transport.receive` when the peer has gone away."""


class Transport(abc.ABC):
    """Wire-level peer abstraction.

    Implementations must guarantee that ``send`` delivers each frame as
    a single atomic unit on the wire (no interleaving with a concurrent
    send), and that ``receive`` yields a frame only when it is fully
    assembled (all MTU chunks concatenated, header included).
    """

    @abc.abstractmethod
    async def send(self, frame: bytes, *, channel: Channel = "control") -> None:
        """Deliver one fully-formed frame to the peer on *channel*."""

    @abc.abstractmethod
    async def receive(self) -> bytes:
        """Return the next fully-assembled frame from the peer.

        Raises :class:`TransportClosed` if the peer has disconnected and
        no further frames will arrive.
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """Tear down the transport. Idempotent."""

    async def frames(self) -> AsyncIterator[bytes]:
        """Iterate frames until the peer disconnects."""
        try:
            while True:
                yield await self.receive()
        except TransportClosed:
            return

    async def __aenter__(self) -> Transport:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()


class LoopbackTransport(Transport):
    """In-memory transport for the simulator and test suite.

    A :class:`LoopbackTransport` reads from one queue (its "inbox") and
    writes to another (its peer's inbox). Two transports are paired
    with :func:`make_loopback_pair` so the client and simulator each
    see the other's writes as their reads — the exact same bytes
    traverse both halves, so an encoding regression on either side
    surfaces in tests as a parse error rather than a mock not firing.

    Loopback preserves the channel tag end-to-end: each item in the
    queue is a ``(channel, bytes)`` tuple. :meth:`receive` returns just
    the bytes (matching the real BLE transports, which don't surface
    the source characteristic), while :meth:`receive_with_channel`
    exposes the tag for tests and the simulator's multi-channel
    handlers (e.g. the route-plan file upload).
    """

    def __init__(
        self,
        inbox: asyncio.Queue[tuple[Channel, bytes] | None],
        outbox: asyncio.Queue[tuple[Channel, bytes] | None],
    ):
        self._inbox = inbox
        self._outbox = outbox
        self._closed = False

    async def send(self, frame: bytes, *, channel: Channel = "control") -> None:
        if self._closed:
            raise TransportClosed("transport is closed")
        await self._outbox.put((channel, frame))

    async def receive(self) -> bytes:
        _, frame = await self.receive_with_channel()
        return frame

    async def receive_with_channel(self) -> tuple[Channel, bytes]:
        """Like :meth:`receive` but also return the source channel.

        Used by the simulator's multi-channel handlers (route-plan
        upload pairs a ``data`` or ``fourth`` chunk with a ``control``
        trailer per chunk).
        """
        item = await self._inbox.get()
        if item is None:
            raise TransportClosed("peer closed the transport")
        return item

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        # Signal peer that no more frames will arrive on its inbox.
        await self._outbox.put(None)


def make_loopback_pair() -> tuple[LoopbackTransport, LoopbackTransport]:
    """Return ``(client_side, peer_side)`` connected by two queues.

    Frames written to the client side appear on the peer side's
    ``receive``, and vice versa.
    """
    a_inbox: asyncio.Queue[tuple[Channel, bytes] | None] = asyncio.Queue()
    b_inbox: asyncio.Queue[tuple[Channel, bytes] | None] = asyncio.Queue()
    return LoopbackTransport(a_inbox, b_inbox), LoopbackTransport(b_inbox, a_inbox)

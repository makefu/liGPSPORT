"""BlueZ-direct BLE transport backend.

Parallel implementation to :class:`ligpsport.ble.BleakTransport`. Both
satisfy the :class:`ligpsport.transport.Transport` ABC, so the higher
layers (client, simulator, commands) don't care which one is in use.

The motivation for a second backend: bleak wraps BlueZ's DBus API at
a level that doesn't expose **MTU control** in a useful way on Linux.
The BSC200's route-upload path sends ~26 KB of data in one logical
blob; with BlueZ's default 23-byte ATT MTU that becomes 1300+
sequential ATT Write Commands, which the device's input buffer
appears to drop. The iGPSPORT Android app negotiates ~244 bytes via
``ConfigureMTUOperation`` and the BSC200 accepts the upload happily.

This backend bypasses bleak and talks to BlueZ via DBus directly,
using two specific BlueZ features:

* ``org.bluez.GattCharacteristic1.AcquireWrite`` — returns a Unix
  file descriptor plus the *negotiated* MTU. Writes to the FD go
  out as ATT Write Commands sized up to that MTU. No per-write DBus
  round-trip; we just ``os.write(fd, chunk)``.
* ``org.bluez.GattCharacteristic1.AcquireNotify`` — returns a Unix
  file descriptor that delivers raw notification bytes. Subscribing
  this way also bumps the MTU during connection setup.

Selecting between backends:

* ``ligpsport.ble.BleakTransport`` — default; portable across
  Linux / macOS / Windows; uses bleak.
* ``ligpsport.bluez.BluezTransport`` — Linux-only; needs BlueZ
  >= 5.50 (for the Acquire* methods) and DBus access to
  ``org.bluez``. Use this when you need MTU control or when bleak's
  abstraction is getting in the way.

The CLI's ``--backend bluez`` flag flips to this backend.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
from typing import TYPE_CHECKING, Final

from . import framing, gatt
from .transport import Transport, TransportClosed

if TYPE_CHECKING:
    from types import TracebackType


_LOG = logging.getLogger(__name__)

BLUEZ_SERVICE: Final[str] = "org.bluez"
ADAPTER_IFACE: Final[str] = "org.bluez.Adapter1"
DEVICE_IFACE: Final[str] = "org.bluez.Device1"
GATT_SERVICE_IFACE: Final[str] = "org.bluez.GattService1"
GATT_CHAR_IFACE: Final[str] = "org.bluez.GattCharacteristic1"
DBUS_OM_IFACE: Final[str] = "org.freedesktop.DBus.ObjectManager"

# We subscribe TX on every UART channel — the BSC200 writes responses
# on the data channel (9e) even though we drive writes on the control
# channel (8e). See PROTOCOL.md §1.
TX_UUIDS: Final[tuple[str, ...]] = (
    gatt.PRIMARY_TX_UUID,
    gatt.DATA_TX_UUID,
    gatt.THIRD_TX_UUID,
    gatt.FOURTH_TX_UUID,
)


class BluezError(RuntimeError):
    """Raised when BlueZ refuses an operation or a required object is missing."""


async def _wait_writable(loop: asyncio.AbstractEventLoop, fd: int) -> None:
    """Park until *fd* is writable. Lifts the closure trap into a top-level fn."""
    fut: asyncio.Future[None] = loop.create_future()

    def _cb() -> None:
        loop.remove_writer(fd)
        if not fut.done():
            fut.set_result(None)

    loop.add_writer(fd, _cb)
    try:
        await fut
    finally:
        with contextlib.suppress(Exception):
            loop.remove_writer(fd)


class BluezTransport(Transport):
    """BLE transport that drives BlueZ via DBus directly.

    Lifecycle::

        async with BluezTransport(address) as transport:
            client = IgpsportClient(transport)
            ...

    Open / close do the following:

    * ``open()`` — find the adapter, locate the ``Device1`` for
      *address*, ``Connect()`` it, wait for service resolution, find
      the four UART characteristics by UUID, call ``AcquireWrite``
      on the control RX char and ``AcquireNotify`` on every TX char.
      Each Acquire returns a Unix FD and the *negotiated* MTU for
      that endpoint; the largest of those MTUs is what
      :meth:`send` uses as the chunk size.
    * ``close()`` — close every FD, ``Disconnect()`` the device.

    The reassembly buffer is shared across all four TX channels: a
    frame can begin on one channel and continue on another if the
    device chooses, though in practice the BSC200 keeps each frame
    on a single channel.
    """

    def __init__(self, address: str, *, adapter: str = "hci0") -> None:
        self._address = address
        self._adapter = adapter
        # DBus state (populated in open()).
        self._bus: object | None = None
        self._device_iface: object | None = None
        # File descriptors and their MTUs returned by Acquire*.
        self._write_fd: int | None = None
        self._write_mtu: int = 23
        self._notify_fds: list[int] = []
        # Inbox: complete reassembled frames.
        self._inbox: asyncio.Queue[bytes | None] = asyncio.Queue()
        self._closed = False
        # Reassembly buffer + expected total. Shared across channels —
        # see class docstring.
        self._rx_buf = bytearray()
        self._rx_expected: int | None = None

    @property
    def address(self) -> str:
        return self._address

    @property
    def mtu(self) -> int:
        return self._write_mtu

    def _register_reader(self, fd: int) -> None:
        """Hook *fd* into the asyncio event loop for readability."""
        loop = asyncio.get_running_loop()

        def _on_readable() -> None:
            try:
                # SOCK_SEQPACKET delivers one notification per recv.
                # 4096 is generous for any BSC200 notification (MTU 247).
                data = os.read(fd, 4096)
            except BlockingIOError:
                return
            except OSError as exc:
                _LOG.debug("BlueZ: read on fd=%d errored: %s", fd, exc)
                loop.remove_reader(fd)
                return
            if not data:
                # EOF: the device disconnected or BlueZ tore down the FD.
                _LOG.debug("BlueZ: fd=%d closed by peer", fd)
                loop.remove_reader(fd)
                return
            self._on_chunk(data)

        loop.add_reader(fd, _on_readable)

    async def open(self) -> None:
        """Connect to BlueZ, discover, acquire MTU-aware FDs."""
        # Lazy import: dbus_fast pulls in a binary extension. Code paths
        # that only use LoopbackTransport (tests) should not pay for it.
        from dbus_fast import BusType  # type: ignore[import-not-found]
        from dbus_fast.aio import MessageBus  # type: ignore[import-not-found]

        # negotiate_unix_fd=True is mandatory — AcquireWrite /
        # AcquireNotify return file descriptors over DBus, and without
        # the FD-passing capability negotiated up front, the bus
        # disconnects when the first FD-bearing reply arrives.
        bus = await MessageBus(bus_type=BusType.SYSTEM, negotiate_unix_fd=True).connect()
        self._bus = bus

        adapter_path = f"/org/bluez/{self._adapter}"
        device_path = f"{adapter_path}/dev_{self._address.replace(':', '_').upper()}"

        # Make sure the device is known to BlueZ. If not, try a short
        # scan to populate it.
        await self._ensure_device_known(bus, adapter_path, device_path)

        device_iface = await self._get_iface(bus, device_path, DEVICE_IFACE)
        self._device_iface = device_iface

        # Connect if not already connected.
        if not await device_iface.get_connected():  # type: ignore[attr-defined]
            await device_iface.call_connect()  # type: ignore[attr-defined]

        # Wait for service resolution. BlueZ exposes the GATT tree
        # asynchronously; ServicesResolved is the canonical "you can
        # start using GATT now" signal.
        await self._wait_services_resolved(device_iface)

        # Walk the GATT tree to find our characteristics by UUID.
        managed = await self._get_managed_objects(bus)
        chars_by_uuid = self._index_chars_by_uuid(managed, device_path)

        rx_path = chars_by_uuid.get(gatt.PRIMARY_RX_UUID)
        if rx_path is None:
            raise BluezError(
                f"control RX characteristic {gatt.PRIMARY_RX_UUID} not exposed by device"
            )

        # AcquireWrite on the control RX. Returns (FD, MTU). The FD is
        # a SOCK_SEQPACKET socket per BlueZ docs; writes go out as ATT
        # Write Commands sized up to MTU.
        rx_iface = await self._get_iface(bus, rx_path, GATT_CHAR_IFACE)
        write_fd, write_mtu = await rx_iface.call_acquire_write({})  # type: ignore[attr-defined]
        # dbus-fast returns a fd handle wrapped in `dbus_fast.signature.Variant`-like
        # object; we duplicate it so closing our side doesn't tug the
        # bus's reference.
        self._write_fd = os.dup(write_fd)
        os.close(write_fd)
        self._write_mtu = int(write_mtu)
        _LOG.info(
            "BlueZ: AcquireWrite on %s -> fd=%d mtu=%d",
            rx_path,
            self._write_fd,
            self._write_mtu,
        )

        # AcquireNotify on every TX characteristic that exists.
        for tx_uuid in TX_UUIDS:
            tx_path = chars_by_uuid.get(tx_uuid)
            if tx_path is None:
                _LOG.debug("BlueZ: skipping unavailable TX %s", tx_uuid)
                continue
            tx_iface = await self._get_iface(bus, tx_path, GATT_CHAR_IFACE)
            try:
                notify_fd, notify_mtu = await tx_iface.call_acquire_notify({})  # type: ignore[attr-defined]
            except Exception as exc:
                _LOG.debug("BlueZ: AcquireNotify on %s failed: %s", tx_path, exc)
                continue
            dup_fd = os.dup(notify_fd)
            os.close(notify_fd)
            self._notify_fds.append(dup_fd)
            _LOG.info(
                "BlueZ: AcquireNotify on %s -> fd=%d mtu=%d",
                tx_path,
                dup_fd,
                notify_mtu,
            )
            # Register the FD with the event loop. BlueZ marks the
            # socket non-blocking, so we use add_reader rather than
            # spawning a thread for a blocking read.
            self._register_reader(dup_fd)

        if not self._notify_fds:
            raise BluezError("no TX notification FDs could be acquired")

    async def __aenter__(self) -> BluezTransport:
        await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        # Stop reading; remove_reader is idempotent.
        loop = asyncio.get_running_loop()
        for fd in self._notify_fds:
            with contextlib.suppress(Exception):
                loop.remove_reader(fd)
            with contextlib.suppress(OSError):
                os.close(fd)
        self._notify_fds.clear()
        if self._write_fd is not None:
            with contextlib.suppress(OSError):
                os.close(self._write_fd)
            self._write_fd = None
        # Disconnect the device (best-effort).
        if self._device_iface is not None:
            with contextlib.suppress(Exception):
                await self._device_iface.call_disconnect()  # type: ignore[attr-defined]
            self._device_iface = None
        # Disconnect the bus.
        if self._bus is not None:
            with contextlib.suppress(Exception):
                self._bus.disconnect()  # type: ignore[attr-defined]
            self._bus = None
        # Wake up any pending receivers.
        await self._inbox.put(None)

    async def send(self, frame: bytes) -> None:
        if self._write_fd is None:
            raise TransportClosed("transport not open")
        # AcquireWrite returns the maximum ATT payload size for each
        # write — already net of the ATT header. The kernel's
        # SOCK_SEQPACKET socket truncates anything larger, so we cap
        # at the negotiated MTU directly (not MTU-3).
        chunk = max(self._write_mtu, 20)
        loop = asyncio.get_running_loop()
        for offset in range(0, len(frame), chunk):
            buf = frame[offset : offset + chunk]
            await self._write_buf(loop, self._write_fd, buf)

    @staticmethod
    async def _write_buf(loop: asyncio.AbstractEventLoop, fd: int, buf: bytes) -> None:
        """Non-blocking write that waits for writability when EAGAIN."""
        while True:
            try:
                written = os.write(fd, buf)
            except BlockingIOError:
                await _wait_writable(loop, fd)
                continue
            if written == len(buf):
                return
            # Short write — keep going with the rest. Rare for
            # SEQPACKET but harmless.
            buf = buf[written:]

    async def receive(self) -> bytes:
        frame = await self._inbox.get()
        if frame is None:
            raise TransportClosed("BlueZ link closed")
        return frame

    # ---- internal helpers ------------------------------------------

    async def _ensure_device_known(self, bus: object, adapter_path: str, device_path: str) -> None:
        """If BlueZ has never seen *address*, do a brief discovery."""
        managed = await self._get_managed_objects(bus)
        if device_path in managed:
            return
        adapter_iface = await self._get_iface(bus, adapter_path, ADAPTER_IFACE)
        with contextlib.suppress(Exception):
            # SetDiscoveryFilter sometimes refuses unknown keys; this
            # placeholder is best-effort, the real discovery still
            # starts below.
            await adapter_iface.call_set_discovery_filter(  # type: ignore[attr-defined]
                {"DuplicateData": False}
            )
        await adapter_iface.call_start_discovery()  # type: ignore[attr-defined]
        try:
            for _ in range(20):  # up to ~6 seconds
                await asyncio.sleep(0.3)
                managed = await self._get_managed_objects(bus)
                if device_path in managed:
                    return
        finally:
            with contextlib.suppress(Exception):
                await adapter_iface.call_stop_discovery()  # type: ignore[attr-defined]
        raise BluezError(
            f"BlueZ never advertised device {self._address}; is it powered on and in range?"
        )

    async def _wait_services_resolved(self, device_iface: object, *, timeout: float = 15.0) -> None:
        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            if await device_iface.get_services_resolved():  # type: ignore[attr-defined]
                return
            await asyncio.sleep(0.2)
        raise BluezError(f"GATT services not resolved within {timeout}s")

    async def _get_iface(self, bus: object, path: str, iface: str) -> object:
        introspection = await bus.introspect(BLUEZ_SERVICE, path)  # type: ignore[attr-defined]
        proxy = bus.get_proxy_object(BLUEZ_SERVICE, path, introspection)  # type: ignore[attr-defined]
        return proxy.get_interface(iface)

    async def _get_managed_objects(self, bus: object) -> dict[str, dict[str, dict]]:
        introspection = await bus.introspect(BLUEZ_SERVICE, "/")  # type: ignore[attr-defined]
        proxy = bus.get_proxy_object(BLUEZ_SERVICE, "/", introspection)  # type: ignore[attr-defined]
        om = proxy.get_interface(DBUS_OM_IFACE)
        result = await om.call_get_managed_objects()
        return result  # type: ignore[no-any-return]

    @staticmethod
    def _index_chars_by_uuid(
        managed: dict[str, dict[str, dict]], device_path: str
    ) -> dict[str, str]:
        """Walk the ObjectManager tree and return {char_uuid: object_path}.

        Only includes characteristics whose path is rooted under
        *device_path*, so we ignore characteristics from other devices
        the adapter has paired.
        """
        out: dict[str, str] = {}
        for path, ifaces in managed.items():
            if not path.startswith(device_path):
                continue
            char_props = ifaces.get(GATT_CHAR_IFACE)
            if not char_props:
                continue
            uuid_val = char_props.get("UUID")
            if uuid_val is None:
                continue
            # dbus-fast wraps property values in Variant objects whose
            # .value attribute holds the unmarshalled Python value.
            uuid = getattr(uuid_val, "value", uuid_val)
            if isinstance(uuid, str):
                out[uuid.lower()] = path
        return out

    def _on_chunk(self, data: bytes) -> None:
        """Reassembly loop — identical to BleakTransport._on_notify."""
        self._rx_buf.extend(data)
        while True:
            if self._rx_expected is None:
                if len(self._rx_buf) < framing.HEADER_SIZE:
                    return
                try:
                    self._rx_expected = framing.expected_total_size(
                        bytes(self._rx_buf[: framing.HEADER_SIZE])
                    )
                except framing.FrameError as exc:
                    _LOG.warning("BlueZ: dropping malformed header: %s", exc)
                    self._rx_buf.clear()
                    return
            assert self._rx_expected is not None
            if len(self._rx_buf) < self._rx_expected:
                return
            frame_bytes = bytes(self._rx_buf[: self._rx_expected])
            del self._rx_buf[: self._rx_expected]
            self._rx_expected = None
            self._inbox.put_nowait(frame_bytes)

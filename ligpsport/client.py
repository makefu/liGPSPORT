"""High-level async client for the iGPSPORT BLE protocol.

The :class:`IgpsportClient` is the public entry point. It owns a
:class:`ligpsport.transport.Transport`, runs a single background task
that reads incoming frames and routes them either to a pending
request future or to the unsolicited-notification queue, and exposes
:meth:`request` for one-shot request/response interactions and
:meth:`subscribe` for unsolicited notification streams.

The client deliberately does **not** open or close the underlying
transport — that's the caller's job (typically via the transport's
async context manager). This keeps the client testable with
:class:`ligpsport.transport.LoopbackTransport` without bringing BLE
into the picture, and keeps the BLE-specific lifecycle in one place
(:class:`ligpsport.transport.BleakTransport`).
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import logging
from collections.abc import AsyncIterator
from typing import Final

from google.protobuf.message import Message

from . import envelope, framing
from .transport import Transport, TransportClosed

_LOG = logging.getLogger(__name__)

# Service-level operation enums shared across the protocol. Every
# per-service `.proto` declares its own `OPERATE_TYPE` enum but the
# numeric values for GET/SET/SEND/ADD/DEL line up across services
# (cf. common.proto's SERVICE_OPERATE_TYPE — most services reuse the
# same numbers verbatim).
OP_NONE: Final[int] = 0
OP_SET: Final[int] = 1
OP_GET: Final[int] = 2
OP_SEND: Final[int] = 3
OP_ADD: Final[int] = 4
OP_DEL: Final[int] = 5


class ProtocolError(RuntimeError):
    """Raised when the peer returns an unexpected frame."""


class RequestTimeout(asyncio.TimeoutError):
    """Raised when :meth:`IgpsportClient.request` exceeds its deadline."""


@dataclasses.dataclass(slots=True, frozen=True)
class Response:
    """A frame the peer sent in reply to a request.

    The library prefers to return parsed protobuf messages, but the
    raw frame stays accessible for callers that need it (e.g. for
    PROTOCOL.md captures or the ``raw`` CLI command).
    """

    frame: framing.Frame
    message: Message


class IgpsportClient:
    """Async request/response client over a :class:`Transport`.

    Typical use::

        async with BleakTransport(address) as transport:
            client = IgpsportClient(transport)
            await client.start()
            version = await client.request(dev_ver_info_pb2.dev_ver_info_msg(...))
            await client.stop()

    Concurrent :meth:`request` calls are serialised on a single
    background read loop. Per-service unsolicited notifications
    (e.g. :data:`OP_SEND` frames from ``DEV_STATUS``) are delivered
    through :meth:`subscribe`.
    """

    def __init__(self, transport: Transport):
        self._transport = transport
        self._reader_task: asyncio.Task[None] | None = None
        # service → list of pending response futures (FIFO).
        self._pending: dict[int, list[asyncio.Future[Response]]] = {}
        self._subscribers: dict[int, list[asyncio.Queue[Response]]] = {}
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        """Begin reading frames from the transport."""
        if self._reader_task is not None:
            return
        self._reader_task = asyncio.create_task(self._read_loop(), name="ligpsport-reader")

    async def stop(self) -> None:
        """Stop the read loop and fail all pending requests."""
        if self._reader_task is None:
            return
        self._reader_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await self._reader_task
        self._reader_task = None
        # Wake up any pending requesters with a clear error.
        for futures in self._pending.values():
            for fut in futures:
                if not fut.done():
                    fut.set_exception(TransportClosed("client stopped"))
        self._pending.clear()

    async def __aenter__(self) -> IgpsportClient:
        await self.start()
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.stop()

    async def request(
        self,
        request_msg: Message,
        *,
        operation: int = OP_GET,
        timeout: float = 5.0,
    ) -> Response:
        """Send *request_msg* and await the next reply on the same service.

        The reply is whatever frame the peer sends back on the same
        ``service_type`` after this request. Unsolicited frames that
        arrive in between are routed to subscribers (or dropped if no
        subscriber exists) — they don't fulfil this future.
        """
        service_type, payload = envelope.encode_message(request_msg)
        frame = framing.Frame(service=service_type, operation=operation, payload=payload)
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Response] = loop.create_future()
        async with self._lock:
            self._pending.setdefault(service_type, []).append(future)
            await self._transport.send(framing.build_frame(frame))
        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except TimeoutError as exc:
            # Remove the future from the pending queue so a late reply
            # doesn't try to fulfil it.
            async with self._lock:
                queue = self._pending.get(service_type, [])
                if future in queue:
                    queue.remove(future)
            raise RequestTimeout(f"no reply for service={service_type} within {timeout}s") from exc

    async def subscribe(self, service_type: int) -> AsyncIterator[Response]:
        """Yield unsolicited frames for *service_type* as they arrive.

        Frames that match a pending :meth:`request` go to that
        request's future instead; only the leftover unsolicited
        frames (e.g. periodic ``DEV_STATUS`` notifications) reach
        subscribers.
        """
        queue: asyncio.Queue[Response] = asyncio.Queue()
        async with self._lock:
            self._subscribers.setdefault(service_type, []).append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            async with self._lock:
                self._subscribers.get(service_type, []).remove(queue)

    async def _read_loop(self) -> None:
        try:
            async for raw in self._transport.frames():
                await self._dispatch(raw)
        except TransportClosed:
            _LOG.debug("transport closed; reader exiting")
        except Exception:
            _LOG.exception("reader loop crashed")
            raise

    async def _dispatch(self, raw: bytes) -> None:
        try:
            frame = framing.parse_frame(raw)
        except framing.FrameError:
            _LOG.warning("dropping malformed frame: %d bytes", len(raw))
            return
        try:
            message = envelope.decode_payload(frame.service, frame.payload)
        except envelope.UnknownServiceError:
            _LOG.warning("dropping frame for unknown service=%d", frame.service)
            return
        response = Response(frame=frame, message=message)
        async with self._lock:
            queue = self._pending.get(frame.service)
            if queue:
                fut = queue.pop(0)
                fut.set_result(response)
                return
            subscribers = list(self._subscribers.get(frame.service, ()))
        # Fanout outside the lock to avoid holding it during put().
        for sub in subscribers:
            await sub.put(response)

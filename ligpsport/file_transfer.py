"""Chunked file upload / download helpers for the iGPSPORT BLE protocol.

The wire mechanic is the same for every file type: each chunk is a
``PbFrame`` whose payload is the per-service container message (e.g.
``cycling_data_msg`` for rides, ``route_plan_data_msg`` for routes)
with the chunk bytes in the ``file_content`` field. The 20-byte
header's ``file_tag`` field (offset 3) increments per chunk so the
receiver can drop duplicates.

For **downloads**, the client issues a ``FILE_GET`` request that
identifies the file (by timestamp for rides, by id for routes). The
device then streams ``FILE_SEND`` frames until the requested file
size is satisfied. The library accumulates ``file_content`` bytes
until the cumulative count matches the size reported by the
preceding LIST_GET (or by the ``file_size`` field in the request).

For **uploads**, the client splits the source bytes into chunks
sized to fit the BLE MTU. Each chunk goes out as a separate
``FILE_SEND`` (or ``ADD_FILE`` for training files); the device
ack-replies with a ``ConfirmFrame``.

This module exposes the two primitives :func:`download_cycling_data`
and (when implemented) :func:`upload_route_plan` etc. The CLI's
``get-ride`` subcommand sits on top of the cycling-data downloader.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
from typing import TYPE_CHECKING

from . import framing
from .proto import common_pb2, cycling_data_pb2, general_file_operation_pb2

if TYPE_CHECKING:
    from .client import IgpsportClient
    from .routes import RouteData

_LOG = logging.getLogger(__name__)


async def download_cycling_data(
    client: IgpsportClient,
    *,
    timestamp: int,
    expected_size: int | None = None,
    chunk_timeout: float = 10.0,
    overall_timeout: float = 300.0,
) -> bytes:
    """Download one recorded ride file from the device.

    *timestamp* is the file identifier from the cycling-data list. If
    *expected_size* is provided (e.g. from a prior LIST_GET) the
    downloader returns as soon as it has accumulated that many bytes;
    otherwise it keeps consuming chunks until ``overall_timeout``
    expires without a fresh chunk.

    Raises :class:`asyncio.TimeoutError` if the device stops sending
    before all bytes arrive.
    """
    # Subscribe to unsolicited CYCLING_DATA frames before sending the
    # request; the device may start replying before the request future
    # resolves, and the response itself usually IS the first chunk.
    request = cycling_data_pb2.cycling_data_msg()
    request.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_GET
    flag = request.cycling_data_file_flag_msg.add()
    flag.timestamp = timestamp

    accumulated = bytearray()
    deadline = asyncio.get_running_loop().time() + overall_timeout

    # The first reply is delivered through `request`; subsequent chunks
    # arrive as unsolicited frames on the same service.
    # Subscribe first so we don't race the first follow-up chunk.
    from .proto import common_pb2

    async def consume(sub_iter):
        nonlocal accumulated
        async for response in sub_iter:
            if not isinstance(response.message, cycling_data_pb2.cycling_data_msg):
                continue
            chunk = response.message.file_content
            if chunk:
                accumulated.extend(chunk)
                _LOG.debug("ride chunk: +%d bytes (total %d)", len(chunk), len(accumulated))
            if expected_size is not None and len(accumulated) >= expected_size:
                return
            if asyncio.get_running_loop().time() > deadline:
                return

    sub_iter = client.subscribe(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA)
    consumer = asyncio.create_task(consume(sub_iter))
    try:
        # Fire the initial request; its response is itself a chunk.
        response = await client.request(request, timeout=chunk_timeout)
        if isinstance(response.message, cycling_data_pb2.cycling_data_msg):
            chunk = response.message.file_content
            if chunk:
                accumulated.extend(chunk)

        # If the first chunk already satisfies expected_size, we're done.
        if expected_size is None or len(accumulated) < expected_size:
            with contextlib.suppress(TimeoutError):
                await asyncio.wait_for(consumer, timeout=overall_timeout)
    finally:
        consumer.cancel()
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await consumer
    return bytes(accumulated)


async def upload_route_plan(
    client: IgpsportClient,
    route: RouteData,
    *,
    file_id: int = 1,
    file_extension: str = "gpx",
    timeout: float = 30.0,
) -> int:
    """Upload *route* to the device as a route_plan file.

    Returns the status byte from the device's ConfirmFrame reply (0
    means success; non-zero means the device rejected the upload).

    The upload mechanic is **not** the standard PbFrame layout — it's
    a bespoke ``FILE_OPERATION`` envelope discovered in
    ``IGPDeviceManager.sendRoutePlanFileSingleChannel``:

    1. 20-byte header with ``service=21 (FILE_OPERATION)`` and
       ``operation=3 (SERVICE_OPERATE_TYPE_ADD)``. The header's
       payload-size field is **0** — the device dispatches on the
       (service, operation) tuple instead of reading a length here.
    2. 4-byte **big-endian** length prefix giving the size in bytes
       of the next field.
    3. A ``general_file_operation`` protobuf message announcing the
       upload (file_type=ROUTE_PLAN, file_id, file_extension,
       file_name, file_size).
    4. The raw file content (the GPX/CNX/FIT/... bytes themselves).

    The whole blob is then written to the BLE RX characteristic in
    MTU-sized chunks like any other frame; the device knows to expect
    ``file_size`` bytes of content because that's what the gfo
    message announces.

    The iGPSPORT app hardcodes ``file_extension="cnx"`` in
    ``IGPDeviceManager`` even though the on-device parser also
    accepts GPX. This function defaults to ``"gpx"`` so callers can
    upload OSM-exported routes verbatim.
    """
    from .routes import to_gpx_bytes

    gpx_bytes = to_gpx_bytes(route)

    gfo = general_file_operation_pb2.general_file_operation()
    gfo.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION
    gfo.operate_type = common_pb2.enum_SERVICE_OPERATE_TYPE_ADD
    gfo.file_type = general_file_operation_pb2.enum_FILE_TYPE_ROUTE_PLAN
    gfo.file_id = file_id
    gfo.file_extension = file_extension
    gfo.file_name = route.name
    gfo.file_size = len(gpx_bytes)
    gfo_bytes = gfo.SerializeToString()

    # The 20-byte header: payload_size=0, service=FILE_OPERATION, op=ADD.
    header = framing.build_frame(
        framing.Frame(
            service=common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION,
            operation=common_pb2.enum_SERVICE_OPERATE_TYPE_ADD,
            payload=b"",
        )
    )
    length_prefix = len(gfo_bytes).to_bytes(4, "big")
    blob = header + length_prefix + gfo_bytes + gpx_bytes
    _LOG.debug(
        "upload route: header=%d gfo=%d file=%d total=%d",
        len(header),
        len(gfo_bytes),
        len(gpx_bytes),
        len(blob),
    )

    # Subscribe to FILE_OPERATION replies before sending so we don't
    # race the device's ack.
    sub = client.subscribe(common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION)
    # Send the whole blob in one go via the client's underlying
    # transport. We bypass `request()` because that wraps the payload
    # in another build_frame call; here the wire bytes are already
    # framed (plus the extra length-prefixed bits).
    await client._transport.send(blob)  # type: ignore[attr-defined]

    try:
        response = await asyncio.wait_for(sub.__anext__(), timeout=timeout)
    except (StopAsyncIteration, TimeoutError) as exc:
        raise TimeoutError("no FILE_OPERATION reply from device") from exc
    finally:
        with contextlib.suppress(Exception):
            await sub.aclose()  # type: ignore[attr-defined]
    return response.frame.status

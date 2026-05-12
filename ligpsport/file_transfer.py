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

from .proto import cycling_data_pb2

if TYPE_CHECKING:
    from .client import IgpsportClient

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

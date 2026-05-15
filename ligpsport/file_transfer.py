"""Chunked file upload / download helpers for the iGPSPORT BLE protocol.

For **downloads** (e.g. recorded ride files), the client issues a
``FILE_GET`` request that identifies the file (by timestamp for rides,
by id for routes). The device then streams ``FILE_SEND`` frames until
the requested file size is satisfied. The library accumulates
``file_content`` bytes until the cumulative count matches the size
reported by the preceding LIST_GET (or by the ``file_size`` field in
the request).

For **route uploads** (``upload_route_plan``), the protocol is a
two-characteristic chunked stream — *not* the standard PbFrame layout
the read commands use. The mechanic was reverse-engineered from
``IGPDeviceManager.sendRoutePlanFile`` in the iGPSPORT Android APK
(line range 24586-24996 of the c4 smali); the byte-level spec lives
in ``docs/PROTOCOL.md`` §7. Summary, per chunk:

1. Build a ``route_plan_data_msg`` protobuf with the file metadata
   (id, name, type, total distance) and ``file_content = <chunk>``.
   Serialise to ``sendData`` — **raw protobuf bytes**, no 20-byte
   header.
2. Build a 20-byte ``confirmData`` header (same shape as a
   :class:`framing.Frame` PbFrame for ROUTE_PLAN / FILE_SEND) with
   ``payload_size = len(sendData)``, a CRC8 over ``sendData`` at
   offset 9, and an ``endType`` byte at offset 10 — ``2`` for every
   chunk except the last, ``3`` for the last chunk. The CRC at
   offset 19 covers bytes 0..18.
3. Write ``sendData`` to the **data** characteristic (the
   ``…-9e`` UART, called ``mRxCharacteristic`` in the smali) for
   generation-1/2 devices, or to the **fourth** characteristic
   (``…-6e``) for generation-3+ devices.
4. Write ``confirmData`` to the **control** characteristic
   (``…-8e``).
5. Wait for the device's ACK on the notify side: a 20-byte
   :class:`framing.Frame` with ``service=ROUTE_PLAN``,
   ``operation=FILE_SEND``, and a ``status`` byte at offset 7.
   The byte is a ``DeviceReturnStatus`` ordinal (see
   :data:`_STATUS_NAMES`):
   * ``status=0`` (Success) → advance to next chunk; on the *last*
     chunk this means the upload is complete.
   * ``status=4`` (QuantityIsFull) → the device terminates early
     (queue drained); also treat as success.
   * any other status → device rejected the upload. The library
     raises :class:`RouteUploadError`. The BSC200's firmware
     returns ``status=1`` (DataError) for every chunk when the
     content is not in CNX format — see PROTOCOL.md §7.1.

6. After all chunks have been ACKed, issue a single ``FILE_USE``
   command (operation=5) with no ``file_content`` to commit the
   upload. Same two-write pattern (data + control). Mirrors
   ``setRoutePlanFile`` in the smali, which the app always invokes
   after a successful ``sendRoutePlanFile``.

This module exposes :func:`download_cycling_data` and
:func:`upload_route_plan`. The CLI's ``get-ride`` and
``upload-route`` subcommands sit on top of them.
"""

from __future__ import annotations

import asyncio
import dataclasses
import logging
import math
import struct
from typing import TYPE_CHECKING, Final

from . import client as _client_module
from . import framing
from .proto import common_pb2, cycling_data_pb2, route_plan_pb2

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .client import IgpsportClient
    from .cnx import Waypoint
    from .routes import RouteData
    from .transport import Channel

_LOG = logging.getLogger(__name__)

# Per-chunk endType byte (offset 10 of confirmData). Source:
# `sendRoutePlanFile` smali line 24846-24851 (`const/4 v2, 3` / `const/4 v2, 2`).
_END_TYPE_CONTINUE: Final[int] = 2  # not the last chunk
_END_TYPE_LAST: Final[int] = 3  # last chunk

# Device-reply status byte (offset 7 of the ACK ConfirmFrame). Source:
# `com.igpsport.blelib.DeviceReturnStatus` enum. Maps the device's
# generic "command outcome" byte:
#
#   0 = Success
#   1 = DataError                   ← rejection (e.g. wrong file format)
#   2 = MemoryError
#   3 = LowBattery
#   4 = QuantityIsFull / DoneEarly  ← for route-plan FILE_SEND this also
#                                     means "queue cleanup, stop"
#   5 = IsBeingUsed
#   6 = UnsupportedCommand
#   ... (full table in PROTOCOL.md §7)
#
# For chunked route uploads the receive handler treats status=0 +
# isLastPack as "done" (success). status=4 is "early done / queue
# drained". Every other value (including the BSC200's persistent
# status=1) is a device-side rejection that the app's
# `checkIsFinish` would raise as `DeviceReturnsErrorCode` and
# retry; the library surfaces it as :class:`RouteUploadError`.
_STATUS_OK: Final[int] = 0
_STATUS_DATA_ERROR: Final[int] = 1
_STATUS_DONE_EARLY: Final[int] = 4

# Filename length limit by device name. Source: `sendRoutePlanFile`
# smali line 24648-24705 — BSC200 falls in the 60-byte group with
# BSC300, iGS320 variants and iGS630.
_FILENAME_MAX_BY_DEVICE: Final[dict[str, int]] = {
    "BSC200": 60,
    "BSC300": 60,
    "iGS320": 60,
    "iGS320-": 60,
    "iGS320-V2": 60,
    "iGS630": 60,
    "iGS620": 28,
    "iGS520": 50,
}
_FILENAME_MAX_DEFAULT: Final[int] = 40

# Default chunk size when the device has not reported a sendFileMtuSize.
# Source: `DeviceInfoHelper.getDeviceInfo` smali fallback table — gen-3
# computers (iGS520/iGS320/iGS50S/iGS10S) use 512; gen-2/4 use 4096.
# 512 is the safe default for an unknown gen-3 device.
_DEFAULT_CHUNK_SIZE: Final[int] = 512

# Protobuf enum values, mirrored here so the upload code stays
# self-contained even if the generated module's enum aliasing changes.
_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND: Final[int] = (
    route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND
)
_ROUTE_PLAN_FILE_TYPE_BY_EXT: Final[dict[str, int]] = {
    "cnx": route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_CNX,
    "gpx": route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_GPX,
    "fit": route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_FIT,
    "tcx": route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_TCX,
    "xml": route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_XML,
}


# Friendly names for the device-status byte. Keeps error messages
# readable; the integer is still authoritative.
#
# Source: `com.igpsport.blelib.DeviceReturnStatus` smali enum init
# (DeviceReturnStatus.smali line 145-260). The first 7 entries map
# directly (ordinal == wire byte); the Wifi block jumps to 16-23 and
# the Navigation block to 65-66. We had values 7-16 wrong in earlier
# releases — verified against snoop_start.log where a FILE_USE for a
# not-yet-uploaded route returns status byte 0x42 = 66 =
# NavigationRouteDoesNotExist.
_STATUS_NAMES: Final[dict[int, str]] = {
    0: "Success",
    1: "DataError",
    2: "MemoryError",
    3: "LowBattery",
    4: "QuantityIsFull",
    5: "IsBeingUsed",
    6: "UnsupportedCommand",
    16: "WifiConnectionSucceeded",
    17: "WifiWrongPassword",
    18: "WifiConnectionTimedOut",
    19: "WifiNotConnected",
    20: "WifiPleaseEnterPassword",
    21: "WifiMapDownload",
    22: "WifiFirmwareDownload",
    23: "WifiCyclingActivityIsUploading",
    65: "NavigationRouteDeletionFailed",
    66: "NavigationRouteDoesNotExist",
}


def _status_name(status: int) -> str:
    return _STATUS_NAMES.get(status, f"unknown({status})")


class RouteUploadError(RuntimeError):
    """Raised when the BSC200 rejects a route-plan upload chunk.

    The device's status byte is the ``DeviceReturnStatus`` ordinal
    (see :data:`_STATUS_NAMES`). status=1 ("DataError") is the most
    common rejection — the BSC200 firmware only accepts CNX-format
    route files; uploading raw GPX yields a persistent DataError on
    every chunk. PROTOCOL.md §7 has the details.
    """

    def __init__(self, status: int, chunk_index: int, total_chunks: int):
        super().__init__(
            f"device rejected route upload chunk {chunk_index}/{total_chunks} "
            f"with status={status} ({_status_name(status)})"
        )
        self.status = status
        self.status_name = _status_name(status)
        self.chunk_index = chunk_index
        self.total_chunks = total_chunks


class NavigationStartError(RuntimeError):
    """Raised when the device refuses a FILE_USE (start-navigation) request.

    The upload itself succeeded — the device has the file — but the
    follow-up ``ROUTE_PLAN FILE_USE`` returned a non-success
    ``DeviceReturnStatus``. The route stays on the device's file list
    and can be activated later (e.g. via the on-device UI or a
    retried FILE_USE). PROTOCOL.md §7.2 has the wire-level details.
    """

    def __init__(self, status: int, file_id: int):
        super().__init__(
            f"device refused FILE_USE for file_id={file_id} with "
            f"status={status} ({_status_name(status)})"
        )
        self.status = status
        self.status_name = _status_name(status)
        self.file_id = file_id


@dataclasses.dataclass(slots=True, frozen=True)
class ActivityDownload:
    """Result of an activity ``FILE_GET`` exchange.

    *file_size* is the size declared in the device's embedded
    ``file_download`` protobuf (PROTOCOL.md §6.4); it matches the
    ``file_size`` reported by the preceding ``LIST_GET`` entry.
    *file_id* and *file_name* are usually 0 / "" — the BSC200
    firmware doesn't populate them.
    """

    content: bytes
    file_size: int
    file_id: int
    file_name: str


async def download_cycling_data(
    client: IgpsportClient,
    *,
    timestamp: int,
    expected_size: int | None = None,
    chunk_timeout: float = 10.0,
    overall_timeout: float = 300.0,
) -> bytes:
    """Download one recorded activity file from the device (FIT bytes).

    Thin wrapper around :func:`download_activity` for callers that only
    want the file content. *expected_size* is accepted for backwards
    compatibility but ignored — the embedded ``file_download`` protobuf
    carries the authoritative length, and the transmit-complete
    framing path always returns a complete file or raises.
    """
    del expected_size  # tolerated for backwards compat; size comes from device
    result = await download_activity(
        client,
        timestamp=timestamp,
        timeout=max(overall_timeout, chunk_timeout),
    )
    return result.content


async def download_activity(
    client: IgpsportClient,
    *,
    timestamp: int,
    timeout: float = 60.0,
) -> ActivityDownload:
    """Download one recorded activity by *timestamp*.

    Mirrors ``IGPDeviceManager.readActivityFitFile`` (smali line
    1424-1450) for gen-4 devices like the BSC200:

    1. Build a ``cycling_data_msg`` with ``FILE_GET`` + one
       ``cycling_data_file_flag_message`` carrying the timestamp.
    2. Wrap the serialised protobuf in a 20-byte head with
       ``file_tag = 0x55`` (the ``TransmitCompleteCommand`` magic
       from the smali — without it the BSC200 silently ignores the
       request).
    3. Single merged write of ``(head ‖ body)`` to the **third UART
       RX** (``…-7e``) — verified against btsnoop frame 35365 of
       ``snoop_start.log`` and live tests against firmware 2024-05-14.
    4. The device replies with a single transmit-complete PbFrame on
       the third TX: ``[20B head, file_tag=0x55, end_marker=0x03] ‖
       [4B BE pb_size] ‖ [file_download protobuf] ‖ [file_size
       bytes of FIT]``. The 20-byte head's ``payload_size`` field is
       bogus on this firmware (0x07a7 = 1959 for a 15572-byte file);
       the embedded protobuf is authoritative. The reassembly path
       in :func:`framing.transmit_complete_total_size` already
       handles this; we just consume the resulting Frame here.

    Raises :class:`asyncio.TimeoutError` if no reply arrives within
    *timeout* seconds. Raises :class:`ProtocolError` if the response
    head doesn't look like a FILE_SEND reply.
    """
    pb = cycling_data_pb2.cycling_data_msg()
    pb.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA
    pb.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_GET
    flag = pb.cycling_data_file_flag_msg.add()
    flag.timestamp = timestamp
    body = pb.SerializeToString()
    head = _build_cycling_data_head(
        body,
        op=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_GET,
        file_tag=framing.FILE_TAG_TRANSMIT_COMPLETE,
    )
    wire = head + body

    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA)
    try:
        await client._transport.send(wire, channel="third")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA, queue)

    frame = response.frame
    if frame.operation != cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_SEND:
        raise _client_module.ProtocolError(
            f"activity FILE_GET: expected FILE_SEND reply, got op={frame.operation}"
        )
    payload = frame.payload
    if len(payload) < 4:
        raise _client_module.ProtocolError(
            f"activity FILE_GET: reply payload too short ({len(payload)} bytes)"
        )
    pb_size = struct.unpack(">I", payload[:4])[0]
    if len(payload) < 4 + pb_size:
        raise _client_module.ProtocolError(
            f"activity FILE_GET: pb_size={pb_size} exceeds payload ({len(payload)})"
        )
    from .proto import file_download_pb2

    info = file_download_pb2.file_download()
    info.ParseFromString(payload[4 : 4 + pb_size])
    file_start = 4 + pb_size
    file_end = file_start + info.file_size
    if len(payload) < file_end:
        raise _client_module.ProtocolError(
            f"activity FILE_GET: short payload {len(payload)} < {file_end}"
        )
    return ActivityDownload(
        content=bytes(payload[file_start:file_end]),
        file_size=int(info.file_size),
        file_id=int(info.file_id),
        file_name=str(info.file_name),
    )


@dataclasses.dataclass(slots=True, frozen=True)
class ActivityListEntry:
    """One entry in a ``CYCLING_DATA`` LIST_GET reply."""

    timestamp: int
    file_size: int
    user_id: str
    device_id: str


async def list_activities(
    client: IgpsportClient,
    *,
    file_index_start: int = 0,
    file_index_end: int = 100,
    timeout: float = 10.0,
) -> tuple[ActivityListEntry, ...]:
    """Return the device's recorded-activity list.

    Sends ``CYCLING_DATA LIST_GET`` (op=1) with an inclusive index
    range. The smali for gen-4 devices populates a ``file_list_get_msg``
    with start/end values; mirrors ``ROUTE_PLAN LIST_GET``'s expected
    range argument. The BSC200 firmware ignores values outside the
    range but returns all entries when the range covers the whole
    list. Default ``[0, 100]`` is well above the firmware's
    ``file_list_support_num_max`` cap of 20.

    Sent on the **third UART RX** (``…-7e``) — the iGPSPORT app's
    smali (``IGPDeviceManager.readActivityList``) routes
    ``thirdQueue`` for generation ≥ 3, and the btsnoop capture
    (``snoop_start.log`` frame 35365) confirms the wire path.
    """
    pb = cycling_data_pb2.cycling_data_msg()
    pb.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA
    pb.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET
    pb.list_msg.file_index_start = file_index_start
    pb.list_msg.file_index_end = file_index_end
    body = pb.SerializeToString()
    head = _build_cycling_data_head(
        body,
        op=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET,
        file_tag=framing.FILE_TAG_DEFAULT,
    )
    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA)
    try:
        await client._transport.send(head + body, channel="third")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA, queue)
    msg = response.message
    if not isinstance(msg, cycling_data_pb2.cycling_data_msg):
        raise _client_module.ProtocolError(f"unexpected response message: {type(msg).__name__}")
    return tuple(
        ActivityListEntry(
            timestamp=int(f.timestamp),
            file_size=int(f.file_size),
            user_id=str(f.user_id),
            device_id=str(f.device_id),
        )
        for f in msg.cycling_data_file_flag_msg
        # The BSC200 firmware pads the response with zero entries
        # (timestamp=0, file_size=0) up to the list_support_num_max
        # cap. Drop those so callers see real entries only.
        if f.timestamp != 0 or f.file_size != 0
    )


async def delete_activity(
    client: IgpsportClient,
    timestamp: int,
    *,
    timeout: float = 10.0,
) -> int:
    """Delete one activity file from the device by ``timestamp``.

    Mirrors ``IGPDeviceManager.deleteActivityFitFile`` (smali line
    6464+) for gen-4 devices: builds a ``cycling_data_msg`` with
    ``FILE_DEL`` (op=5) and one
    ``cycling_data_file_flag_message`` carrying the timestamp; for
    gen ≥ 3 the smali pushes onto ``thirdQueue`` — the **third UART
    RX** (``…-7e``), same channel as LIST_GET and FILE_GET.

    For gen-4 specifically, the smali calls
    ``byteMerger(dataPair.second, dataPair.first)`` so the head and
    body go out as a **single merged write**; pre-gen-4 splits them
    body-on-data + header-on-control. The merged-write pattern
    matches the route_plan ``FILES_DEL`` path we already exercise.

    The device replies with a ``CYCLING_DATA FILE_DEL`` confirm
    frame; the status byte at offset 7 is the
    ``DeviceReturnStatus`` ordinal (0 = success).

    **Destructive — never call this without explicit user
    confirmation.** The on-device flash entry for the activity is
    erased and not recoverable.
    """
    pb = cycling_data_pb2.cycling_data_msg()
    pb.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA
    pb.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL
    flag = pb.cycling_data_file_flag_msg.add()
    flag.timestamp = timestamp
    body = pb.SerializeToString()
    head = _build_cycling_data_head(
        body,
        op=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL,
        file_tag=framing.FILE_TAG_DEFAULT,
    )
    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA)
    try:
        await client._transport.send(head + body, channel="third")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA, queue)
    return int(response.frame.status)


async def delete_all_activities(
    client: IgpsportClient,
    *,
    timeout: float = 10.0,
) -> int:
    """Delete *every* recorded activity from the device. **Destructive.**

    Mirrors ``IGPDeviceManager.deleteAllActivityFitFile`` (smali line
    6742+): unlike ``FILE_DEL`` (which gen-4 sends as a merged
    ``byteMerger(header ‖ body)`` write on the third UART), ALL_DEL
    uses the **split** write pattern even on gen-4. ``BaseCommand``
    is constructed with ``sendData = body`` and
    ``confirmData = header``; ``BaseCommand.run`` writes the body on
    the chosen characteristic and the lambda follow-up writes the
    20-byte head on the control channel. Mirror that wire pattern:

    1. Write the body (a minimal ``cycling_data_msg`` with
       ``operate_type = ALL_DEL``) to the third UART RX (``…-7e``).
    2. Write the 20-byte head (service=CYCLING_DATA, op=ALL_DEL) to
       the control UART RX (``…-8e``).

    The device replies with a ``ConfirmFrame`` whose status byte at
    offset 7 is the ``DeviceReturnStatus`` ordinal. The BSC200 may
    silently keep an activity that's still considered open by the
    firmware — see PROTOCOL.md §7.5 / §7.4 for the active-file
    protection pattern. Callers should re-list afterwards.
    """
    pb = cycling_data_pb2.cycling_data_msg()
    pb.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA
    pb.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL
    body = pb.SerializeToString()
    head = _build_cycling_data_head(
        body,
        op=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL,
        file_tag=framing.FILE_TAG_DEFAULT,
    )
    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA)
    try:
        # Live BSC200 (gen 4, fw 2024-05-14) accepts only the merged
        # ``(head ‖ body)`` pattern on the third UART here — the
        # smali's nominal split-write recipe yields ``status=1``
        # (DataError) instead. Verified by replaying both wire
        # variants back-to-back via ``tmp/probe_del.py``: merged
        # acks; split rejects.
        await client._transport.send(head + body, channel="third")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA, queue)
    return int(response.frame.status)


def _build_cycling_data_head(body: bytes, *, op: int, file_tag: int) -> bytes:
    """Build a 20-byte PbFrame head for a CYCLING_DATA service request.

    The captured wire (snoop_start.log frame 35365) and the smali both
    set the head's operation byte to the protobuf's
    ``cycling_data_operate_type`` value (not OP_GET = 2). Pass it
    explicitly here so each caller can name its own op.
    """
    size = len(body)
    h = bytearray(framing.HEADER_SIZE)
    h[framing.HDR_TYPE] = framing.TYPE_PB
    h[framing.HDR_SERVICE] = common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA & 0xFF
    h[framing.HDR_SUB_SERVICE] = 0xFF
    h[framing.HDR_FILE_TAG] = file_tag & 0xFF
    h[framing.HDR_OPERATION] = op & 0xFF
    h[framing.HDR_SUB_OPERATION] = 0xFF
    h[framing.HDR_RESERVED_6] = 0xFF
    h[framing.HDR_PAYLOAD_SIZE] = (size >> 8) & 0xFF
    h[framing.HDR_PAYLOAD_SIZE + 1] = size & 0xFF
    h[framing.HDR_PAYLOAD_CRC] = framing.crc8(body)
    h[framing.HDR_END_MARKER] = framing.TYPE_PB
    for off in range(11, 19):
        h[off] = 0xFF
    h[framing.HDR_HEADER_CRC] = framing.crc8(bytes(h[:19]))
    return bytes(h)


def _truncate_filename(name: str, device_name: str | None) -> str:
    """Clip *name* to the device's UTF-8 byte limit.

    Mirrors the iGPSPORT app: encode to UTF-8, truncate by byte count,
    decode with ``errors="replace"``, then strip the replacement
    character so the result always ends on a complete codepoint.
    Source: `sendRoutePlanFile` smali 24711-24725.
    """
    limit = _FILENAME_MAX_BY_DEVICE.get(device_name or "", _FILENAME_MAX_DEFAULT)
    encoded = name.encode("utf-8")
    if len(encoded) <= limit:
        return name
    clipped = encoded[:limit].decode("utf-8", errors="replace")
    return clipped.replace("�", "")


def _build_route_plan_chunk_pb(
    *,
    file_id: int,
    file_extension: str,
    file_name: str,
    chunk: bytes,
    total_distance: int,
    longitude_start: float = 0.0,
    latitude_start: float = 0.0,
) -> bytes:
    """Build the protobuf body for one route-plan upload chunk.

    Mirrors `RoutePlanServiceFactory.getMessage` (smali 188-325):
    every chunk repeats the full metadata (id, name, file_type,
    total_distance, line_id, start lon/lat) and carries the chunk
    bytes in ``file_content``.
    """
    msg = route_plan_pb2.route_plan_data_msg()
    msg.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN
    msg.route_plan_operate_type = _ROUTE_PLAN_OPERATE_TYPE_FILE_SEND
    msg.line_id.append(f"{file_id}.{file_extension}")
    info = msg.route_plan_info_msg.add()
    info.id = file_id
    info.file_type = _ROUTE_PLAN_FILE_TYPE_BY_EXT.get(
        file_extension.lower(),
        route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_INVALID,
    )
    info.name = file_name
    info.total_distance = max(0, int(total_distance))
    info.longitude_start = float(longitude_start)
    info.latitude_start = float(latitude_start)
    msg.file_content = chunk
    return bytes(msg.SerializeToString())


def _build_route_plan_confirm_header(send_data: bytes, *, end_type: int) -> bytes:
    """Build the 20-byte confirm header for one route-plan upload chunk.

    Mirrors `BaseFactory.confirmCommandByteArray` (smali 112-185)
    parameterised for ROUTE_PLAN / FILE_SEND:

    * offset 0  : 0x01 (END_TYPE_PB literal)
    * offset 1  : service = ROUTE_PLAN ordinal = 7
    * offset 4  : operation = FILE_SEND.getNumber() = 4
    * offsets 7-8: BE u16 = len(send_data)
    * offset 9  : CRC8(send_data)
    * offset 10 : *end_type* (2 = continue, 3 = last)
    * offsets 11-18: 0xFF padding
    * offset 19 : CRC8(bytes 0..18)
    """
    if end_type not in (_END_TYPE_CONTINUE, _END_TYPE_LAST):
        raise ValueError(f"end_type must be 2 or 3, got {end_type}")
    size = len(send_data)
    if size > 0xFFFF:
        raise ValueError(f"chunk too large for u16 size field: {size} bytes")

    header = bytearray(framing.HEADER_SIZE)
    header[framing.HDR_TYPE] = framing.TYPE_PB
    header[framing.HDR_SERVICE] = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN & 0xFF
    header[framing.HDR_SUB_SERVICE] = 0xFF
    header[framing.HDR_FILE_TAG] = 0xFF
    header[framing.HDR_OPERATION] = _ROUTE_PLAN_OPERATE_TYPE_FILE_SEND & 0xFF
    header[framing.HDR_SUB_OPERATION] = 0xFF
    header[framing.HDR_RESERVED_6] = 0xFF
    header[framing.HDR_PAYLOAD_SIZE] = (size >> 8) & 0xFF
    header[framing.HDR_PAYLOAD_SIZE + 1] = size & 0xFF
    header[framing.HDR_PAYLOAD_CRC] = framing.crc8(send_data)
    header[framing.HDR_END_MARKER] = end_type
    for off in range(11, 19):
        header[off] = 0xFF
    header[framing.HDR_HEADER_CRC] = framing.crc8(bytes(header[: framing.HDR_HEADER_CRC]))
    return bytes(header)


def _route_chunks(data: bytes, chunk_size: int) -> list[bytes]:
    """Split *data* into ``chunk_size``-byte slices (last may be short)."""
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive: {chunk_size}")
    if not data:
        # Empty payload still needs one (empty) chunk so the device sees
        # a terminator. Matches the smali, which always loops at least
        # once on a non-null fileBytes parameter.
        return [b""]
    n = math.ceil(len(data) / chunk_size)
    return [data[i * chunk_size : (i + 1) * chunk_size] for i in range(n)]


def _build_file_use_pb(
    *,
    file_id: int,
    file_extension: str,
    name: str | None = None,
    total_distance: int = 0,
) -> bytes:
    """Build a route_plan_data_msg with operate_type=FILE_USE.

    Mirrors ``IGPDeviceManager.setRoutePlanFile`` (smali 27391-27430)
    cross-referenced with a btsnoop capture of the live app — the
    captured wire body carries four fields in the nested
    ``route_plan_info_msg``: ``id``, ``file_type``, ``name``,
    ``total_distance``. The smali only wires ``id`` and ``file_type``
    explicitly; ``name`` and ``total_distance`` come from the
    ``RoutePlanData`` constructor's defaults (the file's display
    name and 0 respectively). The BSC200 firmware appears to
    validate the ``name`` field — omitting it yields a malformed
    FILE_USE that the device silently ignores.

    *name* defaults to ``str(file_id)`` (matches the app's behaviour
    for unnamed routes; the capture showed ``name="235679"`` for
    ``file_id=235679``). *total_distance* defaults to 0.
    """
    msg = route_plan_pb2.route_plan_data_msg()
    msg.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN
    msg.route_plan_operate_type = route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE
    msg.line_id.append(f"{file_id}.{file_extension}")
    info = msg.route_plan_info_msg.add()
    info.id = file_id
    info.file_type = _ROUTE_PLAN_FILE_TYPE_BY_EXT.get(
        file_extension.lower(),
        route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_INVALID,
    )
    info.name = name if name is not None else str(file_id)
    info.total_distance = total_distance
    return bytes(msg.SerializeToString())


def _build_file_use_header(send_data: bytes) -> bytes:
    """Standard 20-byte PbFrame header for the FILE_USE protobuf body.

    No ``endType`` quirk — this is a single-frame command, not a
    chunked stream — so byte 10 is the standard ``END_TYPE_PB``
    literal (0x01).
    """
    header = bytearray(framing.HEADER_SIZE)
    header[framing.HDR_TYPE] = framing.TYPE_PB
    header[framing.HDR_SERVICE] = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN & 0xFF
    header[framing.HDR_SUB_SERVICE] = 0xFF
    header[framing.HDR_FILE_TAG] = 0xFF
    header[framing.HDR_OPERATION] = route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE & 0xFF
    header[framing.HDR_SUB_OPERATION] = 0xFF
    header[framing.HDR_RESERVED_6] = 0xFF
    size = len(send_data)
    header[framing.HDR_PAYLOAD_SIZE] = (size >> 8) & 0xFF
    header[framing.HDR_PAYLOAD_SIZE + 1] = size & 0xFF
    header[framing.HDR_PAYLOAD_CRC] = framing.crc8(send_data)
    header[framing.HDR_END_MARKER] = framing.TYPE_PB
    for off in range(11, 19):
        header[off] = 0xFF
    header[framing.HDR_HEADER_CRC] = framing.crc8(bytes(header[: framing.HDR_HEADER_CRC]))
    return bytes(header)


async def _send_file_use(
    client: IgpsportClient,
    *,
    file_id: int,
    file_extension: str,
    generation: int,
    timeout: float,
    name: str | None = None,
    total_distance: int = 0,
    existing_queue: asyncio.Queue[object] | None = None,
) -> int:
    """Send a ``ROUTE_PLAN FILE_USE`` and return the device's status byte.

    Mirrors ``IGPDeviceManager.setRoutePlanFile`` (smali 27391) and
    validated against a live btsnoop capture of the iGPSPORT app's
    "Start navigation" tap on the BSC200 (``docs/PROTOCOL.md`` §7.2).
    The captured wire format is **a single write of header || body to
    the fourth characteristic** (``…-6e``, channel 4) — not the
    two-channel split (body to data + header to control) used by the
    chunked FILE_SEND path. The smali bears this out: for
    ``getGeneration() == 4`` (the BSC200 in current firmware, despite
    early docs treating it as gen 3) ``setRoutePlanFile`` calls
    ``StringUtils.byteMerger(pair.second, pair.first)`` to glue
    header + body together, and the post-write lambda
    (``send$lambda-135``) skips the control-channel follow-up. For
    legacy gen-3 devices the helper falls back to the
    two-channel split.

    *name* / *total_distance* land in the nested
    ``route_plan_info_msg``. The BSC200 firmware silently drops a
    FILE_USE that omits them; the capture shows the app populating
    ``name=str(file_id)`` and ``total_distance=0`` for unnamed routes.

    *existing_queue* lets the chunked-upload path reuse its already-
    open ROUTE_PLAN subscription so the FILE_USE reply doesn't race
    a fresh subscriber registration.

    Returns the device's ``DeviceReturnStatus`` wire byte (0 =
    Success; 66 = NavigationRouteDoesNotExist = the route file
    isn't on the device yet). Callers decide whether to raise
    :class:`NavigationStartError`.
    """
    use_pb = _build_file_use_pb(
        file_id=file_id,
        file_extension=file_extension,
        name=name,
        total_distance=total_distance,
    )
    use_header = _build_file_use_header(use_pb)
    if existing_queue is None:
        queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN)
        owns_queue = True
    else:
        queue = existing_queue  # type: ignore[assignment]
        owns_queue = False
    try:
        if generation >= 4:
            # Gen-4 path (BSC200, iGS630): single merged write to the
            # fourth characteristic. The smali merger order is
            # ``pair.second + pair.first`` → header + body.
            await client._transport.send(use_header + use_pb, channel="fourth")
        else:
            # Legacy gen-3 path: body on the data-bearing UART, then
            # the 20-byte header on the control UART.
            data_channel: Channel = "fourth" if generation >= 3 else "data"
            await client._transport.send(use_pb, channel=data_channel)
            await client._transport.send(use_header, channel="control")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        if owns_queue:
            await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN, queue)
    status = response.frame.status  # type: ignore[attr-defined]
    _LOG.debug("FILE_USE: status=%d (%s)", status, _status_name(status))
    return int(status)


async def upload_route_plan(
    client: IgpsportClient,
    route: RouteData,
    *,
    file_id: int = 1,
    file_extension: str = "gpx",
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
    generation: int = 4,
    device_name: str | None = None,
    timeout: float = 30.0,
    send_file_use: bool = True,
    start_navigation: bool = False,
    raw_bytes: bytes | None = None,
    raw_name: str | None = None,
    waypoints: Sequence[Waypoint] | None = None,
) -> int:
    """Upload *route* to the device as a route_plan file.

    Returns the final status byte from the device (``0 = Success``
    per ``DeviceReturnStatus``).

    *generation* selects the data-bearing characteristic: gen ≥ 3
    writes chunks to the **fourth** channel (``…-6e``); gen < 3
    writes them to the **data** channel (``…-9e``). BSC200 is gen 3
    by analogy with BSC300/iGS320/iGS520 (it is **not** gen 4 — the
    smali calls ``sendRoutePlanFileSingleChannel`` only for iGS630).
    *device_name* is used to pick the filename-length limit (default
    40 bytes if unknown).

    *send_file_use* controls whether a follow-up ``FILE_USE`` command
    is sent after the last chunk of the **chunked** (FILE_SEND) path
    (mirrors ``setRoutePlanFile`` in the smali — the app always
    issues this to commit the upload). Default: True. Has no effect
    on the FILE_OPERATION CNX path; use *start_navigation* for that.

    *start_navigation*, when True, issues ``FILE_USE`` after a
    successful upload on **either** path (chunked or
    FILE_OPERATION). This is what tells the device to switch its
    active route and enter navigation mode — :class:`NavigationStartError`
    is raised if the device refuses. The upload itself is still
    considered successful when the FILE_USE step fails. Default:
    False (the iGPSPORT app makes nav start opt-in too — its
    ``sendOnly`` flag in ``RoadBookSearchActivity.sendFileToDevice``
    suppresses the FILE_USE call when the user only wants to push a
    file without auto-navigating). See PROTOCOL.md §7.2.

    *raw_bytes* and *raw_name*, if given, bypass the serialisers and
    upload the bytes verbatim. Use this for pre-baked payloads (e.g.
    a CNX file fetched directly from the iGPSPORT cloud's
    ``Routes/DownloadRoutes`` endpoint). When *raw_bytes* is set,
    *route* is still consulted for the start coordinate and distance.

    When *file_extension* is ``"cnx"`` and *raw_bytes* is ``None``,
    *route* is converted to CNX locally via :func:`ligpsport.cnx.to_cnx_bytes`
    — sidesteps the iGPSPORT cloud round-trip the Android app
    requires. *waypoints*, if provided, populate the CNX
    ``<Points>`` list (POIs); only consulted for the CNX path.

    Raises :class:`RouteUploadError` if any chunk's ACK has a status
    byte that isn't ``Success`` (0) or ``QuantityIsFull`` (4 — also
    used as the "done early / queue drained" signal during chunked
    sends). The BSC200 returns ``DataError`` (1) for every chunk
    when the file content is the wrong format — see PROTOCOL.md §7.

    Raises :class:`asyncio.TimeoutError` (the standard one) if a
    chunk's ACK doesn't arrive within *timeout* seconds.
    """
    from .routes import to_gpx_bytes

    ext_lower = file_extension.lower()
    if raw_bytes is not None and ext_lower == "cnx":
        # CNX uploads go via FILE_OPERATION regardless of whether
        # the bytes were locally generated or cloud-fetched.
        source_name = raw_name if raw_name is not None else route.name
        file_name = _truncate_filename(source_name, device_name)
        return await upload_general_file(
            client,
            raw_bytes,
            file_type=FILE_OP_TYPE_ROUTE_PLAN,
            file_id=file_id,
            file_name=file_name,
            file_extension="cnx",
            timeout=timeout,
            start_navigation=start_navigation,
            generation=generation,
        )
    if raw_bytes is not None:
        file_bytes = raw_bytes
        source_name = raw_name if raw_name is not None else route.name
    elif ext_lower == "fit":
        # FIT-encoded Course file. The BSC200 firmware rejects GPX
        # (status=1 = DataError) but the route_plan protobuf
        # enumerates FIT as a valid file_type, so this is one
        # candidate format that might land on the device without
        # the CNX cloud round-trip.
        from .fit_course import to_fit_course_bytes

        file_bytes = to_fit_course_bytes(route)
        source_name = route.name
    elif ext_lower == "cnx":
        # Local GPX→CNX conversion. The BSC200 only parses
        # iGPSPORT's proprietary CNX format; ligpsport.cnx emits
        # bytes that match a captured cloud upload byte-for-byte
        # (see docs/PROTOCOL.md §7.1.2). Live-verified working on
        # BSC200 firmware 2024-05-14 via the FILE_OPERATION ADD
        # service — which is a different wire protocol than the
        # ROUTE_PLAN FILE_SEND path below, so dispatch out early.
        from .cnx import to_cnx_bytes

        file_bytes = to_cnx_bytes(route, waypoints=waypoints or ())
        source_name = raw_name if raw_name is not None else route.name
        file_name = _truncate_filename(source_name, device_name)
        return await upload_general_file(
            client,
            file_bytes,
            file_type=FILE_OP_TYPE_ROUTE_PLAN,
            file_id=file_id,
            file_name=file_name,
            file_extension="cnx",
            timeout=timeout,
            start_navigation=start_navigation,
            generation=generation,
        )
    else:
        file_bytes = to_gpx_bytes(route)
        source_name = route.name
    file_name = _truncate_filename(source_name, device_name)
    chunks = _route_chunks(file_bytes, chunk_size)
    n = len(chunks)
    # First point as the route's start coordinate (the iGPSPORT firmware
    # uses these for the navigation entry icon).
    first = route.points[0] if route.points else None
    lon_start = first.longitude if first is not None else 0.0
    lat_start = first.latitude if first is not None else 0.0
    data_channel: Channel = "fourth" if generation >= 3 else "data"
    _LOG.debug(
        "uploading route '%s' (%d bytes, %d chunks @ %d, gen=%d, channel=%s)",
        file_name,
        len(file_bytes),
        n,
        chunk_size,
        generation,
        data_channel,
    )

    # Subscribe **eagerly** to ROUTE_PLAN replies before sending the
    # first chunk. `client.subscribe` is a lazy generator — its
    # subscriber queue isn't registered with the dispatcher until the
    # first `await __anext__()`. With BlueZ's MTU-247 path the device
    # can ack a chunk before our generator advances that far, and the
    # frame ends up dropped because nobody is listening for the
    # service yet. `open_subscription` registers synchronously.
    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN)
    last_status = -1
    try:
        for i, chunk in enumerate(chunks):
            end_type = _END_TYPE_LAST if i == n - 1 else _END_TYPE_CONTINUE
            send_data = _build_route_plan_chunk_pb(
                file_id=file_id,
                file_extension=file_extension,
                file_name=file_name,
                chunk=chunk,
                total_distance=route.distance_m,
                longitude_start=lon_start,
                latitude_start=lat_start,
            )
            confirm_data = _build_route_plan_confirm_header(send_data, end_type=end_type)
            # The data chunk (raw protobuf bytes) goes on the device's
            # data-bearing UART; the 20-byte trailer always lands on
            # the control UART. This is the same two-write pattern as
            # `IGPDeviceManager.send` + `send$lambda-135` in the smali.
            await client._transport.send(send_data, channel=data_channel)
            await client._transport.send(confirm_data, channel="control")

            response = await asyncio.wait_for(queue.get(), timeout=timeout)
            last_status = response.frame.status
            _LOG.debug(
                "chunk %d/%d (endType=%d): status=%d (%s)",
                i + 1,
                n,
                end_type,
                last_status,
                _status_name(last_status),
            )
            if last_status not in (_STATUS_OK, _STATUS_DONE_EARLY):
                raise RouteUploadError(last_status, i, n)
            if last_status == _STATUS_DONE_EARLY:
                _LOG.debug("device returned status=4 after chunk %d/%d; stopping", i + 1, n)
                break

        if send_file_use or start_navigation:
            # FILE_USE commit: tells the device to switch to the
            # newly uploaded route. The app issues this in
            # `setRoutePlanFile` after every successful
            # `sendRoutePlanFile`. On the BSC200 this is also what
            # actually starts navigation; see PROTOCOL.md §7.2. The
            # device validates the protobuf's `name` field — pass
            # the truncated filename we just uploaded under so the
            # firmware accepts the activation request.
            last_status = await _send_file_use(
                client,
                file_id=file_id,
                file_extension=file_extension,
                generation=generation,
                timeout=timeout,
                name=file_name,
                total_distance=route.distance_m,
                existing_queue=queue,
            )
            if start_navigation and last_status not in (_STATUS_OK, _STATUS_DONE_EARLY):
                raise NavigationStartError(last_status, file_id)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN, queue)
    return last_status


# ---- FILE_OPERATION upload path -------------------------------------
#
# The Android app uploads CNX route bytes via the FILE_OPERATION
# service (21), NOT the ROUTE_PLAN service (7). Mirror of
# ``IGPDeviceManager.sendRoutePlanFileSingleChannel`` (smali 3753-).
# This was verified against a live BSC200 (firmware 2024-05-14) by
# btsnoop capture + replay — see docs/PROTOCOL.md §7.1.2. Without it
# the BSC200 returns ``DataError`` for every chunk on the ROUTE_PLAN
# path, regardless of file content.

# common_pb2 enum mirrors.
_SERVICE_FILE_OPERATION: Final[int] = common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION
_SERVICE_OPERATE_TYPE_ADD: Final[int] = common_pb2.enum_SERVICE_OPERATE_TYPE_ADD

# `general_file_operation.file_type` enum values (from
# reference/general_file_operation.proto). Only the values we use are
# named here; the device accepts more (TRAINING, MAP, THEME, FIRMWARE,
# LANGUAGE, AGPS, ROUTE_BOOK).
FILE_OP_TYPE_ROUTE_PLAN: Final[int] = 2

# Magic byte at offset 3 of the 20-byte head for a chunked file
# upload — without this, the device treats the payload as a
# standard PbFrame request and rejects it. Source:
# `sendRoutePlanFileSingleChannel` smali line 3807 (`const/16 v2,
# -86` → 0xaa, written into the byte that BaseFactory calls
# ``byte3``).
_FILE_OP_TAG_UPLOAD: Final[int] = 0xAA


def _build_general_file_operation_pb(
    *,
    file_type: int,
    file_size: int,
    file_id: int,
    file_name: str,
    file_extension: str,
) -> bytes:
    """Hand-roll the ``general_file_operation`` protobuf.

    The generated module isn't checked in (the ``reference/`` proto
    is consumed by ``gen-proto`` but ``general_file_operation`` was
    only discovered after we already shipped the route_plan path);
    hand-encoding keeps the new path self-contained until the
    schema gets the protoc treatment in a follow-up.
    """

    def varint(v: int) -> bytes:
        out = bytearray()
        while v > 0x7F:
            out.append(0x80 | (v & 0x7F))
            v >>= 7
        out.append(v & 0x7F)
        return bytes(out)

    def field_varint(field: int, v: int) -> bytes:
        return bytes([(field << 3) | 0]) + varint(v)

    def field_str(field: int, s: str) -> bytes:
        b = s.encode("utf-8")
        return bytes([(field << 3) | 2]) + varint(len(b)) + b

    return (
        field_varint(1, _SERVICE_FILE_OPERATION)
        + field_varint(2, _SERVICE_OPERATE_TYPE_ADD)
        + field_varint(3, file_type)
        + field_varint(4, file_size)
        + field_varint(5, file_id)
        + field_str(6, file_name)
        + field_str(7, file_extension)
    )


def _build_file_operation_head(*, operate: int) -> bytes:
    """Build the 20-byte head for a chunked FILE_OPERATION upload.

    Layout (matches ``BaseFactory.confirmCommandByteArray()`` with
    ``mainServiceType=FILE_OPERATION``, ``mainCommandByte=ADD``,
    ``getData()`` empty, then byte 3 patched to 0xaa by
    ``sendRoutePlanFileSingleChannel``):

      [0] 0x01 (TYPE_PB)
      [1] 0x15 (FILE_OPERATION)
      [2] 0xff (sub_service)
      [3] 0xaa (file_tag - upload magic)
      [4] op  (ADD = 3)
      [5] 0xff (sub_operation)
      [6] 0xff (reserved)
      [7-8] 0x0000 (size — getData() is empty here; the actual
                    size lives in the 4-byte BE prefix that
                    follows this 20-byte head on the wire)
      [9] 0x00 (CRC8 of empty payload)
      [10] 0x01 (END_TYPE_PB)
      [11-18] 0xff
      [19] CRC8(bytes 0..18)
    """
    head = bytearray(20)
    head[0] = 0x01
    head[1] = _SERVICE_FILE_OPERATION & 0xFF
    head[2] = 0xFF
    head[3] = _FILE_OP_TAG_UPLOAD
    head[4] = operate & 0xFF
    head[5] = 0xFF
    head[6] = 0xFF
    head[7] = 0x00
    head[8] = 0x00
    head[9] = 0x00
    head[10] = 0x01
    for off in range(11, 19):
        head[off] = 0xFF
    head[19] = framing.crc8(bytes(head[:19]))
    return bytes(head)


async def upload_general_file(
    client: IgpsportClient,
    file_bytes: bytes,
    *,
    file_type: int,
    file_id: int,
    file_name: str,
    file_extension: str,
    chunk_size: int | None = None,
    timeout: float = 30.0,
    start_navigation: bool = False,
    generation: int = 4,
) -> int:
    """Upload *file_bytes* via the FILE_OPERATION ADD path.

    Used by the BSC200 (and other devices) for CNX route uploads — the
    Android app calls this ``sendRoutePlanFileSingleChannel``. The full
    payload (head + size prefix + metadata protobuf + file bytes) is
    written in MTU-sized chunks to the "fourth" characteristic
    (``…-6e``). The device sends one notification on the same service
    channel after processing — that notification's ``status`` byte is
    the return value (``0 = Success``).

    *chunk_size* defaults to ``transport MTU - 3``. With BlueZ-direct
    + MTU 247 that's 244 bytes per chunk; with bleak's default MTU
    23 it's 20.

    *start_navigation*, when True, issues a ``ROUTE_PLAN FILE_USE``
    after a successful upload (only meaningful for
    ``file_type=FILE_OP_TYPE_ROUTE_PLAN``). This activates the route
    on the device and starts navigation — mirrors what
    ``RoadBookSearchActivity.sendFileToDevice`` does in the
    iGPSPORT app when its ``sendOnly`` flag is false. *generation*
    is plumbed through to :func:`_send_file_use` to pick the correct
    data-bearing characteristic for the FILE_USE protobuf body.

    Raises :class:`RouteUploadError` if the device returns a non-zero
    status to the upload itself. Raises :class:`NavigationStartError`
    if the FILE_USE step (when requested) fails — the upload landed,
    but the route is not active. Raises :class:`asyncio.TimeoutError`
    if either reply does not arrive within *timeout*.
    """
    head = _build_file_operation_head(operate=_SERVICE_OPERATE_TYPE_ADD)
    pb = _build_general_file_operation_pb(
        file_type=file_type,
        file_size=len(file_bytes),
        file_id=file_id,
        file_name=file_name,
        file_extension=file_extension,
    )
    payload = head + struct.pack(">I", len(pb)) + pb + file_bytes
    if chunk_size is None:
        # Subtract 3 (ATT op + handle) to land each write in one
        # ATT packet. The transport may further split if the MTU is
        # smaller than the chunk, but we send what the device parser
        # expects.
        mtu = client._transport.mtu if hasattr(client._transport, "mtu") else 23
        if callable(mtu):
            mtu = mtu()
        chunk_size = max(int(mtu) - 3, 20)

    queue = await client.open_subscription(_SERVICE_FILE_OPERATION)
    try:
        n_writes = 0
        for off in range(0, len(payload), chunk_size):
            await client._transport.send(payload[off : off + chunk_size], channel="fourth")
            n_writes += 1
        _LOG.debug(
            "FILE_OPERATION ADD upload: %d bytes payload in %d writes (chunk=%d)",
            len(payload),
            n_writes,
            chunk_size,
        )
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(_SERVICE_FILE_OPERATION, queue)

    status = response.frame.status
    _LOG.debug(
        "FILE_OPERATION ADD: status=%d (%s)",
        status,
        _status_name(status),
    )
    if status not in (_STATUS_OK, _STATUS_DONE_EARLY):
        raise RouteUploadError(status, 0, n_writes)
    if start_navigation:
        # Upload landed — activate the route. ROUTE_PLAN FILE_USE on
        # the fourth channel for gen 4+ (single merged write) or
        # split body/header for legacy gen ≤ 3. The device's UI
        # transitions into navigation mode on status=0; the iGPSPORT
        # app waits ~5 s after the ACK before dismissing its dialog.
        # `file_name` carries the display name the upload protobuf
        # used — the BSC200 firmware validates this field in the
        # FILE_USE protobuf and silently drops a request without it.
        nav_status = await _send_file_use(
            client,
            file_id=file_id,
            file_extension=file_extension,
            generation=generation,
            timeout=timeout,
            name=file_name,
        )
        if nav_status not in (_STATUS_OK, _STATUS_DONE_EARLY):
            raise NavigationStartError(nav_status, file_id)
    return status


# ---- ROUTE_PLAN FILES_DEL --------------------------------------------
#
# The iGPSPORT app's `IGPDeviceManager.deleteRoutePlanFile` (smali line
# 7419) is the reference: it builds a route_plan_data_msg with
# operate_type = FILES_DEL (op=6, **not** FILE_DEL=3) and BOTH the
# `line_id` list AND fully populated `route_plan_info_msg` entries
# (id + file_type + name + total_distance). The BSC200 firmware
# silently no-ops FILES_DEL requests that are missing the info_msg
# fields — verified live against firmware 2024-05-14.
#
# The active route (status = USED) is protected by the firmware: a
# FILES_DEL targeting it returns status=0 (Success) but the route
# stays on the device. Callers that need a hard guarantee must
# re-issue LIST_GET and check whether the target id is gone. See
# docs/PROTOCOL.md §7.4.


async def delete_route_plan_files(
    client: IgpsportClient,
    files: Sequence[tuple[int, str, str]],
    *,
    generation: int = 4,
    timeout: float = 10.0,
) -> int:
    """Issue ``ROUTE_PLAN FILES_DEL`` for *files* and return the device status byte.

    *files* is a sequence of ``(file_id, name, extension)`` tuples — the
    smali pulls these from ``DeleteRouteBean`` and the captured wire
    shows the BSC200 firmware requires all three fields populated in
    each ``route_plan_info_msg`` entry.

    *generation*: when ≥ 4 (BSC200, iGS630) the request goes out as a
    single merged write of (head ‖ body) to the fourth characteristic
    — same wire pattern as :func:`_send_file_use`. For legacy gen ≤ 3
    devices it falls back to the body-on-data + header-on-control
    split.

    Returns the wire status byte. **Caveat**: the active route is
    protected by BSC200 firmware — the device returns 0 (Success) for
    any FILES_DEL request that includes the active route, but doesn't
    actually delete it. Callers that need to confirm a successful
    delete should re-issue ``ROUTE_PLAN LIST_GET`` and check whether
    the target ids are gone.
    """
    if not files:
        return _STATUS_OK
    msg = route_plan_pb2.route_plan_data_msg()
    msg.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN
    msg.route_plan_operate_type = route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILES_DEL
    for file_id, name, extension in files:
        msg.line_id.append(f"{file_id}.{extension}")
        info = msg.route_plan_info_msg.add()
        info.id = file_id
        info.file_type = _ROUTE_PLAN_FILE_TYPE_BY_EXT.get(
            extension.lower(),
            route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_INVALID,
        )
        info.name = name or str(file_id)
        info.total_distance = 0
    body = msg.SerializeToString()
    header = _build_files_del_header(body)
    queue = await client.open_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN)
    try:
        if generation >= 4:
            await client._transport.send(header + body, channel="fourth")
        else:
            data_channel: Channel = "fourth" if generation >= 3 else "data"
            await client._transport.send(body, channel=data_channel)
            await client._transport.send(header, channel="control")
        response = await asyncio.wait_for(queue.get(), timeout=timeout)
    finally:
        await client.close_subscription(common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN, queue)
    status = response.frame.status  # type: ignore[attr-defined]
    _LOG.debug(
        "FILES_DEL: %d ids → status=%d (%s)",
        len(files),
        status,
        _status_name(status),
    )
    return int(status)


def _build_files_del_header(send_data: bytes) -> bytes:
    """Standard 20-byte PbFrame head with operation=FILES_DEL."""
    header = bytearray(framing.HEADER_SIZE)
    header[framing.HDR_TYPE] = framing.TYPE_PB
    header[framing.HDR_SERVICE] = common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN & 0xFF
    header[framing.HDR_SUB_SERVICE] = 0xFF
    header[framing.HDR_FILE_TAG] = 0xFF
    header[framing.HDR_OPERATION] = route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILES_DEL & 0xFF
    header[framing.HDR_SUB_OPERATION] = 0xFF
    header[framing.HDR_RESERVED_6] = 0xFF
    size = len(send_data)
    header[framing.HDR_PAYLOAD_SIZE] = (size >> 8) & 0xFF
    header[framing.HDR_PAYLOAD_SIZE + 1] = size & 0xFF
    header[framing.HDR_PAYLOAD_CRC] = framing.crc8(send_data)
    header[framing.HDR_END_MARKER] = framing.TYPE_PB
    for off in range(11, 19):
        header[off] = 0xFF
    header[framing.HDR_HEADER_CRC] = framing.crc8(bytes(header[: framing.HDR_HEADER_CRC]))
    return bytes(header)

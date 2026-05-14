"""Minimal Garmin FIT Course file encoder, stdlib only.

The BSC200 firmware rejects GPX content with ``status=1`` (DataError);
the Android app always passes ``file_extension="cnx"`` and the bytes
have been server-side converted by ``i.igpsport.com``. CNX is opaque,
but ``route_plan`` protobuf's ``fileType`` enum also accepts
``FIT``. FIT is an open Garmin format — if the BSC200 firmware
accepts it directly, we can sidestep the CNX cloud round-trip
entirely.

This module emits a **Course** FIT file (file_id type=6) holding one
lap plus N records (one per route point), per the Garmin FIT 2.0
protocol. Pure stdlib (``struct``, ``time``). Reference:
https://developer.garmin.com/fit/protocol/

Why minimal:
  * Manufacturer = 255 (development), product/serial = 0/1.
  * One lap covering the entire route, fabricated total_elapsed_time.
  * Records carry position_lat/long, distance, altitude. No timestamps
    per record (FIT requires record.timestamp; we synthesise one second
    per record, starting at file's time_created).
  * Sport = Cycling (2).
"""

from __future__ import annotations

import struct
import time
from typing import Final

from .routes import RouteData, _haversine_m

# FIT epoch is 1989-12-31T00:00:00 UTC. Unix epoch + this offset.
_FIT_EPOCH_OFFSET: Final[int] = 631065600

# Global message numbers from the FIT profile (Garmin SDK Profile.xlsx).
_MESG_FILE_ID: Final[int] = 0
_MESG_LAP: Final[int] = 19
_MESG_RECORD: Final[int] = 20
_MESG_EVENT: Final[int] = 21
_MESG_COURSE: Final[int] = 31

# FIT base types used here.
_BT_ENUM: Final[int] = 0x00  # 1 byte
_BT_UINT8: Final[int] = 0x02  # 1 byte
_BT_UINT16: Final[int] = 0x84  # 2 bytes, invalid = 0xFFFF
_BT_UINT32: Final[int] = 0x86  # 4 bytes, invalid = 0xFFFFFFFF
_BT_SINT32: Final[int] = 0x85  # 4 bytes, invalid = 0x7FFFFFFF
_BT_STRING: Final[int] = 0x07  # variable-length UTF-8, null-padded
_BT_UINT32Z: Final[int] = 0x8C  # 4 bytes, invalid = 0x00000000

# CRC-16/ARC table used by FIT (low/high nibbles → 16-bit lookup).
_CRC16_TABLE: Final[tuple[int, ...]] = (
    0x0000,
    0xCC01,
    0xD801,
    0x1400,
    0xF001,
    0x3C00,
    0x2800,
    0xE401,
    0xA001,
    0x6C00,
    0x7800,
    0xB401,
    0x5000,
    0x9C01,
    0x8801,
    0x4400,
)


def _fit_crc16(data: bytes) -> int:
    """CRC-16 over *data* using the FIT-protocol algorithm.

    Garmin FIT SDK uses a 4-bit table-driven CRC-16 (polynomial 0xA001
    reflected = 0x8005 standard form). Process each byte as two nibbles,
    low first. Matches the implementation in ``fit_crc.c`` of the SDK.
    """
    crc = 0
    for b in data:
        tmp = _CRC16_TABLE[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ tmp ^ _CRC16_TABLE[b & 0xF]
        tmp = _CRC16_TABLE[crc & 0xF]
        crc = (crc >> 4) & 0x0FFF
        crc = crc ^ tmp ^ _CRC16_TABLE[(b >> 4) & 0xF]
    return crc & 0xFFFF


def _deg_to_semicircles(deg: float) -> int:
    """Convert degrees to FIT semicircles (sint32, ``deg * 2^31 / 180``)."""
    v = round(deg * (2**31 / 180.0))
    # clamp into sint32 range, leaving 0x7FFFFFFF as the invalid marker
    if v >= 0x7FFFFFFF:
        v = 0x7FFFFFFE
    if v < -0x80000000:
        v = -0x80000000
    return v & 0xFFFFFFFF


def _altitude_encode(metres: float | None) -> int:
    """FIT ``altitude`` (uint16): ``(m + 500) * 5``. Invalid = 0xFFFF."""
    if metres is None:
        return 0xFFFF
    v = round((metres + 500.0) * 5)
    if v < 0 or v > 0xFFFE:
        return 0xFFFF
    return v


def _unix_to_fit_time(unix_seconds: int) -> int:
    """Convert a Unix timestamp to a FIT timestamp (seconds since 1989-12-31)."""
    v = unix_seconds - _FIT_EPOCH_OFFSET
    if v < 0:
        v = 0
    return v & 0xFFFFFFFF


def _truncate_string(s: str, *, max_bytes: int) -> bytes:
    """Encode *s* as UTF-8, truncate to ``max_bytes - 1`` and null-terminate.

    Matches FIT's string field convention: fixed-length, NUL-padded.
    """
    encoded = s.encode("utf-8")[: max_bytes - 1]
    return encoded + b"\x00" * (max_bytes - len(encoded))


def _def_message(local_num: int, global_num: int, fields: list[tuple[int, int, int]]) -> bytes:
    """Build a FIT definition message record.

    *local_num* is the 4-bit local message number (0..15), referenced by
    subsequent data messages. *fields* is a list of
    ``(field_def_num, size_bytes, base_type)`` tuples — order here defines
    the order of values in matching data messages.
    """
    if not (0 <= local_num <= 15):
        raise ValueError(f"local_num out of range: {local_num}")
    buf = bytearray()
    # Record header: bit 6 set = definition message; low nibble = local num.
    buf.append(0x40 | local_num)
    buf.append(0x00)  # reserved
    buf.append(0x00)  # arch (0 = little endian)
    buf += struct.pack("<H", global_num)
    buf.append(len(fields))
    for field_num, size, base_type in fields:
        buf += bytes((field_num, size, base_type))
    return bytes(buf)


def _data_header(local_num: int) -> int:
    """Record header byte for a data message (bit 6 clear)."""
    return local_num & 0x0F


# Local message numbers used in our emitted Course file. The protocol
# allows up to 16 simultaneous definitions, but we only need 4 — they
# never need to be redefined mid-stream.
_LOCAL_FILE_ID: Final[int] = 0
_LOCAL_COURSE: Final[int] = 1
_LOCAL_LAP: Final[int] = 2
_LOCAL_RECORD: Final[int] = 3
_LOCAL_EVENT: Final[int] = 4


def to_fit_course_bytes(route: RouteData, *, time_created: int | None = None) -> bytes:
    """Serialise *route* as a Garmin FIT Course file.

    Returns the complete byte string including the 14-byte header,
    record stream, and trailing 2-byte CRC. The result has the
    ``.FIT`` signature at bytes 8..11 of the header.

    *time_created* is a Unix timestamp; defaults to ``time.time()``.
    Used for ``file_id.time_created`` and as the starting timestamp for
    record/lap/event messages (synthesised one second per record).

    Raises :class:`ValueError` for routes with zero points.
    """
    if not route.points:
        raise ValueError("can't emit a FIT course for a route with no points")
    if time_created is None:
        time_created = int(time.time())
    fit_now = _unix_to_fit_time(time_created)
    n = len(route.points)

    records = bytearray()

    # 1. file_id definition + data
    records += _def_message(
        _LOCAL_FILE_ID,
        _MESG_FILE_ID,
        [
            (0, 1, _BT_ENUM),  # type
            (1, 2, _BT_UINT16),  # manufacturer
            (2, 2, _BT_UINT16),  # product
            (3, 4, _BT_UINT32Z),  # serial_number
            (4, 4, _BT_UINT32),  # time_created
        ],
    )
    records.append(_data_header(_LOCAL_FILE_ID))
    records += bytes([6])  # type = Course
    records += struct.pack("<H", 255)  # manufacturer = Development
    records += struct.pack("<H", 0)  # product
    records += struct.pack("<I", 1)  # serial_number (uint32z; non-zero)
    records += struct.pack("<I", fit_now)

    # 2. course definition + data
    _COURSE_NAME_LEN = 16
    records += _def_message(
        _LOCAL_COURSE,
        _MESG_COURSE,
        [
            (5, _COURSE_NAME_LEN, _BT_STRING),  # name
            (4, 1, _BT_ENUM),  # sport
        ],
    )
    records.append(_data_header(_LOCAL_COURSE))
    records += _truncate_string(route.name, max_bytes=_COURSE_NAME_LEN)
    records += bytes([2])  # sport = Cycling

    # 3. event definition (timer start at file start, timer stop_all at end)
    records += _def_message(
        _LOCAL_EVENT,
        _MESG_EVENT,
        [
            (253, 4, _BT_UINT32),  # timestamp
            (0, 1, _BT_ENUM),  # event
            (1, 1, _BT_ENUM),  # event_type
            (4, 1, _BT_UINT8),  # event_group
        ],
    )
    records.append(_data_header(_LOCAL_EVENT))
    records += struct.pack("<I", fit_now)
    records += bytes([0, 0, 0])  # event=Timer, event_type=Start, group=0

    # 4. record definition
    records += _def_message(
        _LOCAL_RECORD,
        _MESG_RECORD,
        [
            (253, 4, _BT_UINT32),  # timestamp
            (0, 4, _BT_SINT32),  # position_lat
            (1, 4, _BT_SINT32),  # position_long
            (5, 4, _BT_UINT32),  # distance (m * 100)
            (2, 2, _BT_UINT16),  # altitude ((m + 500) * 5)
        ],
    )

    # Records: one per point, synthesising one-second cadence and a
    # cumulative haversine distance so the device has a meaningful
    # progress signal mid-route.
    cumulative_m = 0.0
    prev = None
    record_header = _data_header(_LOCAL_RECORD)
    for i, p in enumerate(route.points):
        if prev is not None:
            cumulative_m += _haversine_m(prev, p)
        prev = p
        ts = fit_now + i
        records.append(record_header)
        records += struct.pack("<I", ts)
        records += struct.pack("<i", _signed32(_deg_to_semicircles(p.latitude)))
        records += struct.pack("<i", _signed32(_deg_to_semicircles(p.longitude)))
        records += struct.pack("<I", min(round(cumulative_m * 100), 0xFFFFFFFE))
        records += struct.pack("<H", _altitude_encode(p.elevation))

    # 5. lap definition + data — one lap summarising the whole course.
    records += _def_message(
        _LOCAL_LAP,
        _MESG_LAP,
        [
            (253, 4, _BT_UINT32),  # timestamp
            (2, 4, _BT_UINT32),  # start_time
            (3, 4, _BT_SINT32),  # start_position_lat
            (4, 4, _BT_SINT32),  # start_position_long
            (5, 4, _BT_SINT32),  # end_position_lat
            (6, 4, _BT_SINT32),  # end_position_long
            (7, 4, _BT_UINT32),  # total_elapsed_time (s * 1000)
            (8, 4, _BT_UINT32),  # total_timer_time
            (9, 4, _BT_UINT32),  # total_distance (m * 100)
        ],
    )
    end_ts = fit_now + max(0, n - 1)
    first_pt = route.points[0]
    last_pt = route.points[-1]
    elapsed_ms = max(1, (n - 1)) * 1000
    records.append(_data_header(_LOCAL_LAP))
    records += struct.pack("<I", end_ts)  # timestamp
    records += struct.pack("<I", fit_now)  # start_time
    records += struct.pack("<i", _signed32(_deg_to_semicircles(first_pt.latitude)))
    records += struct.pack("<i", _signed32(_deg_to_semicircles(first_pt.longitude)))
    records += struct.pack("<i", _signed32(_deg_to_semicircles(last_pt.latitude)))
    records += struct.pack("<i", _signed32(_deg_to_semicircles(last_pt.longitude)))
    records += struct.pack("<I", elapsed_ms)
    records += struct.pack("<I", elapsed_ms)
    records += struct.pack("<I", min(round(cumulative_m * 100), 0xFFFFFFFE))

    # 6. event stop_all
    records.append(_data_header(_LOCAL_EVENT))
    records += struct.pack("<I", end_ts)
    records += bytes([0, 9, 0])  # event=Timer, event_type=Stop_disable_all, group=0

    # Header: size=14, proto=0x20 (v2.0), profile=2100 (21.00),
    # data_size = len(records), ".FIT", crc-16 over bytes 0..11.
    header_no_crc = bytearray()
    header_no_crc.append(14)  # header_size
    header_no_crc.append(0x20)  # protocol_version (2.0)
    header_no_crc += struct.pack("<H", 2100)  # profile_version
    header_no_crc += struct.pack("<I", len(records))  # data_size
    header_no_crc += b".FIT"
    header_crc = _fit_crc16(bytes(header_no_crc))
    header = bytes(header_no_crc) + struct.pack("<H", header_crc)

    body = header + bytes(records)
    file_crc = _fit_crc16(body)
    return body + struct.pack("<H", file_crc)


def _signed32(u: int) -> int:
    """Convert an unsigned 32-bit value to its signed two's-complement form.

    ``_deg_to_semicircles`` returns a value already masked to 32 bits;
    ``struct.pack("<i", ...)`` needs a *signed* int. This adapter
    bridges the two without going through float.
    """
    if u >= 0x80000000:
        return u - 0x100000000
    return u

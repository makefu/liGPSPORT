"""Byte-level framing for the iGPSPORT BLE protocol.

Every logical message is **exactly 20 bytes** of fixed-size header
followed by zero or more bytes of protobuf payload. The first byte of
the header (``type``) selects between three layouts:

* ``0x01`` -- `PbFrame`. The header is followed by a protobuf payload.
  Length is in bytes 7-8 (big-endian u16). Used for every app-issued
  command and most device-issued responses. Source:
  ``com.igpsport.blelib.pbfactory.BaseHead20Bytes#confirmCommandByteArray``.
* ``0x02`` -- `ConfirmFrame`. Standalone 20-byte ack. Sent app to
  device after a notification, or device to app after a multi-frame
  upload. Source: ``com.igpsport.blelib.pbfactory.ConfirmCommand``.
* ``0x03`` -- `RequestFrame`. Same byte layout as `ConfirmFrame` but
  device-initiated (e.g. "send me AGPS ephemeris data"). Source: the
  ``ControlUARTManager`` callback path treats type=3 the same as
  ConfirmCommand for decoding.

All three layouts share the same final byte: a CRC-8/MAXIM over
bytes 0..18. ``PbFrame`` additionally carries a second CRC at
offset 9 over the protobuf payload.

CRC8 is the `CRC-8/MAXIM` variant (polynomial 0x31, init 0, both input
and output reflected, no final XOR) — the algorithm the Dallas/Maxim
1-Wire bus uses for DS18B20-style devices. The 256-byte lookup table
below was transcribed verbatim from ``com.igpsport.blelib.utils.CRC8``
(the ``crc8_tab`` static array in ``classes4.dex``).

Byte layouts:

PbFrame (type=0x01, transcribed from BaseHead20Bytes)::

    offset width  field               default       notes
    ----------------------------------------------------------------
    0      1      type                0x01          END_TYPE_PB
    1      1      service             (per service) common.service_type_index
    2      1      sub_service         0xFF          second-tier service byte
    3      1      file_tag            0xFF          set by setSendFileTag for multipart files
    4      1      operation           0xFF          main operate-type
    5      1      sub_operation       0xFF          second-tier operate-type
    6      1      (reserved)          0xFF          literal -1 in the Kotlin code
    7-8    2      payload_size        u16 big-endian (StringUtils.unsignedShortToByte2)
    9      1      payload_crc         CRC8 over the payload bytes
    10     1      end_marker          0x01          literal 1 in the Kotlin code
    11-18  8      reserved_padding    0xFF x 8      filled by RESERVED_BYTE_SIZE=8 loop
    19     1      header_crc          CRC8 over bytes 0..18 (added by Companion.updateCRC)

ConfirmFrame (type=0x02) and RequestFrame (type=0x03), transcribed
from ConfirmCommand::

    offset width  field               default       notes
    ----------------------------------------------------------------
    0      1      type                0x02 or 0x03
    1      1      service             (set)
    2      1      sub_service         (set)         secondService field
    3      1      (reserved)          0xFF
    4      1      operation           (set)         mainOperation field
    5      1      sub_operation       (set)         secondOperation field
    6      1      (reserved)          0xFF
    7      1      status              (set)         0 = ok, non-zero = error
    8-18   11     reserved_padding    0xFF x 11     RESERVED_BYTE_SIZE=11 loop
    19     1      header_crc          CRC8 over bytes 0..18
"""

from __future__ import annotations

import dataclasses
from typing import Final

HEADER_SIZE: Final[int] = 20

# Field offsets, kept as named constants so call sites read like a spec.
HDR_TYPE: Final[int] = 0
HDR_SERVICE: Final[int] = 1
HDR_SUB_SERVICE: Final[int] = 2
HDR_FILE_TAG: Final[int] = 3  # PbFrame only; ConfirmFrame uses offset 3 as reserved.
HDR_OPERATION: Final[int] = 4
HDR_SUB_OPERATION: Final[int] = 5
HDR_RESERVED_6: Final[int] = 6
HDR_PAYLOAD_SIZE: Final[int] = 7  # PbFrame: 2 bytes BE at 7..8. ConfirmFrame: 1 byte status at 7.
HDR_STATUS: Final[int] = 7
HDR_PAYLOAD_CRC: Final[int] = 9  # PbFrame only.
HDR_END_MARKER: Final[int] = 10  # PbFrame only.
HDR_RESERVED_PAD: Final[int] = 11  # PbFrame: 8 bytes at 11..18. ConfirmFrame: 11 bytes at 8..18.
HDR_HEADER_CRC: Final[int] = 19

# Type-byte values (offset 0). One of these distinguishes the three
# frame layouts: 0x01 carries protobuf payload, 0x02 is an ack, 0x03
# is a device-initiated request.
TYPE_PB: Final[int] = 0x01  # PbFrame with protobuf payload (END_TYPE_PB in the Kotlin)
TYPE_CONFIRM: Final[int] = 0x02  # Standalone ConfirmCommand-style ack
TYPE_REQUEST: Final[int] = 0x03  # Device-initiated request (same byte layout as confirm)

# Backwards-compatibility alias; END_TYPE_PB is the name the Kotlin
# source uses for the same 0x01 constant. Kept so PROTOCOL.md
# transcripts read naturally.
END_TYPE_PB: Final[int] = TYPE_PB

RESERVED_BYTE: Final[int] = 0xFF  # default fill for unset fields
RESERVED_PAD_LENGTH: Final[int] = 8  # PbFrame reserved-pad length (offsets 11..18).
CONFIRM_RESERVED_PAD_LENGTH: Final[int] = 11  # ConfirmFrame reserved-pad length (offsets 8..18).

# CRC-8/MAXIM lookup table, transcribed verbatim from the `crc8_tab`
# static array in `com.igpsport.blelib.utils.CRC8` (classes4.dex).
# Polynomial 0x31, init 0, reflected input/output, no xor-out — the
# CRC-8/DOW algorithm used by Dallas/Maxim 1-Wire devices. Stored as a
# hex string so `ruff format` doesn't expand it into 256 one-per-line
# entries; bytes.fromhex decodes it once at module load.
_CRC8_TABLE: Final[bytes] = bytes.fromhex(
    "005ebce2613fdd83c29c7e20a3fd1f41"
    "9dc3217ffca2401e5f01e3bd3e6082dc"
    "237d9fc1421cfea0e1bf5d0380de3c62"
    "bee0025cdf81633d7c22c09e1d43a1ff"
    "4618faa427799bc584da3866e5bb5907"
    "db856739bae406581947a5fb7826c49a"
    "653bd987045ab8e6a7f91b45c6987a24"
    "f8a6441a99c7257b3a6486d85b05e7b9"
    "8cd2306eedb3510f4e10f2ac2f7193cd"
    "114fadf3702ecc92d38d6f31b2ec0e50"
    "aff1134dce90722c6d33d18f0c52b0ee"
    "326c8ed0530defb1f0ae4c1291cf2d73"
    "ca947628abf517490856b4ea6937d58b"
    "5709ebb536688ad495cb2977f4aa4816"
    "e9b7550b88d6346a2b7597c94a14f6a8"
    "742ac896154ba9f7b6e80a54d7896b35"
)
assert len(_CRC8_TABLE) == 256


def crc8(data: bytes, *, init: int = 0) -> int:
    """CRC-8/MAXIM over *data*.

    Matches ``com.igpsport.blelib.utils.CRC8.calcCrc8(byte[])`` byte
    for byte. ``init`` defaults to 0 (the zero-arg overload's choice);
    pass through a previous CRC to chain over discontiguous spans.
    """
    crc = init & 0xFF
    for b in data:
        crc = _CRC8_TABLE[(crc ^ b) & 0xFF]
    return crc


class FrameError(ValueError):
    """Raised by :func:`parse_frame` when a frame fails validation."""


@dataclasses.dataclass(slots=True, frozen=True)
class Frame:
    """A parsed (or to-be-built) iGPSPORT logical frame.

    For ``type == TYPE_PB`` (the common case), ``payload`` carries the
    protobuf bytes that follow the 20-byte header. For
    ``TYPE_CONFIRM`` / ``TYPE_REQUEST`` (acks and device-initiated
    requests), ``payload`` is always empty and the ``status`` field
    carries the byte at offset 7.
    """

    service: int
    payload: bytes = b""
    operation: int = 0xFF
    sub_service: int = 0xFF
    sub_operation: int = 0xFF
    file_tag: int = 0xFF
    type: int = TYPE_PB
    status: int = 0


def build_frame(frame: Frame) -> bytes:
    """Serialise *frame* to the on-wire byte string.

    Dispatches on ``frame.type`` between the three layouts. Both CRC8
    bytes (payload + header for PbFrame, just header for the others)
    are filled in here.
    """
    if frame.type == TYPE_PB:
        return _build_pb_frame(frame)
    if frame.type in (TYPE_CONFIRM, TYPE_REQUEST):
        if frame.payload:
            raise FrameError(
                f"type=0x{frame.type:02X} frames carry no payload (got {len(frame.payload)} bytes)"
            )
        return _build_confirm_frame(frame)
    raise FrameError(f"unknown frame type: 0x{frame.type:02X}")


def _build_pb_frame(frame: Frame) -> bytes:
    payload = frame.payload
    size = len(payload)
    if size > 0xFFFF:
        raise FrameError(f"payload too large for u16 size field: {size} bytes")

    header = bytearray(HEADER_SIZE)
    header[HDR_TYPE] = TYPE_PB
    header[HDR_SERVICE] = frame.service & 0xFF
    header[HDR_SUB_SERVICE] = frame.sub_service & 0xFF
    header[HDR_FILE_TAG] = frame.file_tag & 0xFF
    header[HDR_OPERATION] = frame.operation & 0xFF
    header[HDR_SUB_OPERATION] = frame.sub_operation & 0xFF
    header[HDR_RESERVED_6] = RESERVED_BYTE
    header[HDR_PAYLOAD_SIZE] = (size >> 8) & 0xFF  # big-endian, high byte first
    header[HDR_PAYLOAD_SIZE + 1] = size & 0xFF
    header[HDR_PAYLOAD_CRC] = crc8(payload)
    header[HDR_END_MARKER] = TYPE_PB
    for off in range(HDR_RESERVED_PAD, HDR_RESERVED_PAD + RESERVED_PAD_LENGTH):
        header[off] = RESERVED_BYTE
    header[HDR_HEADER_CRC] = crc8(bytes(header[:HDR_HEADER_CRC]))
    return bytes(header) + payload


def _build_confirm_frame(frame: Frame) -> bytes:
    header = bytearray(HEADER_SIZE)
    header[HDR_TYPE] = frame.type & 0xFF
    header[HDR_SERVICE] = frame.service & 0xFF
    header[HDR_SUB_SERVICE] = frame.sub_service & 0xFF
    header[3] = RESERVED_BYTE
    header[HDR_OPERATION] = frame.operation & 0xFF
    header[HDR_SUB_OPERATION] = frame.sub_operation & 0xFF
    header[HDR_RESERVED_6] = RESERVED_BYTE
    header[HDR_STATUS] = frame.status & 0xFF
    for off in range(8, 8 + CONFIRM_RESERVED_PAD_LENGTH):
        header[off] = RESERVED_BYTE
    header[HDR_HEADER_CRC] = crc8(bytes(header[:HDR_HEADER_CRC]))
    return bytes(header)


def parse_frame(buf: bytes) -> Frame:
    """Parse and validate *buf*.

    Dispatches on the type byte at offset 0: ``TYPE_PB`` carries a
    protobuf payload after the 20-byte header (size at offsets 7-8,
    payload CRC at offset 9); ``TYPE_CONFIRM`` / ``TYPE_REQUEST`` are
    standalone 20-byte messages. The header CRC at offset 19 is
    validated in all three cases.
    """
    if len(buf) < HEADER_SIZE:
        raise FrameError(f"frame too short: {len(buf)} < {HEADER_SIZE}")
    type_byte = buf[HDR_TYPE]
    header_crc_observed = buf[HDR_HEADER_CRC]
    header_crc_expected = crc8(bytes(buf[:HDR_HEADER_CRC]))
    if header_crc_observed != header_crc_expected:
        raise FrameError(
            f"header CRC mismatch: have 0x{header_crc_observed:02X}, "
            f"want 0x{header_crc_expected:02X}"
        )
    if type_byte == TYPE_PB:
        return _parse_pb_frame(buf)
    if type_byte in (TYPE_CONFIRM, TYPE_REQUEST):
        if len(buf) != HEADER_SIZE:
            raise FrameError(f"type=0x{type_byte:02X} frames are 20 bytes; got {len(buf)}")
        return Frame(
            type=type_byte,
            service=buf[HDR_SERVICE],
            operation=buf[HDR_OPERATION],
            sub_service=buf[HDR_SUB_SERVICE],
            sub_operation=buf[HDR_SUB_OPERATION],
            status=buf[HDR_STATUS],
        )
    raise FrameError(f"unknown frame type byte: 0x{type_byte:02X}")


def _parse_pb_frame(buf: bytes) -> Frame:
    if buf[HDR_END_MARKER] != TYPE_PB:
        raise FrameError(
            f"unexpected end_marker byte: 0x{buf[HDR_END_MARKER]:02X} (want 0x{TYPE_PB:02X})"
        )
    size = (buf[HDR_PAYLOAD_SIZE] << 8) | buf[HDR_PAYLOAD_SIZE + 1]
    expected_total = HEADER_SIZE + size
    if len(buf) != expected_total:
        raise FrameError(f"frame length mismatch: have {len(buf)}, header says {expected_total}")
    payload = bytes(buf[HEADER_SIZE:])
    payload_crc_observed = buf[HDR_PAYLOAD_CRC]
    payload_crc_expected = crc8(payload)
    if payload_crc_observed != payload_crc_expected:
        raise FrameError(
            f"payload CRC mismatch: have 0x{payload_crc_observed:02X}, "
            f"want 0x{payload_crc_expected:02X}"
        )
    return Frame(
        type=TYPE_PB,
        service=buf[HDR_SERVICE],
        operation=buf[HDR_OPERATION],
        sub_service=buf[HDR_SUB_SERVICE],
        sub_operation=buf[HDR_SUB_OPERATION],
        file_tag=buf[HDR_FILE_TAG],
        payload=payload,
    )


def expected_total_size(header: bytes) -> int:
    """Total frame size in bytes from a 20-byte header buffer.

    Used by the BLE reassembly loop in :mod:`ligpsport.ble` to know
    when to stop accumulating chunks before validating with
    :func:`parse_frame`.
    """
    if len(header) < HEADER_SIZE:
        raise FrameError(f"header too short: {len(header)} < {HEADER_SIZE}")
    type_byte = header[HDR_TYPE]
    if type_byte == TYPE_PB:
        return HEADER_SIZE + ((header[HDR_PAYLOAD_SIZE] << 8) | header[HDR_PAYLOAD_SIZE + 1])
    if type_byte in (TYPE_CONFIRM, TYPE_REQUEST):
        return HEADER_SIZE
    raise FrameError(f"unknown frame type byte: 0x{type_byte:02X}")


# Backwards-compatibility alias used by older test code.
parse_header = expected_total_size

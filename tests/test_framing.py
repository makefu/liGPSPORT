"""Tests for the 20-byte header + CRC8 framing codec.

Both halves of the build/parse pair traverse the same code path, so a
regression in either direction surfaces here. Reference vectors come
from the CRC-8/MAXIM specification (the check value 0xA1 over
b"123456789" is the canonical sanity check) and from the constants
hard-coded in
``com.igpsport.blelib.pbfactory.BaseHead20Bytes.confirmCommandByteArray``.
"""

from __future__ import annotations

import os

import pytest

from ligpsport.framing import (
    END_TYPE_PB,
    HDR_END_MARKER,
    HDR_HEADER_CRC,
    HDR_PAYLOAD_CRC,
    HDR_PAYLOAD_SIZE,
    HDR_RESERVED_6,
    HDR_RESERVED_PAD,
    HDR_TYPE,
    HEADER_SIZE,
    RESERVED_BYTE,
    RESERVED_PAD_LENGTH,
    TYPE_CONFIRM,
    TYPE_REQUEST,
    Frame,
    FrameError,
    build_frame,
    crc8,
    expected_total_size,
    parse_frame,
)

# ---------- CRC8 vectors -------------------------------------------------


def test_crc8_matches_maxim_check_value() -> None:
    # CRC-8/MAXIM canonical check value: 0xA1 over b"123456789".
    # Matches the table sourced from com.igpsport.blelib.utils.CRC8.
    assert crc8(b"123456789") == 0xA1


def test_crc8_empty_is_zero() -> None:
    # The empty-message CRC must be the init value (0); otherwise
    # we'd reject zero-payload frames the device sends.
    assert crc8(b"") == 0


def test_crc8_init_threads_state() -> None:
    # Chaining two halves of an input must equal the CRC over the whole.
    full = bytes(range(64))
    half = crc8(full[:32])
    assert crc8(full[32:], init=half) == crc8(full)


# ---------- Frame round trips --------------------------------------------


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        b"\x00",
        b"\x08\x0a\x10\x01",  # a real BLE service serialized payload
        bytes(range(256)),
        os.urandom(1024),
    ],
)
def test_round_trip(payload: bytes) -> None:
    frame_in = Frame(service=10, operation=2, payload=payload)
    wire = build_frame(frame_in)
    assert len(wire) == HEADER_SIZE + len(payload)
    frame_out = parse_frame(wire)
    assert frame_out == frame_in


def test_payload_size_is_big_endian() -> None:
    # 256-byte payload encodes as 0x01 0x00 at offsets 7..8.
    wire = build_frame(Frame(service=1, payload=b"\x00" * 256))
    assert wire[HDR_PAYLOAD_SIZE] == 0x01
    assert wire[HDR_PAYLOAD_SIZE + 1] == 0x00


def test_constant_marker_bytes() -> None:
    wire = build_frame(Frame(service=10, payload=b"hi"))
    assert wire[HDR_TYPE] == END_TYPE_PB
    assert wire[HDR_END_MARKER] == END_TYPE_PB
    assert wire[HDR_RESERVED_6] == RESERVED_BYTE
    pad = wire[HDR_RESERVED_PAD : HDR_RESERVED_PAD + RESERVED_PAD_LENGTH]
    assert pad == bytes([RESERVED_BYTE] * RESERVED_PAD_LENGTH)


def test_expected_total_size_pb_frame() -> None:
    wire = build_frame(Frame(service=10, payload=b"hello world"))
    assert expected_total_size(wire[:HEADER_SIZE]) == HEADER_SIZE + len(b"hello world")


def test_expected_total_size_confirm_frame() -> None:
    wire = build_frame(Frame(service=10, type=TYPE_CONFIRM, status=0))
    assert expected_total_size(wire) == HEADER_SIZE


def test_confirm_frame_round_trip() -> None:
    f_in = Frame(service=3, sub_service=5, operation=1, type=TYPE_CONFIRM, status=0)
    wire = build_frame(f_in)
    assert len(wire) == HEADER_SIZE
    assert wire[HDR_TYPE] == TYPE_CONFIRM
    f_out = parse_frame(wire)
    assert f_out == f_in


def test_request_frame_round_trip_with_observed_device_frame() -> None:
    # Verbatim 20-byte frame the BSC200 sends to ask for AGPS ephemeris
    # data: type=0x03, service=BACK(3), sub_service=EPHEMERIS(5),
    # operation=GET(1), status=0, header CRC = 0xB3.
    observed = bytes.fromhex("030305ff01ffff00ffffffffffffffffffffffb3")
    f = parse_frame(observed)
    assert f.type == TYPE_REQUEST
    assert f.service == 3
    assert f.sub_service == 5
    assert f.operation == 1
    assert f.status == 0
    # And round-trip identity.
    assert build_frame(f) == observed


# ---------- Error paths --------------------------------------------------


def test_parse_rejects_short_buffer() -> None:
    with pytest.raises(FrameError):
        parse_frame(b"\x01" + b"\x00" * 5)


def test_parse_rejects_wrong_total_length() -> None:
    wire = bytearray(build_frame(Frame(service=10, payload=b"hi")))
    wire.append(0xAA)  # extra byte
    with pytest.raises(FrameError, match="length mismatch"):
        parse_frame(bytes(wire))


def test_parse_rejects_bad_header_crc() -> None:
    wire = bytearray(build_frame(Frame(service=10, payload=b"hi")))
    wire[HDR_HEADER_CRC] ^= 0xFF
    with pytest.raises(FrameError, match="header CRC mismatch"):
        parse_frame(bytes(wire))


def test_parse_rejects_bad_payload_crc() -> None:
    wire = bytearray(build_frame(Frame(service=10, payload=b"hi")))
    wire[HDR_PAYLOAD_CRC] ^= 0xFF
    # Bad payload-CRC: have to also fix the header-CRC, otherwise that
    # raises first (the codec is layered).
    from ligpsport.framing import crc8 as _crc8

    wire[HDR_HEADER_CRC] = _crc8(bytes(wire[:HDR_HEADER_CRC]))
    with pytest.raises(FrameError, match="payload CRC mismatch"):
        parse_frame(bytes(wire))


def test_parse_rejects_unknown_type_byte() -> None:
    wire = bytearray(build_frame(Frame(service=10, payload=b"hi")))
    wire[HDR_TYPE] = 0xAA
    from ligpsport.framing import crc8 as _crc8

    wire[HDR_HEADER_CRC] = _crc8(bytes(wire[:HDR_HEADER_CRC]))
    with pytest.raises(FrameError, match="unknown frame type"):
        parse_frame(bytes(wire))


def test_build_rejects_oversized_payload() -> None:
    huge = b"\x00" * 0x10000
    with pytest.raises(FrameError, match="payload too large"):
        build_frame(Frame(service=10, payload=huge))

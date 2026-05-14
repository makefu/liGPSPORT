"""Round-trip tests for :mod:`ligpsport.fit_course`.

The hermetic test parses the bytes we emit using the third-party
:mod:`fitparse` library (a read-only parser, declared as a test-only
dep in ``flake.nix``). If our header / record-stream / CRCs / field
encodings are correct, fitparse will yield the same records back —
that's a much stricter check than asserting on the raw byte stream.
"""

from __future__ import annotations

import io

import fitparse

from ligpsport.fit_course import _fit_crc16, to_fit_course_bytes
from ligpsport.routes import Point, RouteData


def _parse(buf: bytes) -> fitparse.FitFile:
    fit = fitparse.FitFile(io.BytesIO(buf))
    fit.parse()
    return fit


def test_fit_header_layout() -> None:
    """Header has size=14, ``.FIT`` magic at offset 8, valid CRC."""
    route = RouteData(name="tiny", points=(Point(latitude=52.5, longitude=13.4),))
    buf = to_fit_course_bytes(route, time_created=1_700_000_000)

    assert buf[0] == 14  # header size
    assert buf[1] == 0x20  # protocol version 2.0
    # bytes 2-3: profile version (LE u16) — 2100 → b"4\x08"
    assert int.from_bytes(buf[2:4], "little") == 2100
    # data_size at bytes 4-7
    data_size = int.from_bytes(buf[4:8], "little")
    assert buf[8:12] == b".FIT"
    # header CRC at bytes 12-13 — must match CRC of bytes 0..11
    header_crc = int.from_bytes(buf[12:14], "little")
    assert header_crc == _fit_crc16(buf[:12])
    # total length = 14 (header) + data_size + 2 (file CRC)
    assert len(buf) == 14 + data_size + 2


def test_fit_file_crc_valid() -> None:
    """The trailing 2 bytes are a valid CRC-16 over the rest of the file."""
    route = RouteData(name="tiny", points=(Point(latitude=52.5, longitude=13.4),))
    buf = to_fit_course_bytes(route)
    body = buf[:-2]
    file_crc = int.from_bytes(buf[-2:], "little")
    assert file_crc == _fit_crc16(body)


def test_fitparse_round_trip() -> None:
    """A real route survives encode → fitparse decode unchanged.

    Asserts on file_id type, course name, sport, record count, and that
    the first/last positions decode back to the lat/lon we encoded
    (within FIT's semicircle resolution, which is ~2.3 cm).
    """
    points = (
        Point(latitude=52.5200, longitude=13.4050, elevation=34.0),
        Point(latitude=52.5300, longitude=13.4150, elevation=45.0),
        Point(latitude=52.5400, longitude=13.4250, elevation=60.0),
    )
    route = RouteData(name="berlin-loop", points=points)
    buf = to_fit_course_bytes(route, time_created=1_700_000_000)

    fit = _parse(buf)

    # file_id message: type=Course
    file_id_msgs = list(fit.get_messages("file_id"))
    assert len(file_id_msgs) == 1
    fid = file_id_msgs[0]
    assert fid.get_value("type") == "course"

    # course message: name and sport
    course_msgs = list(fit.get_messages("course"))
    assert len(course_msgs) == 1
    cm = course_msgs[0]
    assert cm.get_value("name") == "berlin-loop"
    assert cm.get_value("sport") == "cycling"

    # one record per input point
    record_msgs = list(fit.get_messages("record"))
    assert len(record_msgs) == 3
    # fitparse returns position_lat/long in raw semicircles for record
    # messages (no per-field unit conversion). Convert back manually
    # to verify our encoder.
    semicircle_to_deg = 180.0 / (2**31)
    assert abs(record_msgs[0].get_value("position_lat") * semicircle_to_deg - 52.5200) < 1e-5
    assert abs(record_msgs[0].get_value("position_long") * semicircle_to_deg - 13.4050) < 1e-5
    assert abs(record_msgs[-1].get_value("position_lat") * semicircle_to_deg - 52.5400) < 1e-5
    assert abs(record_msgs[-1].get_value("position_long") * semicircle_to_deg - 13.4250) < 1e-5
    # altitudes decode back too (FIT altitude resolution = 0.2 m)
    assert abs(record_msgs[0].get_value("altitude") - 34.0) < 0.3
    assert abs(record_msgs[-1].get_value("altitude") - 60.0) < 0.3

    # One lap summarising the whole course
    lap_msgs = list(fit.get_messages("lap"))
    assert len(lap_msgs) == 1
    lap = lap_msgs[0]
    assert lap.get_value("total_distance") is not None
    assert lap.get_value("total_distance") > 1000  # >1 km between Berlin points

    # Start + stop events
    event_msgs = list(fit.get_messages("event"))
    event_types = [e.get_value("event_type") for e in event_msgs]
    assert "start" in event_types
    # event_type 9 = stop_disable_all
    assert any(et in ("stop_disable_all", "stop_all") for et in event_types)


def test_fit_long_name_truncates_at_byte_boundary() -> None:
    """A name longer than 15 bytes is truncated and round-trips clean."""
    long_name = "a" * 100
    route = RouteData(name=long_name, points=(Point(latitude=0.1, longitude=0.2),))
    buf = to_fit_course_bytes(route)
    fit = _parse(buf)
    course = next(fit.get_messages("course"))
    # FIT course.name field is 16 bytes incl. null, so up to 15 chars.
    assert course.get_value("name") == "a" * 15


def test_fit_rejects_empty_route() -> None:
    """Encoder refuses an empty point sequence — the device would too."""
    empty = RouteData(name="ghost", points=())
    try:
        to_fit_course_bytes(empty)
    except ValueError:
        return
    raise AssertionError("expected ValueError for empty route")

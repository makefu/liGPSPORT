"""Tests for :mod:`ligpsport.cnx`.

The golden output here is anchored on
``tests/fixtures/cnx_cloud_capture.cnx`` — a real CNX file captured
over BLE while the iGPSPORT Android app uploaded a route to a live
BSC200. That file is the canonical "what the device's parser
accepts" reference; if our encoder drifts, byte-equal assertions on
the structural fields catch it. The full round-trip (encode →
upload → device says status=0) is verified by the live-device test
in ``tests/test_bsc200_live.py``.
"""

from __future__ import annotations

import pathlib
import xml.etree.ElementTree as ET

import pytest

from ligpsport.cnx import Waypoint, parse_gpx_waypoints, to_cnx_bytes
from ligpsport.routes import Point, RouteData

_FIXTURE_DIR = pathlib.Path(__file__).parent / "fixtures"
_CLOUD_CNX = _FIXTURE_DIR / "cnx_cloud_capture.cnx"


def test_cloud_fixture_present() -> None:
    """The capture file is checked in; later tests read structural details from it."""
    assert _CLOUD_CNX.is_file(), f"missing fixture: {_CLOUD_CNX}"
    raw = _CLOUD_CNX.read_bytes()
    # No BOM, starts with the XML declaration.
    assert raw.startswith(b'<?xml version="1.0" encoding="UTF-8"?>'), raw[:50]
    # Self-closing <Navs/> (no space), <Points/>, then PointsCount.
    assert b"<Navs/>" in raw
    assert b"<Points/><PointsCount>" in raw


def test_to_cnx_no_bom_single_line_xml() -> None:
    """Output matches the captured cloud CNX shape: no BOM, no pretty-print."""
    route = RouteData(
        name="round-trip",
        points=(
            Point(latitude=48.7561529, longitude=9.2263629, elevation=552.41),
            Point(latitude=48.7563700, longitude=9.2265800, elevation=552.41),
        ),
    )
    raw = to_cnx_bytes(route, route_id=3130362)
    # No BOM.
    assert not raw.startswith(b"\xef\xbb\xbf")
    # XML declaration matches the captured fixture exactly.
    assert raw.startswith(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    # <Navs/> has no space; <Points/> is self-closing; PointsCount
    # comes AFTER Points (order matters — the captured cloud CNX
    # puts it there too, and so does our encoder).
    assert b"<Navs/>" in raw
    assert b" <Navs" not in raw  # belt and braces against pretty-print regressions
    assert b"<Points/><PointsCount>" in raw


def test_to_cnx_matches_cloud_shape() -> None:
    """The structural fields all parse out of the encoded XML."""
    route = RouteData(
        name="ignored-in-cnx",
        points=(
            Point(latitude=48.7561529, longitude=9.2263629, elevation=552.41),
            Point(latitude=48.7563700, longitude=9.2265800, elevation=552.41),
            Point(latitude=48.7563900, longitude=9.2266000, elevation=553.0),
        ),
    )
    raw = to_cnx_bytes(route, route_id=42)
    root = ET.fromstring(raw)
    assert root.tag == "Route"
    # Element order matches the cloud capture.
    tags = [child.tag for child in root]
    assert tags == [
        "Id",
        "Distance",
        "Duration",
        "Ascent",
        "Descent",
        "Encode",
        "Lang",
        "TracksCount",
        "Tracks",
        "Navs",
        "Points",
        "PointsCount",
    ]
    assert root.findtext("Id") == "42"
    assert root.findtext("Encode") == "2"
    assert root.findtext("Lang") == "0"
    assert root.findtext("TracksCount") == "3"
    assert root.findtext("PointsCount") == "0"
    # Distance keeps 2 decimal places like the cloud (e.g. "8062.16").
    distance = root.findtext("Distance") or ""
    assert "." in distance and len(distance.split(".")[1]) == 2
    # Ascent / Descent are integers (no decimal point) — different
    # from GPXtoCNXConverter's 2dp; matches the cloud capture.
    assert "." not in (root.findtext("Ascent") or "")
    assert "." not in (root.findtext("Descent") or "")
    # Tracks ends with the trailing-`;` terminator and uses the
    # second-difference encoding (one absolute record + N-1 deltas).
    tracks = root.findtext("Tracks") or ""
    assert tracks.endswith(";")
    assert len(tracks.rstrip(";").split(";")) == 3


def test_cloud_fixture_decodes_through_same_parser() -> None:
    """The captured fixture parses through the same path our output does.

    Stronger than ``test_to_cnx_no_bom_single_line_xml``: confirms the
    fixture's structural assumptions still hold (and so the encoder we
    write against them is on solid ground).
    """
    raw = _CLOUD_CNX.read_bytes()
    root = ET.fromstring(raw)
    assert root.tag == "Route"
    tags = [child.tag for child in root]
    assert tags == [
        "Id",
        "Distance",
        "Duration",
        "Ascent",
        "Descent",
        "Encode",
        "Lang",
        "TracksCount",
        "Tracks",
        "Navs",
        "Points",
        "PointsCount",
    ]
    # Confirm the cloud's known cardinality (213 track points, no
    # waypoints) so we notice if someone replaces the fixture.
    assert root.findtext("TracksCount") == "213"
    assert root.findtext("PointsCount") == "0"
    tracks = (root.findtext("Tracks") or "").rstrip(";")
    assert len(tracks.split(";")) == 213


def test_tracks_encoding_second_difference_roundtrip() -> None:
    """Reconstruct absolute coords from the emitted Tracks delta stream."""
    points = (
        Point(latitude=52.5000, longitude=13.4000, elevation=10.0),
        Point(latitude=52.5010, longitude=13.4010, elevation=12.0),
        Point(latitude=52.5025, longitude=13.4020, elevation=11.0),
        Point(latitude=52.5045, longitude=13.4030, elevation=15.0),
    )
    route = RouteData(name="recon", points=points)
    raw = to_cnx_bytes(route, route_id=1)
    root = ET.fromstring(raw)
    tracks = (root.findtext("Tracks") or "").rstrip(";")
    records = [r.split(",") for r in tracks.split(";")]

    abs_lat = float(records[0][0])
    abs_lon = float(records[0][1])
    abs_ele = int(records[0][2]) / 100.0
    assert abs_lat == pytest.approx(52.5000)
    assert abs_lon == pytest.approx(13.4000)
    assert abs_ele == pytest.approx(10.0)

    d_lat = int(records[1][0]) / 1e7
    d_lon = int(records[1][1]) / 1e7
    d_ele = int(records[1][2]) / 100.0
    lat1 = abs_lat + d_lat
    lon1 = abs_lon + d_lon
    ele1 = abs_ele + d_ele
    assert lat1 == pytest.approx(52.5010, abs=1e-7)
    assert lon1 == pytest.approx(13.4010, abs=1e-7)
    assert ele1 == pytest.approx(12.0, abs=1e-2)

    prev_d_lat = int(records[1][0])
    prev_d_lon = int(records[1][1])
    cum_lat = lat1
    cum_lon = lon1
    cum_ele = ele1
    expected = [(52.5025, 13.4020, 11.0), (52.5045, 13.4030, 15.0)]
    for i, (exp_lat, exp_lon, exp_ele) in enumerate(expected):
        dd_lat = int(records[i + 2][0])
        dd_lon = int(records[i + 2][1])
        d_ele = int(records[i + 2][2]) / 100.0
        prev_d_lat += dd_lat
        prev_d_lon += dd_lon
        cum_lat += prev_d_lat / 1e7
        cum_lon += prev_d_lon / 1e7
        cum_ele += d_ele
        assert cum_lat == pytest.approx(exp_lat, abs=1e-7)
        assert cum_lon == pytest.approx(exp_lon, abs=1e-7)
        assert cum_ele == pytest.approx(exp_ele, abs=1e-2)


def test_to_cnx_handles_missing_elevation() -> None:
    """Points without ``ele`` are treated as 0 m — still serialises."""
    route = RouteData(
        name="flat",
        points=(
            Point(latitude=52.5, longitude=13.4, elevation=None),
            Point(latitude=52.6, longitude=13.5, elevation=None),
        ),
    )
    raw = to_cnx_bytes(route)
    root = ET.fromstring(raw)
    assert root.findtext("Ascent") == "0"
    assert root.findtext("Descent") == "0"
    tracks = root.findtext("Tracks") or ""
    assert tracks.startswith("52.5,13.4,0;")


def test_to_cnx_rejects_empty_route() -> None:
    empty = RouteData(name="ghost", points=())
    with pytest.raises(ValueError):
        to_cnx_bytes(empty)


def test_to_cnx_escapes_xml_special_chars_in_waypoint_name() -> None:
    route = RouteData(
        name="x",
        points=(Point(latitude=52.5, longitude=13.4),),
    )
    wpts = (Waypoint(latitude=52.5, longitude=13.4, name="A & <b>", poi_type=14),)
    raw = to_cnx_bytes(route, waypoints=wpts)
    root = ET.fromstring(raw)
    point = root.find("Points/Point")
    assert point is not None
    assert point.findtext("Descr") == "A & <b>"
    assert point.findtext("Type") == "14"


def test_to_cnx_waypoints_render_inline() -> None:
    """Non-empty waypoints expand <Points/> into a <Points>…</Points> block."""
    route = RouteData(name="x", points=(Point(latitude=52.5, longitude=13.4),))
    wpts = (
        Waypoint(latitude=52.5, longitude=13.4, name="start"),
        Waypoint(latitude=52.51, longitude=13.41, name="finish"),
    )
    raw = to_cnx_bytes(route, waypoints=wpts)
    root = ET.fromstring(raw)
    assert root.findtext("PointsCount") == "2"
    points = root.findall("Points/Point")
    assert len(points) == 2
    assert points[0].findtext("Descr") == "start"


def test_parse_gpx_waypoints_extracts_alongside_track() -> None:
    gpx = b"""<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <wpt lat="52.5163" lon="13.3777"><name>start</name></wpt>
  <wpt lat="52.5180" lon="13.3795"><name>finish</name></wpt>
  <trk><name>loop</name><trkseg>
    <trkpt lat="52.5163" lon="13.3777"/>
    <trkpt lat="52.5170" lon="13.3780"/>
  </trkseg></trk>
</gpx>"""
    wpts = parse_gpx_waypoints(gpx)
    assert len(wpts) == 2
    assert wpts[0].name == "start"
    assert wpts[1].latitude == 52.5180


def test_parse_gpx_waypoints_returns_empty_for_track_only() -> None:
    gpx = b"""<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <trk><trkseg><trkpt lat="52.5" lon="13.4"/></trkseg></trk>
</gpx>"""
    assert parse_gpx_waypoints(gpx) == ()

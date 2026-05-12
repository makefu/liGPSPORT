"""Tests for the GPX / geoJSON parser + GPX emitter.

Inputs are realistic (multi-point track segments, real coordinates)
rather than mocked single-point stubs; the haversine distance helper
needs at least a couple of consecutive points to be meaningful.
"""

from __future__ import annotations

import pytest

from ligpsport.routes import (
    Point,
    RouteData,
    RouteParseError,
    parse_geojson,
    parse_gpx,
    to_gpx_bytes,
)

# A small Berlin-area three-point track ~620 m total.
BERLIN_GPX = b"""<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <name>Brandenburg loop</name>
  <trk><name>Brandenburg loop</name><trkseg>
    <trkpt lat="52.5163" lon="13.3777"><ele>35.0</ele></trkpt>
    <trkpt lat="52.5170" lon="13.3780"></trkpt>
    <trkpt lat="52.5178" lon="13.3795"><ele>35.5</ele></trkpt>
  </trkseg></trk>
</gpx>"""


def test_parse_gpx_track() -> None:
    route = parse_gpx(BERLIN_GPX)
    assert route.name == "Brandenburg loop"
    assert len(route.points) == 3
    assert route.points[0].latitude == 52.5163
    assert route.points[0].elevation == 35.0
    assert route.points[1].elevation is None  # no <ele>
    assert 100 < route.distance_m < 5000


def test_parse_gpx_route_fallback() -> None:
    data = b"""<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <rte><name>Brandenburg route</name>
    <rtept lat="52.5163" lon="13.3777"/>
    <rtept lat="52.5170" lon="13.3780"/>
  </rte>
</gpx>"""
    route = parse_gpx(data)
    assert route.name == "Brandenburg route"
    assert len(route.points) == 2


def test_parse_gpx_waypoint_fallback() -> None:
    data = b"""<?xml version="1.0"?>
<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1">
  <wpt lat="52.5163" lon="13.3777"/>
  <wpt lat="52.5170" lon="13.3780"/>
</gpx>"""
    route = parse_gpx(data, default_name="waypoints")
    assert route.name == "waypoints"
    assert len(route.points) == 2


def test_parse_gpx_rejects_garbage() -> None:
    with pytest.raises(RouteParseError):
        parse_gpx(b"not xml at all")


def test_parse_gpx_rejects_empty() -> None:
    data = b'<?xml version="1.0"?><gpx version="1.1"/>'
    with pytest.raises(RouteParseError, match="no <trk>"):
        parse_gpx(data)


def test_parse_geojson_feature_collection_linestring() -> None:
    data = b"""{
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {"name": "Brandenburg loop"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [13.3777, 52.5163, 35.0],
                    [13.3780, 52.5170],
                    [13.3795, 52.5178, 35.5]
                ]
            }
        }]
    }"""
    route = parse_geojson(data)
    assert route.name == "Brandenburg loop"
    assert len(route.points) == 3
    assert route.points[0].latitude == 52.5163
    assert route.points[0].longitude == 13.3777
    assert route.points[0].elevation == 35.0
    assert route.points[1].elevation is None


def test_parse_geojson_bare_linestring() -> None:
    data = b"""{
        "type": "LineString",
        "coordinates": [[13.3, 52.5], [13.4, 52.6]]
    }"""
    route = parse_geojson(data, default_name="anon")
    assert route.name == "anon"
    assert len(route.points) == 2


def test_parse_geojson_multilinestring_concatenates() -> None:
    data = b"""{
        "type": "Feature",
        "properties": {"name": "Two segments"},
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
                [[13.0, 52.5], [13.1, 52.5]],
                [[13.1, 52.5], [13.2, 52.6]]
            ]
        }
    }"""
    route = parse_geojson(data)
    assert len(route.points) == 4


def test_parse_geojson_rejects_garbage() -> None:
    with pytest.raises(RouteParseError):
        parse_geojson(b"not json")


def test_parse_geojson_requires_a_linestring() -> None:
    data = b'{"type": "Point", "coordinates": [13.3, 52.5]}'
    with pytest.raises(RouteParseError):
        parse_geojson(data)


def test_to_gpx_round_trip_preserves_points() -> None:
    original = RouteData(
        name="round-trip",
        points=(
            Point(52.5163, 13.3777, 35.0),
            Point(52.5170, 13.3780, None),
            Point(52.5178, 13.3795, 35.5),
        ),
    )
    wire = to_gpx_bytes(original)
    again = parse_gpx(wire)
    assert again.name == "round-trip"
    assert len(again.points) == 3
    assert again.points[0].latitude == pytest.approx(52.5163)
    assert again.points[0].elevation == 35.0
    assert again.points[1].elevation is None


def test_to_gpx_distance_matches_haversine() -> None:
    # Two points 1 degree apart at the equator ≈ 111.195 km.
    r = RouteData(name="x", points=(Point(0.0, 0.0), Point(0.0, 1.0)))
    assert 110_000 < r.distance_m < 112_000


def test_geojson_to_gpx_via_round_trip() -> None:
    # Critical path: geoJSON in, GPX bytes out, GPX bytes parse back
    # to the same coordinates. This is what `upload-route` does for
    # geoJSON inputs.
    geojson = b"""{
        "type": "LineString",
        "coordinates": [[13.3777, 52.5163], [13.3780, 52.5170]]
    }"""
    parsed = parse_geojson(geojson, default_name="from-geojson")
    gpx = to_gpx_bytes(parsed)
    again = parse_gpx(gpx)
    assert again.name == "from-geojson"
    assert again.points[0].latitude == pytest.approx(52.5163)
    assert again.points[0].longitude == pytest.approx(13.3777)
    assert again.points[1].latitude == pytest.approx(52.5170)

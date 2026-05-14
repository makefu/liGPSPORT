"""CNX (iGPSPORT proprietary) route format encoder, stdlib only.

CNX is the only route format the BSC200 firmware accepts over BLE; the
Android app uploads ``.cnx`` bytes that the iGPSPORT cloud generated
from a user-supplied GPX. This module emits bytes in the same shape
as those cloud outputs so callers can sidestep the cloud round-trip.

The format was reverse-engineered from a captured BLE upload (Android
app to BSC200, firmware 2024-05-14) — see
``tests/fixtures/cnx_cloud_capture.cnx`` for the reference file and
``docs/PROTOCOL.md`` §7.1.2 for the byte-level breakdown.

Captured layout — single-line, ASCII (no BOM):

  <?xml version="1.0" encoding="UTF-8"?>
  <Route>
    <Id>INT</Id>
    <Distance>DEC.2DP</Distance>
    <Duration></Duration>
    <Ascent>INT</Ascent>
    <Descent>INT</Descent>
    <Encode>2</Encode>
    <Lang>0</Lang>
    <TracksCount>N</TracksCount>
    <Tracks>LAT,LON,ELE*100;ΔLAT*1e7,ΔLON*1e7,ΔELE*100;ΔΔLAT,ΔΔLON,ΔELE*100;...</Tracks>
    <Navs/>
    <Points/>          (or <Points><Point>…</Point></Points>)
    <PointsCount>M</PointsCount>
  </Route>

The Tracks delta encoding is identical to the one LudvvigB's
GPXtoCNXConverter (Apache 2.0) reverse-engineered for the desktop
side; the wrapping XML differs (no BOM, no pretty-printing, integer
``<Ascent>`` / ``<Descent>``, ``<Navs/>`` without a space,
``<PointsCount>`` after ``<Points>``). See ``NOTICE`` and
``LICENSES/GPXtoCNXConverter-LICENSE`` for the attribution required
by the Apache license — the Tracks-encoding algorithm is derived
from that project.
"""

from __future__ import annotations

import dataclasses
import math
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Sequence
from decimal import ROUND_HALF_UP, Decimal
from typing import Final
from xml.sax.saxutils import escape as _xml_escape

from .routes import GPX_NAMESPACE, Point, RouteData, RouteParseError, _findall, _findtext


@dataclasses.dataclass(slots=True, frozen=True)
class Waypoint:
    """A point-of-interest entry for the CNX ``<Points>`` list.

    ``poi_type`` indexes into iGPSPORT's icon table (0..22; 0 = plain
    Waypoint). The catalogue is documented in the upstream
    ``GPXtoCNXConverter`` project (``config/poi_types_list.txt``).
    The captured cloud-CNX did not contain waypoints; ``<Point>``
    field order follows the smali ``bbmodel.Point`` bean
    (``Lat``, ``Lng``, ``Descr``) — the upstream tool's extra
    ``<Type>`` field is included since the schema seems to tolerate
    it and POI icons depend on it.
    """

    latitude: float
    longitude: float
    name: str = ""
    poi_type: int = 0


_DEC_2DP: Final[Decimal] = Decimal("0.01")
_DEC_INT: Final[Decimal] = Decimal("1")
_LAT_LON_SCALE: Final[Decimal] = Decimal(10_000_000)
_ELE_SCALE: Final[Decimal] = Decimal(100)
_EARTH_RADIUS_M: Final[Decimal] = Decimal(6_371_000)


def to_cnx_bytes(
    route: RouteData,
    *,
    route_id: int = 1,
    waypoints: Sequence[Waypoint] = (),
    lang: int = 0,
) -> bytes:
    """Serialise *route* as an iGPSPORT CNX byte string.

    The result is ASCII XML on a single line, ready to drop into the
    ``general_file_operation`` upload path (see
    :func:`ligpsport.file_transfer.upload_general_file`).

    *route_id* populates the ``<Id>`` element. The captured cloud
    CNX uses the iGPSPORT cloud's numeric ``RouteId`` (e.g.
    ``3130362``); when generating bytes locally any positive integer
    works — the device storage is keyed by the protobuf-level
    ``file_id`` rather than by this XML field.

    Raises :class:`ValueError` for a route with zero track points.
    """
    if not route.points:
        raise ValueError("can't emit a CNX file for a route with no points")

    metrics = _calculate_metrics(route.points)
    tracks_field = _encode_tracks(route.points)

    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    parts.append("<Route>")
    parts.append(f"<Id>{int(route_id)}</Id>")
    parts.append(f"<Distance>{metrics.distance}</Distance>")
    parts.append("<Duration></Duration>")
    parts.append(f"<Ascent>{metrics.ascent}</Ascent>")
    parts.append(f"<Descent>{metrics.descent}</Descent>")
    parts.append("<Encode>2</Encode>")
    parts.append(f"<Lang>{int(lang)}</Lang>")
    parts.append(f"<TracksCount>{len(route.points)}</TracksCount>")
    parts.append(f"<Tracks>{tracks_field}</Tracks>")
    parts.append("<Navs/>")
    if waypoints:
        parts.append("<Points>")
        for wpt in waypoints:
            parts.append("<Point>")
            parts.append(f"<Lat>{_format_coord(wpt.latitude)}</Lat>")
            parts.append(f"<Lng>{_format_coord(wpt.longitude)}</Lng>")
            parts.append(f"<Type>{int(wpt.poi_type)}</Type>")
            parts.append(f"<Descr>{_xml_escape(wpt.name)}</Descr>")
            parts.append("</Point>")
        parts.append("</Points>")
    else:
        # Captured cloud CNX uses self-closing <Points/> for empty.
        parts.append("<Points/>")
    parts.append(f"<PointsCount>{len(waypoints)}</PointsCount>")
    parts.append("</Route>")

    return "".join(parts).encode("utf-8")


# ---- Metrics --------------------------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class _Metrics:
    distance: str  # metres, 2dp string ("8062.16")
    ascent: str  # metres, INTEGER string ("181")
    descent: str  # metres, INTEGER string (negative or "0")


def _calculate_metrics(points: Sequence[Point]) -> _Metrics:
    """Sum 3D haversine distance and split ele deltas into ascent / descent.

    Distance keeps 2 decimal places (the captured cloud CNX shows
    e.g. ``8062.16``); ascent/descent are stored as integers
    (``181``, ``-200``) — different from the GPXtoCNXConverter
    desktop tool, which emits 2dp on all three. Matches the cloud
    output byte-for-byte.
    """
    distance = Decimal(0)
    ascent = Decimal(0)
    descent = Decimal(0)

    prev = None
    for p in points:
        if prev is not None:
            distance += _haversine_3d_m(prev, p)
            ele_diff = _ele(p) - _ele(prev)
            if ele_diff > 0:
                ascent += ele_diff
            else:
                descent += ele_diff
            distance = distance.quantize(_DEC_2DP, rounding=ROUND_HALF_UP)
        prev = p

    return _Metrics(
        distance=str(distance.quantize(_DEC_2DP, rounding=ROUND_HALF_UP)),
        ascent=str(int(ascent.quantize(_DEC_INT, rounding=ROUND_HALF_UP))),
        descent=str(int(descent.quantize(_DEC_INT, rounding=ROUND_HALF_UP))),
    )


def _ele(p: Point) -> Decimal:
    """Elevation as Decimal, defaulting missing values to 0.0 metres."""
    if p.elevation is None:
        return Decimal(0)
    return Decimal(repr(p.elevation))


def _haversine_3d_m(a: Point, b: Point) -> Decimal:
    """3D great-circle distance between *a* and *b*, in metres.

    Uses a 6371 km Earth radius — matches the upstream
    GPXtoCNXConverter formula (and, as far as we can tell, the
    cloud's). Result is a :class:`Decimal` so callers can sum
    without float drift.
    """
    lat1 = math.radians(a.latitude)
    lat2 = math.radians(b.latitude)
    dlat = math.radians(b.latitude - a.latitude)
    dlon = math.radians(b.longitude - a.longitude)
    sin_dlat = math.sin(dlat / 2)
    sin_dlon = math.sin(dlon / 2)
    h = sin_dlat * sin_dlat + math.cos(lat1) * math.cos(lat2) * sin_dlon * sin_dlon
    angle = 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))
    horizontal = _EARTH_RADIUS_M * Decimal(repr(angle))
    ele_diff = _ele(b) - _ele(a)
    horiz_sq = horizontal * horizontal
    ele_sq = ele_diff * ele_diff
    return (horiz_sq + ele_sq).sqrt()


# ---- Tracks encoding ------------------------------------------------


def _encode_tracks(points: Sequence[Point]) -> str:
    """Build the CNX ``<Tracks>`` field for *points*.

    Output is a ``;``-separated, semicolon-terminated string.
    Algorithm derived from GPXtoCNXConverter (Apache 2.0). The
    captured cloud CNX uses the same scheme — first record absolute,
    second record first-difference, subsequent records second-
    difference for lat/lon and first-difference for elevation.
    """
    records: list[str] = []

    first = points[0]
    first_lat = _format_coord(first.latitude)
    first_lon = _format_coord(first.longitude)
    first_ele = _round_half_up(_ele(first) * _ELE_SCALE)
    records.append(f"{first_lat},{first_lon},{first_ele}")

    first_diffs: list[tuple[Decimal, Decimal, Decimal]] = []
    for i in range(1, len(points)):
        a = points[i - 1]
        b = points[i]
        d_lat = (Decimal(repr(b.latitude)) - Decimal(repr(a.latitude))) * _LAT_LON_SCALE
        d_lon = (Decimal(repr(b.longitude)) - Decimal(repr(a.longitude))) * _LAT_LON_SCALE
        d_ele = _ele(b) * _ELE_SCALE - _ele(a) * _ELE_SCALE
        first_diffs.append((d_lat, d_lon, d_ele))

    if first_diffs:
        d_lat, d_lon, d_ele = first_diffs[0]
        records.append(f"{_round_half_up(d_lat)},{_round_half_up(d_lon)},{_round_half_up(d_ele)}")

    for i in range(1, len(first_diffs)):
        dd_lat = first_diffs[i][0] - first_diffs[i - 1][0]
        dd_lon = first_diffs[i][1] - first_diffs[i - 1][1]
        d_ele = first_diffs[i][2]
        records.append(f"{_round_half_up(dd_lat)},{_round_half_up(dd_lon)},{_round_half_up(d_ele)}")

    # Trailing `;` matches both the cloud capture and the upstream
    # GPXtoCNXConverter — the iGPSPORT parser uses it as a record
    # terminator, not a separator.
    return ";".join(records) + ";"


def _round_half_up(v: Decimal) -> int:
    """Round *v* to the nearest integer using ROUND_HALF_UP."""
    return int(v.quantize(_DEC_INT, rounding=ROUND_HALF_UP))


# ---- Coordinate formatting -----------------------------------------


def _format_coord(v: float) -> str:
    """Format a degree value for the absolute lat/lon at record 0.

    Up to 7 decimal places, trailing zeros stripped — matches the
    cloud output (``48.7561529``, ``9.2263629`` in the captured
    file).

    **Locale gotcha for porters:** the CNX ``<Tracks>`` field uses
    commas as record-field separators, so the absolute coordinates
    at record 0 **must** use a period as their decimal separator.
    Python's f-string ``f"{v:.7f}"`` and ``%``-format are
    locale-independent (only the ``:n`` format spec consults
    ``locale.localeconv``), so this implementation is safe regardless
    of ``LC_NUMERIC``. Other ports are not: Kotlin/Java
    ``"%.7f".format(v)`` honours ``Locale.getDefault()`` and emits
    ``"48,7561529"`` on a de_DE phone, corrupting the first record
    so the BSC200 parser falls off the rails (observed: an on-device
    goal distance of 693 km for a route that's actually 9 km long).
    Pin to ``Locale.ROOT`` in any non-Python port.
    """
    s = f"{v:.7f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ---- GPX waypoint extraction ---------------------------------------


def parse_gpx_waypoints(data: bytes) -> tuple[Waypoint, ...]:
    """Pull standalone ``<wpt>`` elements out of a GPX byte string."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise RouteParseError(f"invalid GPX XML: {exc}") from exc
    return tuple(_iter_waypoints(_findall(root, "wpt")))


def _iter_waypoints(elements: Iterable[ET.Element]) -> Iterable[Waypoint]:
    for el in elements:
        try:
            lat = float(el.attrib["lat"])
            lon = float(el.attrib["lon"])
        except (KeyError, ValueError):
            continue
        name = _findtext(el, "name") or ""
        yield Waypoint(latitude=lat, longitude=lon, name=name)


# Keep the GPX_NAMESPACE re-export for downstream consumers.
_ = GPX_NAMESPACE

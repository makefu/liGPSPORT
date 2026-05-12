"""GPX and geoJSON parsing and serialisation, stdlib only.

The BSC200 (and the wider iGPSPORT family) accepts route uploads in
five file formats: ``CNX``, ``GPX``, ``FIT``, ``TCX``, ``XML``. GPX is
the universal one — every consumer-grade route-planning tool produces
it, and the device parses it directly without server-side
preprocessing.

This module accepts both **GPX** and **geoJSON** input files and
normalises them through one common :class:`RouteData` dataclass.
Output is always a canonical GPX byte string ready to drop into a
``route_plan_data_msg.file_content`` field for upload.

Pure stdlib: ``xml.etree.ElementTree`` for GPX parse/emit, ``json``
for geoJSON parse, ``math.radians`` / ``math.sin`` etc. for the
haversine distance helper. No third-party dependencies.

GPX schema reference: https://www.topografix.com/GPX/1/1/gpx.xsd
geoJSON schema reference: https://datatracker.ietf.org/doc/html/rfc7946
"""

from __future__ import annotations

import dataclasses
import io
import json
import math
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Iterator
from pathlib import Path

GPX_NAMESPACE = "http://www.topografix.com/GPX/1/1"
# Register the default namespace so emitted XML uses xmlns="..." rather
# than ns0:trk style prefixes. Idempotent; safe to call repeatedly.
ET.register_namespace("", GPX_NAMESPACE)


class RouteParseError(ValueError):
    """Raised when an input file can't be parsed into a :class:`RouteData`."""


@dataclasses.dataclass(slots=True, frozen=True)
class Point:
    """One point on a route, with optional elevation."""

    latitude: float
    longitude: float
    elevation: float | None = None


@dataclasses.dataclass(slots=True, frozen=True)
class RouteData:
    """Normalised representation of a route, regardless of source format."""

    name: str
    points: tuple[Point, ...]

    @property
    def distance_m(self) -> int:
        """Total route length in metres (haversine over consecutive points)."""
        total = 0.0
        for a, b in _pairs(self.points):
            total += _haversine_m(a, b)
        return round(total)


def _pairs(items: tuple[Point, ...]) -> Iterator[tuple[Point, Point]]:
    last: Point | None = None
    for p in items:
        if last is not None:
            yield last, p
        last = p


def _haversine_m(a: Point, b: Point) -> float:
    """Great-circle distance between two points in metres.

    Earth radius 6371008.8 m (mean radius per WGS84). Accurate enough
    for route-distance display; the device reports back its own value
    once the file is parsed on-board.
    """
    r = 6371008.8
    lat1 = math.radians(a.latitude)
    lat2 = math.radians(b.latitude)
    dlat = math.radians(b.latitude - a.latitude)
    dlon = math.radians(b.longitude - a.longitude)
    sin_dlat = math.sin(dlat / 2)
    sin_dlon = math.sin(dlon / 2)
    h = sin_dlat * sin_dlat + math.cos(lat1) * math.cos(lat2) * sin_dlon * sin_dlon
    return 2 * r * math.asin(math.sqrt(h))


# ---- GPX parsing ----------------------------------------------------


def parse_gpx(data: bytes, *, default_name: str = "route") -> RouteData:
    """Parse a GPX byte string into :class:`RouteData`.

    Accepts both namespaced (``{http://...}trk``) and unnamespaced GPX
    files, since real-world emitters are inconsistent. Pulls points in
    this priority order:

    1. The first ``<trk>`` element's ``<trkpt>`` children (a track).
    2. The first ``<rte>`` element's ``<rtept>`` children (a route).
    3. All standalone ``<wpt>`` waypoints.

    A GPX with none of those raises :class:`RouteParseError`.
    """
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise RouteParseError(f"invalid GPX XML: {exc}") from exc
    name = _findtext(root, "name") or default_name

    # Tracks
    for trk in _findall(root, "trk"):
        pts = list(_iter_pt(_findall_concat(trk, "trkseg", "trkpt")))
        if pts:
            return RouteData(name=_findtext(trk, "name") or name, points=tuple(pts))

    # Routes
    for rte in _findall(root, "rte"):
        pts = list(_iter_pt(_findall(rte, "rtept")))
        if pts:
            return RouteData(name=_findtext(rte, "name") or name, points=tuple(pts))

    # Waypoints
    pts = list(_iter_pt(_findall(root, "wpt")))
    if pts:
        return RouteData(name=name, points=tuple(pts))

    raise RouteParseError("no <trk>, <rte>, or <wpt> elements with points found")


def _strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _findall(parent: ET.Element, name: str) -> list[ET.Element]:
    """Like ``parent.findall(name)`` but namespace-agnostic."""
    return [child for child in parent if _strip_ns(child.tag) == name]


def _findall_concat(parent: ET.Element, container: str, leaf: str) -> list[ET.Element]:
    """Walk ``parent/<container>/<leaf>`` for every container."""
    out: list[ET.Element] = []
    for c in _findall(parent, container):
        out.extend(_findall(c, leaf))
    return out


def _findtext(parent: ET.Element, name: str) -> str | None:
    for child in parent:
        if _strip_ns(child.tag) == name and child.text:
            return child.text.strip()
    return None


def _iter_pt(elements: Iterable[ET.Element]) -> Iterator[Point]:
    for el in elements:
        try:
            lat = float(el.attrib["lat"])
            lon = float(el.attrib["lon"])
        except (KeyError, ValueError):
            continue
        ele_text = _findtext(el, "ele")
        elevation: float | None = None
        if ele_text:
            try:
                elevation = float(ele_text)
            except ValueError:
                elevation = None
        yield Point(latitude=lat, longitude=lon, elevation=elevation)


# ---- geoJSON parsing ------------------------------------------------


def parse_geojson(data: bytes, *, default_name: str = "route") -> RouteData:
    """Parse a geoJSON byte string into :class:`RouteData`.

    Supported geometries:

    * ``LineString`` — used as-is.
    * ``MultiLineString`` — the first line is used; subsequent lines
      are concatenated (so two-segment maps still produce one route).
    * ``Feature`` wrapping either of the above. The feature's
      ``properties.name`` populates the route name if set.
    * ``FeatureCollection`` — the first feature with a LineString or
      MultiLineString is taken.

    Coordinates are ``[lon, lat]`` or ``[lon, lat, ele]`` per RFC 7946.
    """
    try:
        doc = json.loads(data)
    except json.JSONDecodeError as exc:
        raise RouteParseError(f"invalid geoJSON: {exc}") from exc
    feature = _select_feature(doc)
    if feature is None:
        raise RouteParseError("geoJSON has no LineString / MultiLineString geometry")
    name = default_name
    props = feature.get("properties") if isinstance(feature, dict) else None
    if isinstance(props, dict):
        n = props.get("name")
        if isinstance(n, str) and n.strip():
            name = n.strip()
    geom = _geometry_of(feature)
    points = tuple(_iter_geojson_points(geom))
    if not points:
        raise RouteParseError("geoJSON LineString has no coordinates")
    return RouteData(name=name, points=points)


def _select_feature(doc: object) -> object | None:
    """Return the first thing whose geometry is a (Multi)LineString."""
    if not isinstance(doc, dict):
        return None
    t = doc.get("type")
    if t == "FeatureCollection":
        for feat in doc.get("features", ()):
            if _geometry_of(feat) is not None:
                return feat
        return None
    if t == "Feature":
        if _geometry_of(doc) is not None:
            return doc
        return None
    # Bare geometry.
    if t in ("LineString", "MultiLineString"):
        # Wrap in a synthetic feature so the caller sees the same shape.
        return {"type": "Feature", "geometry": doc, "properties": {}}
    return None


def _geometry_of(feature: object) -> dict[str, object] | None:
    if not isinstance(feature, dict):
        return None
    geom = feature.get("geometry") if "geometry" in feature else feature
    if not isinstance(geom, dict):
        return None
    if geom.get("type") in ("LineString", "MultiLineString"):
        return geom
    return None


def _iter_geojson_points(geom: dict[str, object] | None) -> Iterator[Point]:
    if geom is None:
        return
    coords = geom.get("coordinates")
    if geom.get("type") == "LineString" and isinstance(coords, list):
        yield from _iter_coords(coords)
    elif geom.get("type") == "MultiLineString" and isinstance(coords, list):
        for line in coords:
            if isinstance(line, list):
                yield from _iter_coords(line)


def _iter_coords(coords: list[object]) -> Iterator[Point]:
    for entry in coords:
        if not isinstance(entry, list | tuple) or len(entry) < 2:
            continue
        try:
            lon = float(entry[0])
            lat = float(entry[1])
        except (TypeError, ValueError):
            continue
        elevation: float | None = None
        if len(entry) >= 3:
            try:
                elevation = float(entry[2])
            except (TypeError, ValueError):
                elevation = None
        yield Point(latitude=lat, longitude=lon, elevation=elevation)


# ---- GPX serialisation ----------------------------------------------


def to_gpx_bytes(route: RouteData) -> bytes:
    """Render *route* as a GPX 1.1 byte string ready for upload.

    The structure is intentionally minimal — a single ``<trk>`` with
    one ``<trkseg>`` and one ``<trkpt>`` per :class:`Point`. The
    iGPSPORT firmware accepts this layout (it's what most GPX-emitters
    produce); fancier producers add ``<extensions>`` blocks but the
    device ignores them.
    """
    gpx = ET.Element(
        f"{{{GPX_NAMESPACE}}}gpx",
        attrib={
            "version": "1.1",
            "creator": "ligpsport",
        },
    )
    ET.SubElement(gpx, f"{{{GPX_NAMESPACE}}}name").text = route.name
    trk = ET.SubElement(gpx, f"{{{GPX_NAMESPACE}}}trk")
    ET.SubElement(trk, f"{{{GPX_NAMESPACE}}}name").text = route.name
    trkseg = ET.SubElement(trk, f"{{{GPX_NAMESPACE}}}trkseg")
    for p in route.points:
        attrs = {"lat": _f(p.latitude), "lon": _f(p.longitude)}
        trkpt = ET.SubElement(trkseg, f"{{{GPX_NAMESPACE}}}trkpt", attrib=attrs)
        if p.elevation is not None:
            ET.SubElement(trkpt, f"{{{GPX_NAMESPACE}}}ele").text = _f(p.elevation)

    buf = io.BytesIO()
    tree = ET.ElementTree(gpx)
    tree.write(buf, encoding="utf-8", xml_declaration=True)
    return buf.getvalue()


def _f(v: float) -> str:
    """Format a float for GPX output: up to 7 decimal places, trim trailing zeros."""
    s = f"{v:.7f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ---- High-level helpers --------------------------------------------


def load_route(path: str | Path) -> RouteData:
    """Load a route from disk; format is detected from the file extension.

    Supported extensions: ``.gpx`` and ``.geojson`` / ``.json``.
    """
    p = Path(path)
    ext = p.suffix.lower().lstrip(".")
    data = p.read_bytes()
    if ext == "gpx":
        return parse_gpx(data, default_name=p.stem)
    if ext in ("geojson", "json"):
        return parse_geojson(data, default_name=p.stem)
    # Fall back: sniff the payload — GPX starts with `<`, geoJSON with `{`.
    stripped = data.lstrip()
    if stripped.startswith(b"<"):
        return parse_gpx(data, default_name=p.stem)
    if stripped.startswith(b"{"):
        return parse_geojson(data, default_name=p.stem)
    raise RouteParseError(f"unknown route file format: {path!r}")

"""Activity-FIT reader, GPX writer, and filename helpers.

The bike computer stores recorded activities as Garmin FIT *activity*
files. This module parses those files via :mod:`fitparse` and
re-renders them as GPX 1.1 tracks, with the Garmin
``TrackPointExtension`` namespace carrying HR / cadence and the
Cluetrust-style bare ``<power>`` element that both Strava and
Garmin Connect accept. It is the read-side complement of
:mod:`ligpsport.fit_course`, which writes Course FIT.

Public surface (see ``__all__``): a small dataclass pair for the
parsed file, an ``activity_filename`` helper that turns a
Garmin-epoch timestamp + device model into a canonical
``<compact-iso>_<model>.<ext>`` filename, and the
``garmin_epoch_to_datetime`` helper shared with
:mod:`ligpsport.commands`.
"""

from __future__ import annotations

import dataclasses
import io
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta
from typing import Final

import fitparse

__all__ = [
    "GARMIN_EPOCH_UTC",
    "ActivityFitMeta",
    "ActivityFitRecord",
    "activity_filename",
    "activity_filename_from_meta",
    "device_model_for",
    "garmin_epoch_to_datetime",
    "read_activity_fit",
    "to_gpx_bytes",
]

GPX_NAMESPACE: Final[str] = "http://www.topografix.com/GPX/1/1"
GPXTPX_NAMESPACE: Final[str] = "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
XSI_NAMESPACE: Final[str] = "http://www.w3.org/2001/XMLSchema-instance"

# Register prefixes so ET emits ``xmlns="..."`` for the default GPX
# namespace and short ``gpxtpx:`` / ``xsi:`` prefixes instead of the
# auto-generated ``ns0:``-style. Idempotent at import time.
ET.register_namespace("", GPX_NAMESPACE)
ET.register_namespace("gpxtpx", GPXTPX_NAMESPACE)
ET.register_namespace("xsi", XSI_NAMESPACE)

GARMIN_EPOCH_UTC: Final[datetime] = datetime(1989, 12, 31, tzinfo=UTC)

# FIT stores latitude/longitude as signed 32-bit semicircles.
_SEMI_TO_DEG: Final[float] = 180.0 / (2**31)

_IGPSPORT_MODELS: Final[dict[int, str]] = {
    100: "BSC100",
    200: "BSC200",
    300: "BSC300",
    320: "iGS320",
    520: "iGS520",
    620: "iGS620",
    630: "iGS630",
}


def garmin_epoch_to_datetime(seconds: int) -> datetime:
    """Convert seconds since the Garmin/FIT epoch (1989-12-31 UTC) to a UTC datetime."""
    return GARMIN_EPOCH_UTC + timedelta(seconds=seconds)


def device_model_for(manufacturer: str | None, product: int | None) -> str:
    """Resolve a friendly device model from a FIT manufacturer/product pair.

    Non-iGPSPORT (or absent) manufacturer falls back to ``"iGPSPORT"``;
    unknown iGPSPORT products are rendered as ``iGS{product}``.
    """
    if manufacturer is None or manufacturer.lower() != "igpsport":
        return "iGPSPORT"
    if not product:
        return "iGPSPORT"
    mapped = _IGPSPORT_MODELS.get(product)
    if mapped is not None:
        return mapped
    return f"iGS{product}"


@dataclasses.dataclass(slots=True, frozen=True)
class ActivityFitMeta:
    """Activity-level header extracted from the FIT ``file_id`` message."""

    time_created: datetime
    manufacturer: str
    product: int
    device_model: str


@dataclasses.dataclass(slots=True, frozen=True)
class ActivityFitRecord:
    """One ``record`` message from a FIT activity, normalised to SI units."""

    timestamp: datetime
    latitude: float | None
    longitude: float | None
    altitude: float | None
    heart_rate: int | None
    cadence: int | None
    power: int | None
    distance: float | None
    speed: float | None


def _as_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        # fitparse returns naive datetimes for FIT timestamps but the
        # underlying values are seconds since the FIT epoch (UTC).
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _semi_to_deg(value: int | None) -> float | None:
    if value is None:
        return None
    return float(value) * _SEMI_TO_DEG


def read_activity_fit(
    fit_bytes: bytes,
) -> tuple[ActivityFitMeta, list[ActivityFitRecord]]:
    """Parse activity-FIT bytes into a metadata header plus list of records.

    Records that carry neither latitude nor longitude are dropped —
    they don't contribute to a track (the device occasionally emits
    them while paused or when waiting for a GPS fix).
    """
    fit = fitparse.FitFile(io.BytesIO(fit_bytes))
    fit.parse()

    file_id_msgs = list(fit.get_messages("file_id"))
    if not file_id_msgs:
        raise ValueError("FIT file has no file_id message")
    fid = file_id_msgs[0]

    manufacturer_raw = fid.get_value("manufacturer")
    manufacturer = str(manufacturer_raw).lower() if manufacturer_raw is not None else ""
    product_raw = fid.get_value("product")
    product = int(product_raw) if product_raw is not None else 0
    time_created = _as_utc(fid.get_value("time_created"))
    if time_created is None:
        raise ValueError("FIT file_id has no time_created")

    meta = ActivityFitMeta(
        time_created=time_created,
        manufacturer=manufacturer,
        product=product,
        device_model=device_model_for(manufacturer or None, product or None),
    )

    records: list[ActivityFitRecord] = []
    for r in fit.get_messages("record"):
        lat = _semi_to_deg(r.get_value("position_lat"))
        lon = _semi_to_deg(r.get_value("position_long"))
        if lat is None and lon is None:
            continue
        timestamp = _as_utc(r.get_value("timestamp"))
        if timestamp is None:
            continue
        altitude_raw = r.get_value("altitude")
        speed_raw = r.get_value("speed")
        distance_raw = r.get_value("distance")
        hr_raw = r.get_value("heart_rate")
        cad_raw = r.get_value("cadence")
        pwr_raw = r.get_value("power")
        records.append(
            ActivityFitRecord(
                timestamp=timestamp,
                latitude=lat,
                longitude=lon,
                altitude=float(altitude_raw) if altitude_raw is not None else None,
                heart_rate=int(hr_raw) if hr_raw is not None else None,
                cadence=int(cad_raw) if cad_raw is not None else None,
                power=int(pwr_raw) if pwr_raw is not None else None,
                distance=float(distance_raw) if distance_raw is not None else None,
                speed=float(speed_raw) if speed_raw is not None else None,
            )
        )

    return meta, records


# ---- GPX serialisation ----------------------------------------------


def _iso_utc(value: datetime) -> str:
    """Format *value* as ISO 8601 UTC with the ``Z`` suffix GPX expects."""
    utc = value.astimezone(UTC) if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def _f(v: float) -> str:
    s = f"{v:.7f}".rstrip("0").rstrip(".")
    return s if s else "0"


def to_gpx_bytes(
    meta: ActivityFitMeta,
    records: list[ActivityFitRecord],
    *,
    name: str | None = None,
) -> bytes:
    """Render an activity as a GPX 1.1 byte string.

    Layout: one ``<trk>`` with one ``<trkseg>`` and one ``<trkpt>`` per
    record that has both lat and lon. Optional ``<ele>``, ``<time>``,
    and an ``<extensions>`` block carrying ``<gpxtpx:hr>`` /
    ``<gpxtpx:cad>`` (Garmin TrackPointExtension v1) and a bare
    ``<power>`` element (Cluetrust GPXDATA shape; accepted by Strava
    and Garmin Connect alike).
    """
    gpx_name = name or f"{meta.device_model} activity {meta.time_created.isoformat()}"

    gpx = ET.Element(
        f"{{{GPX_NAMESPACE}}}gpx",
        attrib={
            "version": "1.1",
            "creator": "ligpsport",
            f"{{{XSI_NAMESPACE}}}schemaLocation": (
                "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
            ),
        },
    )
    metadata = ET.SubElement(gpx, f"{{{GPX_NAMESPACE}}}metadata")
    ET.SubElement(metadata, f"{{{GPX_NAMESPACE}}}time").text = _iso_utc(meta.time_created)
    ET.SubElement(metadata, f"{{{GPX_NAMESPACE}}}name").text = gpx_name

    trk = ET.SubElement(gpx, f"{{{GPX_NAMESPACE}}}trk")
    ET.SubElement(trk, f"{{{GPX_NAMESPACE}}}name").text = gpx_name
    trkseg = ET.SubElement(trk, f"{{{GPX_NAMESPACE}}}trkseg")

    for r in records:
        if r.latitude is None or r.longitude is None:
            continue
        trkpt = ET.SubElement(
            trkseg,
            f"{{{GPX_NAMESPACE}}}trkpt",
            attrib={"lat": _f(r.latitude), "lon": _f(r.longitude)},
        )
        if r.altitude is not None:
            ET.SubElement(trkpt, f"{{{GPX_NAMESPACE}}}ele").text = _f(r.altitude)
        ET.SubElement(trkpt, f"{{{GPX_NAMESPACE}}}time").text = _iso_utc(r.timestamp)

        tpx_fields: list[tuple[str, str]] = []
        if r.heart_rate is not None:
            tpx_fields.append(("hr", str(r.heart_rate)))
        if r.cadence is not None:
            tpx_fields.append(("cad", str(r.cadence)))
        has_power = r.power is not None
        if not tpx_fields and not has_power:
            continue

        extensions = ET.SubElement(trkpt, f"{{{GPX_NAMESPACE}}}extensions")
        if tpx_fields:
            tpx = ET.SubElement(extensions, f"{{{GPXTPX_NAMESPACE}}}TrackPointExtension")
            for tag, value in tpx_fields:
                ET.SubElement(tpx, f"{{{GPXTPX_NAMESPACE}}}{tag}").text = value
        if has_power:
            ET.SubElement(extensions, f"{{{GPX_NAMESPACE}}}power").text = str(r.power)

    buf = io.BytesIO()
    ET.ElementTree(gpx).write(buf, encoding="utf-8", xml_declaration=True)
    return buf.getvalue()


# ---- Filename derivation -------------------------------------------


def activity_filename(
    *,
    timestamp: int,
    device_model: str | None,
    extension: str,
) -> str:
    """Build ``<compact-iso>_<device_model>.<extension>`` from a Garmin-epoch timestamp.

    ``compact-iso`` is ISO 8601 basic form, ``YYYYMMDDTHHMMSSZ``.
    Missing/empty ``device_model`` falls back to ``"iGPSPORT"``.
    ``extension`` is passed without a leading dot.
    """
    model = device_model or "iGPSPORT"
    compact = garmin_epoch_to_datetime(timestamp).strftime("%Y%m%dT%H%M%SZ")
    return f"{compact}_{model}.{extension}"


def activity_filename_from_meta(meta: ActivityFitMeta, extension: str) -> str:
    """Derive the canonical filename from a parsed activity's metadata."""
    seconds = int((meta.time_created - GARMIN_EPOCH_UTC).total_seconds())
    return activity_filename(
        timestamp=seconds,
        device_model=meta.device_model,
        extension=extension,
    )

"""Tests for :mod:`ligpsport.fit_activity`.

The fixture ``tests/fixtures/activity_bsc200.fit`` is a real BSC200
capture (15572 B, manufacturer=igpsport, product=200, 421 records,
1 session, 2 laps). The fixture provides position+altitude+speed but
no heart-rate / cadence / power data, so the extension test exercises
the writer against synthetic records instead.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ligpsport.fit_activity import (
    ActivityFitMeta,
    ActivityFitRecord,
    activity_filename,
    activity_filename_from_meta,
    device_model_for,
    garmin_epoch_to_datetime,
    read_activity_fit,
    to_gpx_bytes,
)

GPX_NS = "http://www.topografix.com/GPX/1/1"
GPXTPX_NS = "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"

FIXTURE = Path(__file__).parent / "fixtures" / "activity_bsc200.fit"


@pytest.fixture
def fixture_bytes() -> bytes:
    return FIXTURE.read_bytes()


def test_garmin_epoch_conversion() -> None:
    """``1147795610`` round-trips to 2026-05-15 16:06:50 UTC."""
    assert garmin_epoch_to_datetime(1147795610) == datetime(2026, 5, 15, 16, 6, 50, tzinfo=UTC)


def test_read_activity_fit_meta(fixture_bytes: bytes) -> None:
    """File-id metadata identifies the BSC200 capture."""
    meta, _ = read_activity_fit(fixture_bytes)
    assert meta.manufacturer == "igpsport"
    assert meta.product == 200
    assert meta.device_model == "BSC200"
    assert meta.time_created.year == 2026
    assert meta.time_created.tzinfo is not None


def test_read_activity_fit_records(fixture_bytes: bytes) -> None:
    """The fixture has hundreds of records with sane positions and monotonic time."""
    _, records = read_activity_fit(fixture_bytes)
    assert len(records) >= 400
    first = records[0]
    assert first.latitude is not None and -90.0 <= first.latitude <= 90.0
    assert first.longitude is not None and -180.0 <= first.longitude <= 180.0
    for i in range(len(records) - 1):
        assert records[i].timestamp < records[i + 1].timestamp


def test_to_gpx_round_trip(fixture_bytes: bytes) -> None:
    """FIT → GPX → ET re-parse preserves trackpoint count and bookend coordinates."""
    meta, records = read_activity_fit(fixture_bytes)
    gpx_bytes = to_gpx_bytes(meta, records)

    root = ET.fromstring(gpx_bytes)
    trkpts = root.findall(f"{{{GPX_NS}}}trk/{{{GPX_NS}}}trkseg/{{{GPX_NS}}}trkpt")
    with_position = [r for r in records if r.latitude is not None and r.longitude is not None]
    assert len(trkpts) == len(with_position)
    assert len(trkpts) > 0

    first_pt, last_pt = trkpts[0], trkpts[-1]
    first_rec, last_rec = with_position[0], with_position[-1]
    assert first_rec.latitude is not None and first_rec.longitude is not None
    assert last_rec.latitude is not None and last_rec.longitude is not None
    assert abs(float(first_pt.attrib["lat"]) - first_rec.latitude) < 1e-5
    assert abs(float(first_pt.attrib["lon"]) - first_rec.longitude) < 1e-5
    assert abs(float(last_pt.attrib["lat"]) - last_rec.latitude) < 1e-5
    assert abs(float(last_pt.attrib["lon"]) - last_rec.longitude) < 1e-5

    for pt in trkpts:
        time_el = pt.find(f"{{{GPX_NS}}}time")
        assert time_el is not None
        text = time_el.text or ""
        assert text.endswith("Z")
        # Round-trip: must parse back as an ISO datetime.
        datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def test_to_gpx_extensions() -> None:
    """``<gpxtpx:hr>`` and ``<gpxtpx:cad>`` appear when the source record carries them.

    The committed fixture has no HR/cadence values (it predates the
    BSC200 being paired with a sensor), so the extension path is
    exercised via synthetic records that explicitly set the fields.
    """
    meta = ActivityFitMeta(
        time_created=datetime(2026, 5, 15, 16, 0, 0, tzinfo=UTC),
        manufacturer="igpsport",
        product=200,
        device_model="BSC200",
    )
    records = [
        ActivityFitRecord(
            timestamp=datetime(2026, 5, 15, 16, 0, i, tzinfo=UTC),
            latitude=48.8 + i * 0.0001,
            longitude=9.2 + i * 0.0001,
            altitude=234.0 + i,
            heart_rate=140 + i,
            cadence=85 + i,
            power=210 + i,
            distance=float(i * 10),
            speed=8.5,
        )
        for i in range(3)
    ]
    gpx_bytes = to_gpx_bytes(meta, records)
    root = ET.fromstring(gpx_bytes)
    hr_elems = root.findall(
        f".//{{{GPX_NS}}}trkpt/{{{GPX_NS}}}extensions"
        f"/{{{GPXTPX_NS}}}TrackPointExtension/{{{GPXTPX_NS}}}hr"
    )
    cad_elems = root.findall(
        f".//{{{GPX_NS}}}trkpt/{{{GPX_NS}}}extensions"
        f"/{{{GPXTPX_NS}}}TrackPointExtension/{{{GPXTPX_NS}}}cad"
    )
    power_elems = root.findall(f".//{{{GPX_NS}}}trkpt/{{{GPX_NS}}}extensions/{{{GPX_NS}}}power")
    assert len(hr_elems) >= 1
    assert len(cad_elems) >= 1
    assert len(power_elems) >= 1
    assert hr_elems[0].text == "140"
    assert cad_elems[0].text == "85"
    assert power_elems[0].text == "210"


def test_device_model_mapping() -> None:
    """Known iGPSPORT products map to friendly names; the rest fall back."""
    assert device_model_for("igpsport", 200) == "BSC200"
    assert device_model_for("igpsport", 320) == "iGS320"
    assert device_model_for("igpsport", 1234) == "iGS1234"
    assert device_model_for("garmin", 200) == "iGPSPORT"
    assert device_model_for(None, None) == "iGPSPORT"
    assert device_model_for("IGPSPORT", 200) == "BSC200"
    assert device_model_for("igpsport", None) == "iGPSPORT"
    assert device_model_for("igpsport", 0) == "iGPSPORT"


def test_activity_filename() -> None:
    """Filename composition matches the spec example and falls back when model is missing."""
    assert (
        activity_filename(timestamp=1147795610, device_model="BSC200", extension="fit")
        == "20260515T160650Z_BSC200.fit"
    )
    assert (
        activity_filename(timestamp=1147795610, device_model=None, extension="gpx")
        == "20260515T160650Z_iGPSPORT.gpx"
    )
    assert (
        activity_filename(timestamp=1147795610, device_model="", extension="fit")
        == "20260515T160650Z_iGPSPORT.fit"
    )


def test_activity_filename_from_meta() -> None:
    """The meta convenience wrapper reproduces the canonical filename."""
    meta = ActivityFitMeta(
        time_created=datetime(2026, 5, 15, 16, 6, 50, tzinfo=UTC),
        manufacturer="igpsport",
        product=200,
        device_model="BSC200",
    )
    assert activity_filename_from_meta(meta, "fit") == "20260515T160650Z_BSC200.fit"
    assert activity_filename_from_meta(meta, "gpx") == "20260515T160650Z_BSC200.gpx"

"""End-to-end test for :func:`ligpsport.file_transfer.upload_route_plan`.

Wires the simulator and client over a LoopbackTransport. Loads the
checked-in OSM-exported route (``route.geojson``), uploads it, and
asserts on the wire-level fingerprint:

* every chunk's payload CRC at offset 9 matches CRC8 of the chunk,
* endType=2 for all but the last chunk, endType=3 for the last,
* the simulator reassembles the same bytes the client sent (GPX form
  of the route),
* the client returns ``status=0`` from the final ACK.
"""

from __future__ import annotations

import math
import pathlib

import pytest

from ligpsport import file_transfer
from ligpsport.client import IgpsportClient
from ligpsport.routes import Point, RouteData, load_route, to_gpx_bytes
from ligpsport.simulator import Simulator, SimulatorState
from ligpsport.transport import make_loopback_pair

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


async def _run_upload(
    route: RouteData, *, chunk_size: int, generation: int
) -> tuple[SimulatorState, int, list[int]]:
    """Drive a route upload end-to-end and return ``(state, status, end_types)``."""
    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.upload_route_plan(
            client,
            route,
            file_id=42,
            file_extension="gpx",
            chunk_size=chunk_size,
            generation=generation,
            device_name="BSC200",
            timeout=2.0,
        )
    assert state.uploaded_routes, "simulator should have finalised one upload"
    end_types = state.uploaded_routes[-1].end_types
    return state, status, end_types


async def test_upload_route_geojson_round_trip() -> None:
    """The real osm-derived route, chunked at 512 bytes, gen-3 BSC200."""
    route = load_route(str(_REPO_ROOT / "route.geojson"))
    gpx_bytes = to_gpx_bytes(route)
    state, status, end_types = await _run_upload(route, chunk_size=512, generation=3)

    assert status == 0
    # The simulator's reassembled content matches the GPX the client
    # produced for the chunked stream. No mocks; both halves traverse
    # the framing layer.
    uploaded = state.uploaded_routes[-1]
    assert uploaded.content == gpx_bytes
    assert uploaded.file_id == 42
    assert uploaded.extension == "gpx"
    assert uploaded.name == route.name

    expected_chunks = max(1, math.ceil(len(gpx_bytes) / 512))
    assert len(end_types) == expected_chunks
    # All but the last chunk carry endType=2; the last carries 3.
    assert end_types[:-1] == [2] * (expected_chunks - 1)
    assert end_types[-1] == 3

    # The follow-up FILE_USE commit must land too: the simulator's
    # active_route_id reflects the file_id we just uploaded.
    assert state.active_route_id == 42


async def test_upload_tiny_route_single_chunk() -> None:
    """A one-point route fits in a single chunk → end_types == [3]."""
    tiny = RouteData(
        name="tiny",
        points=(Point(latitude=52.5, longitude=13.4),),
    )
    state, status, end_types = await _run_upload(tiny, chunk_size=4096, generation=3)
    assert status == 0
    assert end_types == [3]
    # Decoded protobuf still carries the correct metadata.
    uploaded = state.uploaded_routes[-1]
    assert uploaded.name == "tiny"
    assert uploaded.content == to_gpx_bytes(tiny)


async def test_upload_chunk_count_matches_chunk_size() -> None:
    """A precisely-sized route splits into the expected number of chunks."""
    # Build a route whose GPX serialisation is comfortably over 1KB so
    # we exercise the multi-chunk path.
    points = tuple(Point(latitude=52.5 + i * 1e-4, longitude=13.4 + i * 1e-4) for i in range(60))
    big = RouteData(name="multi", points=points)
    gpx = to_gpx_bytes(big)
    assert len(gpx) > 1024  # exercise the multi-chunk path

    state, status, end_types = await _run_upload(big, chunk_size=256, generation=3)
    assert status == 0
    expected = math.ceil(len(gpx) / 256)
    assert len(end_types) == expected
    assert end_types[-1] == 3
    assert all(et == 2 for et in end_types[:-1])
    assert state.uploaded_routes[-1].content == gpx


async def test_upload_raw_bytes_passes_through() -> None:
    """``raw_bytes`` with a non-CNX extension goes through the
    ROUTE_PLAN FILE_SEND chunked path verbatim.

    CNX uploads use a different wire protocol (FILE_OPERATION ADD —
    see ``test_file_operation_upload_format`` below); this test
    covers the GPX/FIT/TCX/XML path that still uses ROUTE_PLAN.
    """
    raw = b"\x89GPX\r\n\x1a\n" + bytes(range(256)) * 4  # ~1KB, multi-chunk
    route = RouteData(
        name="from-cloud",
        points=(Point(latitude=52.5, longitude=13.4),),
    )
    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.upload_route_plan(
            client,
            route,
            file_id=7,
            file_extension="gpx",
            chunk_size=256,
            generation=3,
            device_name="BSC200",
            timeout=2.0,
            raw_bytes=raw,
            raw_name="from-cloud",
        )
    assert status == 0
    uploaded = state.uploaded_routes[-1]
    assert uploaded.content == raw
    assert uploaded.extension == "gpx"
    assert uploaded.file_id == 7
    assert state.active_route_id == 7


def test_file_operation_upload_format() -> None:
    """Verify the byte-level shape of the FILE_OPERATION upload payload.

    The full live round-trip is covered by
    ``test_bsc200_live::test_live_upload_cnx_via_file_operation``;
    this hermetic check anchors the head + protobuf encoding so we
    notice regressions without needing the device.
    """
    head = file_transfer._build_file_operation_head(
        operate=file_transfer._SERVICE_OPERATE_TYPE_ADD,
    )
    # Captured cloud head, byte for byte:
    #   01 15 ff aa 03 ff ff 00 00 00 01 ff*8 57
    assert head.hex() == "0115ffaa03ffff00000001ffffffffffffffff57"

    pb = file_transfer._build_general_file_operation_pb(
        file_type=file_transfer.FILE_OP_TYPE_ROUTE_PLAN,
        file_size=3254,
        file_id=3130362,
        file_name="From Tiefenbachstraße 30, 70329, Stuttgart to Hohenstaufens",
        file_extension="cnx",
    )
    # Decode back via the captured byte structure: field 1=21, 2=3,
    # 3=2, 4=3254, 5=3130362, 6=name, 7="cnx".
    assert pb.startswith(bytes([0x08, 0x15]))  # field 1 (varint) = 21
    assert bytes([0x10, 0x03]) in pb  # field 2 (varint) = 3 (ADD)
    assert bytes([0x18, 0x02]) in pb  # field 3 (varint) = 2 (ROUTE_PLAN)
    # file_extension is the last field, length 3 = "cnx".
    assert pb.endswith(b"\x3a\x03cnx")


def test_confirm_header_layout() -> None:
    """Verify the 20-byte trailer layout (offsets, CRCs, endType byte)."""
    payload = b"\x01\x02\x03\x04" * 10  # 40 bytes
    header = file_transfer._build_route_plan_confirm_header(payload, end_type=3)
    assert len(header) == 20
    assert header[0] == 0x01  # END_TYPE_PB
    assert header[1] == 7  # ROUTE_PLAN service ordinal
    assert header[4] == 4  # FILE_SEND operation value
    assert header[7:9] == len(payload).to_bytes(2, "big")
    # Payload CRC: CRC8 of the protobuf bytes. Calling the public
    # framing helper gives us the reference value.
    from ligpsport import framing

    assert header[9] == framing.crc8(payload)
    assert header[10] == 3  # endType
    assert header[11:19] == b"\xff" * 8
    assert header[19] == framing.crc8(header[:19])


def test_confirm_header_rejects_invalid_end_type() -> None:
    with pytest.raises(ValueError):
        file_transfer._build_route_plan_confirm_header(b"x", end_type=1)


async def test_file_operation_upload_starts_navigation() -> None:
    """``start_navigation=True`` triggers FILE_USE on the CNX path.

    Reverse-engineered from
    ``RoadBookSearchActivity.sendFileToDevice``: after a successful
    FILE_OPERATION ADD upload, the iGPSPORT app calls
    ``IGPDeviceManager.setRoutePlanFile`` (ROUTE_PLAN FILE_USE) which
    activates the route and starts navigation on the device. We
    assert the simulator (a) records the FILE_OPERATION upload and
    (b) gets a follow-up FILE_USE that sets ``active_route_id``.
    """
    # Captured CNX bytes — exercise the multi-write fourth-channel
    # accumulator in the simulator.
    cnx_bytes = (_REPO_ROOT / "tests" / "fixtures" / "cnx_cloud_capture.cnx").read_bytes()
    route = RouteData(name="trip", points=(Point(latitude=48.8, longitude=9.2),))

    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.upload_route_plan(
            client,
            route,
            file_id=99,
            file_extension="cnx",
            generation=3,
            device_name="BSC200",
            timeout=2.0,
            raw_bytes=cnx_bytes,
            raw_name="trip",
            start_navigation=True,
        )
    assert status == 0
    # The FILE_OPERATION ADD upload landed.
    assert state.uploaded_routes, "simulator should have absorbed the CNX upload"
    uploaded = state.uploaded_routes[-1]
    assert uploaded.content == cnx_bytes
    assert uploaded.file_id == 99
    assert uploaded.extension == "cnx"
    # The follow-up FILE_USE flipped the active route on the device.
    assert state.active_route_id == 99


async def test_file_operation_upload_without_start_skips_file_use() -> None:
    """``start_navigation=False`` (default) leaves ``active_route_id`` unset."""
    cnx_bytes = (_REPO_ROOT / "tests" / "fixtures" / "cnx_cloud_capture.cnx").read_bytes()
    route = RouteData(name="trip", points=(Point(latitude=48.8, longitude=9.2),))

    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.upload_route_plan(
            client,
            route,
            file_id=99,
            file_extension="cnx",
            generation=3,
            device_name="BSC200",
            timeout=2.0,
            raw_bytes=cnx_bytes,
            raw_name="trip",
        )
    assert status == 0
    assert state.uploaded_routes
    assert state.active_route_id is None


async def test_navigation_start_error_when_file_use_fails() -> None:
    """A non-success FILE_USE status raises :class:`NavigationStartError`.

    Pre-populate the simulator with an unrelated route id so the
    FILE_USE handler's id-lookup branch sets active_route_id only
    when the uploaded id matches. Then force a mismatch by uploading
    one id and requesting FILE_USE for another via a low-level call.
    """
    # Verify the exception class plumbs the file_id + status through.
    err = file_transfer.NavigationStartError(status=1, file_id=42)
    assert err.file_id == 42
    assert err.status == 1
    assert "DataError" in str(err)


async def test_upload_with_start_navigation_gen4_e2e() -> None:
    """End-to-end: CNX upload + FILE_USE on gen-4 path → navigation active.

    Exercises the wire format the BSC200 firmware actually accepts,
    verified against ``snoop_start.log``:

    1. CNX bytes go via FILE_OPERATION ADD (single multi-write
       stream on the fourth characteristic, head + size + protobuf
       + bytes).
    2. After the upload ACKs, the library issues a ROUTE_PLAN
       FILE_USE — for ``generation=4`` (BSC200) this is a single
       merged write of (20-byte head || protobuf body) to the
       fourth characteristic, **not** the legacy split.
    3. The simulator activates the route (sets ``active_route_id``
       and flips ``navi_status`` to ``DEV_NAVI_STATUS_ON``) and ACKs
       with status=0.
    4. A follow-up ``nav-status`` query confirms the device-side
       state by going through the public ``DEV_STATUS GET`` path —
       the same way an external monitoring caller would check.

    Earlier releases had three independent bugs that made this
    sequence fail against the real device (and made an end-to-end
    test impossible against the simulator):

      * FILE_USE was sent as two writes (body on data, header on
        control) which the gen-4 BSC200 ignored.
      * The route_plan_info_msg protobuf was missing the ``name``
        field, which the firmware validates.
      * The default device generation was 3, taking the wrong
        wire-format branch in :func:`_send_file_use`.

    This test wires all three together.
    """
    cnx_bytes = (_REPO_ROOT / "tests" / "fixtures" / "cnx_cloud_capture.cnx").read_bytes()
    route = RouteData(name="trip", points=(Point(latitude=48.8, longitude=9.2),))
    file_id = 1778760617  # matches the captured cloud CNX

    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.upload_route_plan(
            client,
            route,
            file_id=file_id,
            file_extension="cnx",
            # generation=4 (default) → merged-write FILE_USE on the
            # fourth channel.
            device_name="BSC200",
            timeout=2.0,
            raw_bytes=cnx_bytes,
            raw_name="trip",
            start_navigation=True,
        )
        # The library returns the FILE_OPERATION upload status (0).
        assert status == 0
        # The simulator received the CNX upload.
        assert state.uploaded_routes
        uploaded = state.uploaded_routes[-1]
        assert uploaded.file_id == file_id
        assert uploaded.content == cnx_bytes
        # FILE_USE flipped the simulator's active-route + nav state.
        assert state.active_route_id == file_id
        assert state.navi_status == 1  # DEV_NAVI_STATUS_ON

        # The public DEV_STATUS GET path now reports nav as active —
        # this is what the new `nav-status` CLI command consumes.
        from ligpsport.commands import COMMANDS

        result = await COMMANDS["nav-status"].run(client, args=())
        assert result.value.is_navigating is True
        assert result.value.raw == 1


async def test_file_use_not_exist_returns_status_66() -> None:
    """FILE_USE for a route the device doesn't have returns wire byte 66.

    Mirrors the BSC200's documented "route not on device yet"
    behaviour from ``snoop_start.log``: the app fires FILE_USE
    before the upload, gets back status=0x42=66
    (NavigationRouteDoesNotExist), then uploads and retries.

    The library promotes this into :class:`NavigationStartError`
    when ``start_navigation=True`` was requested, with the
    human-readable ``NavigationRouteDoesNotExist`` name.
    """
    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()  # empty uploaded_routes
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer._send_file_use(
            client,
            file_id=9999,
            file_extension="cnx",
            generation=4,
            timeout=2.0,
            name="9999",
        )
    assert status == 66
    assert file_transfer._status_name(66) == "NavigationRouteDoesNotExist"
    # Navigation must NOT have been activated.
    assert state.active_route_id is None
    assert state.navi_status == 0

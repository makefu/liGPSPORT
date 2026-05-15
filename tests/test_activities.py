"""End-to-end tests for activity list / download / delete.

Drives the in-tree :class:`ligpsport.simulator.Simulator` over a
:class:`ligpsport.transport.LoopbackTransport`, so the framing,
envelope, file_transfer and command layers all traverse the same
wire path as a live BSC200 download would. The transmit-complete
download stream — the device's bogus ``payload_size``, the embedded
``file_download`` protobuf, the 0x55 file_tag — is exercised by
:meth:`Simulator._send_activity_file` and consumed by
:func:`ligpsport.framing.transmit_complete_total_size`.
"""

from __future__ import annotations

import pathlib
import xml.etree.ElementTree as ET

import pytest

from ligpsport import file_transfer, fit_activity
from ligpsport.client import IgpsportClient
from ligpsport.commands import (
    ActivityFile,
    ActivityList,
    DelActivityResult,
    DownloadedActivityList,
    DownloadedFile,
    SimActivityResult,
    run_named,
)
from ligpsport.simulator import (
    SimulatedRideFile,
    Simulator,
    SimulatorState,
)
from ligpsport.transport import make_loopback_pair

_REAL_FIT_PATH = pathlib.Path(__file__).parent / "fixtures" / "activity_bsc200.fit"
_REAL_FIT_BYTES = _REAL_FIT_PATH.read_bytes()
# Derived once so tests stay self-contained even if the fixture changes:
# the real BSC200 capture parses to time_created = 2026-05-15 14:06:50 UTC
# and device_model = BSC200, giving "20260515T140650Z_BSC200.<ext>".
_REAL_META, _REAL_RECORDS = fit_activity.read_activity_fit(_REAL_FIT_BYTES)
_REAL_FIT_NAME = fit_activity.activity_filename_from_meta(_REAL_META, "fit")
_REAL_GPX_NAME = fit_activity.activity_filename_from_meta(_REAL_META, "gpx")
_REAL_TIMESTAMP = int((_REAL_META.time_created - fit_activity.GARMIN_EPOCH_UTC).total_seconds())


def _make_fit_bytes(size: int) -> bytes:
    """Return *size* bytes that pass the FIT magic check.

    A real device-side FIT file is structured; the simulator only
    needs the magic at bytes 8..11 so the
    :class:`ligpsport.commands.DownloadedFile`'s ``fit_magic`` flag
    flips to True in tests.
    """
    if size < 12:
        return b"\x0e\x10\x54\x08" + b"\x00" * 4 + b".FIT" + b"\x00" * (size - 12)
    body = b"\x0e\x10\x54\x08" + (size - 16).to_bytes(4, "little") + b".FIT"
    return body + b"\xab" * (size - len(body))


@pytest.fixture
def state_with_one_activity() -> SimulatorState:
    """A simulator state holding one recorded activity."""
    return SimulatorState(
        ride_files=[
            SimulatedRideFile(
                timestamp=1147795610,
                file_size=512,
                user_id="user-42",
                device_id="BSC200-test",
                content=_make_fit_bytes(512),
            )
        ]
    )


@pytest.fixture
def state_with_real_activity() -> SimulatorState:
    """One activity whose payload is the captured BSC200 FIT fixture.

    Tests that exercise the GPX conversion or filename derivation need
    the real FIT records — synthetic bytes only carry the magic.
    """
    return SimulatorState(
        ride_files=[
            SimulatedRideFile(
                timestamp=_REAL_TIMESTAMP,
                file_size=len(_REAL_FIT_BYTES),
                user_id="user-42",
                device_id="BSC200-test",
                content=_REAL_FIT_BYTES,
            )
        ]
    )


@pytest.fixture
def state_with_three_real_activities() -> SimulatorState:
    """Three activities, all carrying the real FIT payload at different timestamps."""
    return SimulatorState(
        ride_files=[
            SimulatedRideFile(
                timestamp=_REAL_TIMESTAMP - 200,
                file_size=len(_REAL_FIT_BYTES),
                user_id="user-42",
                device_id="BSC200-test",
                content=_REAL_FIT_BYTES,
            ),
            SimulatedRideFile(
                timestamp=_REAL_TIMESTAMP - 100,
                file_size=len(_REAL_FIT_BYTES),
                user_id="user-42",
                device_id="BSC200-test",
                content=_REAL_FIT_BYTES,
            ),
            SimulatedRideFile(
                timestamp=_REAL_TIMESTAMP,
                file_size=len(_REAL_FIT_BYTES),
                user_id="user-42",
                device_id="BSC200-test",
                content=_REAL_FIT_BYTES,
            ),
        ]
    )


@pytest.fixture
def state_with_three_activities() -> SimulatorState:
    """Three activities — drives the multi-entry listing path."""
    return SimulatorState(
        ride_files=[
            SimulatedRideFile(
                timestamp=1147000000,
                file_size=1024,
                content=_make_fit_bytes(1024),
            ),
            SimulatedRideFile(
                timestamp=1147500000,
                file_size=512,
                content=_make_fit_bytes(512),
            ),
            SimulatedRideFile(
                timestamp=1147795610,
                file_size=2048,
                content=_make_fit_bytes(2048),
            ),
        ]
    )


async def test_list_activities_returns_simulator_files(
    state_with_three_activities: SimulatorState,
) -> None:
    """``list-activities`` round-trips every recorded entry's timestamp + size."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_three_activities), IgpsportClient(client_t) as client:
        entries = await file_transfer.list_activities(client)

    assert len(entries) == 3
    timestamps = [e.timestamp for e in entries]
    assert 1147000000 in timestamps
    assert 1147795610 in timestamps
    sizes = {e.timestamp: e.file_size for e in entries}
    assert sizes[1147000000] == 1024
    assert sizes[1147500000] == 512
    assert sizes[1147795610] == 2048


async def test_list_activities_empty_when_no_recordings() -> None:
    """No recordings → empty tuple, not a timeout."""
    client_t, peer_t = make_loopback_pair()
    state = SimulatorState()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        entries = await file_transfer.list_activities(client)
    assert entries == ()


async def test_download_activity_returns_fit_bytes(
    state_with_one_activity: SimulatorState,
) -> None:
    """``download_activity`` reassembles the simulator's transmit-complete stream.

    Hits every code path the live device exercises:

    * 20-byte head with ``file_tag = 0x55`` (transmit-complete magic).
    * Bogus ``payload_size`` in the head (1959).
    * 4-byte BE ``pb_size`` + ``file_download`` protobuf carrying
      the authoritative ``file_size``.
    * ``file_size`` raw FIT bytes.
    """
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_one_activity), IgpsportClient(client_t) as client:
        result = await file_transfer.download_activity(client, timestamp=1147795610)

    assert result.file_size == 512
    assert len(result.content) == 512
    assert result.content[8:12] == b".FIT"


async def test_download_activity_with_three_in_list(
    state_with_three_activities: SimulatorState,
) -> None:
    """Downloading one of three entries returns just that file's bytes."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_three_activities), IgpsportClient(client_t) as client:
        result = await file_transfer.download_activity(client, timestamp=1147500000)

    assert result.file_size == 512
    assert len(result.content) == 512
    assert result.content[8:12] == b".FIT"


async def test_download_cycling_data_legacy_alias(
    state_with_one_activity: SimulatorState,
) -> None:
    """The old ``download_cycling_data`` name still returns the file bytes."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_one_activity), IgpsportClient(client_t) as client:
        data = await file_transfer.download_cycling_data(
            client, timestamp=1147795610, expected_size=512
        )
    assert len(data) == 512
    assert data[8:12] == b".FIT"


async def test_delete_activity_drops_from_list(
    state_with_three_activities: SimulatorState,
) -> None:
    """``delete_activity`` removes the entry; LIST_GET no longer reports it."""
    state_with_three_activities.allow_destructive = True
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_three_activities), IgpsportClient(client_t) as client:
        status = await file_transfer.delete_activity(client, 1147500000)
        post = await file_transfer.list_activities(client)

    assert status == 0
    remaining = [e.timestamp for e in post]
    assert 1147500000 not in remaining
    assert 1147000000 in remaining
    assert 1147795610 in remaining


async def test_delete_activity_destructive_gate_refused() -> None:
    """Simulator refuses FILE_DEL when ``allow_destructive=False``.

    The guardrail mirrors the runtime gate in
    :func:`ligpsport.commands.run_named`. A test that exercises the
    wire path without the opt-in flag should observe the device
    return status=6 (UnsupportedCommand) and *not* see the entry
    disappear from the list.
    """
    state = SimulatorState(
        ride_files=[
            SimulatedRideFile(timestamp=1147795610, file_size=10, content=b"x" * 10),
        ]
    )
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        status = await file_transfer.delete_activity(client, 1147795610)
        post = await file_transfer.list_activities(client)

    assert status == 6
    assert any(e.timestamp == 1147795610 for e in post)


async def test_command_list_activities_returns_activity_list(
    state_with_three_activities: SimulatorState,
) -> None:
    """``run_named('list-activities')`` returns an ActivityList ``CommandResult``."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_three_activities), IgpsportClient(client_t) as client:
        result = await run_named(client, "list-activities")

    assert result.name == "list-activities"
    value = result.value
    assert isinstance(value, ActivityList)
    assert len(value.files) == 3
    assert all(isinstance(f, ActivityFile) for f in value.files)


async def test_command_download_activity_writes_file(
    state_with_one_activity: SimulatorState,
    tmp_path,
) -> None:
    """``run_named('download-activity')`` writes the FIT bytes to disk."""
    out = tmp_path / "activity.fit"
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_one_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "download-activity",
            args=("1147795610", str(out)),
            timeout=10.0,
        )

    assert result.name == "download-activity"
    value = result.value
    assert isinstance(value, DownloadedFile)
    assert value.size_bytes == 512
    assert value.fit_magic is True
    assert out.read_bytes()[:12].endswith(b".FIT")


async def test_command_del_activity_destructive_gate(
    state_with_three_activities: SimulatorState,
) -> None:
    """``del-activity`` refuses without ``allow_destructive=True``."""
    state_with_three_activities.allow_destructive = True
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_three_activities), IgpsportClient(client_t) as client:
        # 1) without allow_destructive: command-level refusal.
        from ligpsport.commands import DestructiveCommandError

        with pytest.raises(DestructiveCommandError):
            await run_named(client, "del-activity", args=("1147500000",))

        # 2) with the gate flipped: the activity is gone after the call.
        result = await run_named(
            client,
            "del-activity",
            args=("1147500000",),
            allow_destructive=True,
        )

    assert isinstance(result.value, DelActivityResult)
    assert result.value.deleted is True
    assert result.value.timestamp == 1147500000
    assert result.value.device_status == 0


async def test_command_del_activity_reports_not_found(
    state_with_one_activity: SimulatorState,
) -> None:
    """``del-activity`` for a timestamp that isn't on the device reports not_found."""
    state_with_one_activity.allow_destructive = True
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_one_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "del-activity",
            args=("999999999",),
            allow_destructive=True,
        )

    assert isinstance(result.value, DelActivityResult)
    assert result.value.not_found is True
    assert result.value.deleted is False


async def test_del_activity_command_is_destructive() -> None:
    """The registry entry is marked destructive."""
    from ligpsport.commands import get_command

    spec = get_command("del-activity")
    assert spec.destructive is True
    assert spec.danger is not None
    # Same for the legacy alias.
    assert get_command("delete-ride").destructive is True


async def test_sim_activity_gated() -> None:
    """Without ``allow_destructive=True`` the registry refuses ``sim-activity``."""
    from ligpsport.commands import DestructiveCommandError

    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, SimulatorState()), IgpsportClient(client_t) as client:
        with pytest.raises(DestructiveCommandError):
            await run_named(client, "sim-activity", args=("count=1", "size=2048"))


async def test_sim_activity_creates_entries(tmp_path) -> None:
    """``sim-activity count=2 size=2048`` populates two downloadable entries."""
    state = SimulatorState(allow_destructive=True)
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "sim-activity",
            args=("count=2", "size=2048"),
            allow_destructive=True,
        )
        listing = await run_named(client, "list-activities")
        assert isinstance(listing.value, ActivityList)
        assert len(listing.value.files) == 2

        out_paths = []
        for entry in listing.value.files:
            out = tmp_path / f"{entry.timestamp}.fit"
            download = await run_named(
                client,
                "download-activity",
                args=(str(entry.timestamp), str(out)),
                timeout=10.0,
            )
            assert isinstance(download.value, DownloadedFile)
            assert download.value.size_bytes == 2048
            out_paths.append(out)

    assert isinstance(result.value, SimActivityResult)
    assert result.value.count == 2
    assert result.value.size_bytes == 2048
    assert result.value.status == 0
    assert len(state.ride_files) == 2
    for path in out_paths:
        data = path.read_bytes()
        assert data[8:12] == b".FIT"


async def test_sim_activity_destructive_marker() -> None:
    """The registry entry is destructive and the prefix list covers FACTORY/SIM_FIT_SET."""
    from ligpsport.commands import DESTRUCTIVE_PREFIXES, get_command

    spec = get_command("sim-activity")
    assert spec.destructive is True
    assert spec.danger is not None
    assert (11, 7) in DESTRUCTIVE_PREFIXES


async def test_download_activity_type_gpx(
    state_with_real_activity: SimulatorState,
    tmp_path,
) -> None:
    """``download-activity ... type=gpx`` converts FIT to GPX before writing.

    The real captured FIT carries 421 records with GPS — the rendered
    GPX must parse and contain at least one ``<trkpt>``.
    """
    out = tmp_path / "ride.gpx"
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_real_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "download-activity",
            args=(str(_REAL_TIMESTAMP), str(out), "type=gpx"),
            timeout=10.0,
        )

    assert result.name == "download-activity"
    value = result.value
    assert isinstance(value, DownloadedFile)
    assert value.file_format == "gpx"
    assert out.exists()
    tree = ET.fromstring(out.read_bytes())
    gpx_ns = "{http://www.topografix.com/GPX/1/1}"
    trkpts = tree.findall(f".//{gpx_ns}trkpt")
    assert len(trkpts) >= 1


async def test_download_activity_filename_derivation(
    state_with_real_activity: SimulatorState,
    tmp_path,
) -> None:
    """Directory out-path triggers ``activity_filename_from_meta`` for both formats."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_real_activity), IgpsportClient(client_t) as client:
        fit_result = await run_named(
            client,
            "download-activity",
            args=(str(_REAL_TIMESTAMP), str(tmp_path), "type=fit"),
            timeout=10.0,
        )
        gpx_result = await run_named(
            client,
            "download-activity",
            args=(str(_REAL_TIMESTAMP), str(tmp_path), "type=gpx"),
            timeout=10.0,
        )

    assert isinstance(fit_result.value, DownloadedFile)
    assert fit_result.value.path == str(tmp_path / _REAL_FIT_NAME)
    assert (tmp_path / _REAL_FIT_NAME).exists()
    assert fit_result.value.file_format == "fit"

    assert isinstance(gpx_result.value, DownloadedFile)
    assert gpx_result.value.path == str(tmp_path / _REAL_GPX_NAME)
    assert (tmp_path / _REAL_GPX_NAME).exists()
    assert _REAL_GPX_NAME.endswith(".gpx")


async def test_download_all_activities_writes_all(
    state_with_three_real_activities: SimulatorState,
    tmp_path,
) -> None:
    """Bulk download produces one derived-name file per listed activity."""
    client_t, peer_t = make_loopback_pair()
    async with (
        Simulator(peer_t, state_with_three_real_activities),
        IgpsportClient(client_t) as client,
    ):
        result = await run_named(
            client,
            "download-all-activities",
            args=(str(tmp_path),),
            timeout=10.0,
        )

    assert result.name == "download-all-activities"
    value = result.value
    assert isinstance(value, DownloadedActivityList)
    assert len(value.entries) == 3
    assert value.skipped == ()
    for entry in value.entries:
        assert entry.file_format == "fit"
        path = pathlib.Path(entry.path)
        assert path.exists()
        assert path.parent == tmp_path
        # Every written file is a real FIT — bytes 8..11 = ".FIT".
        assert path.read_bytes()[8:12] == b".FIT"


async def test_download_all_activities_gpx_type(
    state_with_real_activity: SimulatorState,
    tmp_path,
) -> None:
    """``type=gpx`` on the bulk command emits GPX files."""
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_real_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "download-all-activities",
            args=(str(tmp_path), "type=gpx"),
            timeout=10.0,
        )

    assert isinstance(result.value, DownloadedActivityList)
    assert len(result.value.entries) == 1
    entry = result.value.entries[0]
    assert entry.file_format == "gpx"
    assert entry.path.endswith(".gpx")
    # Round-trip: the written GPX has at least one trkpt.
    tree = ET.fromstring(pathlib.Path(entry.path).read_bytes())
    gpx_ns = "{http://www.topografix.com/GPX/1/1}"
    assert tree.findall(f".//{gpx_ns}trkpt")


async def test_download_all_activities_skips_existing(
    state_with_real_activity: SimulatorState,
    tmp_path,
) -> None:
    """Pre-existing target file ends up in *skipped* and is not overwritten."""
    target = tmp_path / _REAL_FIT_NAME
    sentinel = b"PRE-EXISTING\n"
    target.write_bytes(sentinel)

    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_real_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "download-all-activities",
            args=(str(tmp_path),),
            timeout=10.0,
        )

    assert isinstance(result.value, DownloadedActivityList)
    assert result.value.entries == ()
    assert result.value.skipped == (str(target),)
    # Sentinel content untouched — the existing file was not overwritten.
    assert target.read_bytes() == sentinel


async def test_download_activity_legacy_default_is_fit(
    state_with_one_activity: SimulatorState,
    tmp_path,
) -> None:
    """No ``type`` token → raw FIT bytes written verbatim, file_format='fit'.

    Back-compat guarantee for scripts that already use the
    ``download-activity <ts> <path>`` two-positional form.
    """
    out = tmp_path / "ride.fit"
    client_t, peer_t = make_loopback_pair()
    async with Simulator(peer_t, state_with_one_activity), IgpsportClient(client_t) as client:
        result = await run_named(
            client,
            "download-activity",
            args=("1147795610", str(out)),
            timeout=10.0,
        )

    value = result.value
    assert isinstance(value, DownloadedFile)
    assert value.file_format == "fit"
    assert value.fit_magic is True
    assert out.read_bytes()[8:12] == b".FIT"

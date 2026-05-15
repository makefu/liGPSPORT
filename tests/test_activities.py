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

import pytest

from ligpsport import file_transfer
from ligpsport.client import IgpsportClient
from ligpsport.commands import (
    ActivityFile,
    ActivityList,
    DelActivityResult,
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

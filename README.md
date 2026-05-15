# **libre iGPSPORT** (ligpsport)

Python BLE library and CLI for **iGPSPORT** cycling computers,
verified end-to-end against an **iGPSPORT BSC200**. Other models in
the BSC100 / iGS family advertise the same Nordic-UART-style services
and share the protobuf protocol, so they should work too — only the
BSC200 has been exercised against a live device here.

The protocol is reverse-engineered from the iGPSPORT Android APK
(see [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for the byte-level
spec).

## Status

| Capability                                    | Implemented |
|-----------------------------------------------|-------------|
| BLE scan + name-prefix filter (`discover`)    | yes         |
| 20-byte header / CRC-8/MAXIM framing codec    | yes         |
| 23 service-type indices wired to protobuf     | yes         |
| In-process LoopbackTransport + simulator      | yes         |
| Live-device transport over `bleak`            | yes         |
| Credential storage (XDG, atomic, 0600)        | yes         |
| Named-command registry + destructive gate     | yes         |
| Read commands (`version`, `status`, `user`, `firmware`, `rides`, `sensors`, `routes`, `route-books`, `wifi`) | yes |
| Write commands (`set-rtc`, `set-user`)        | yes         |
| Destructive commands (`delete-ride`, `delete-all-rides`) gated | yes |
| File download (`get-ride`, `download-activity`) | yes (live-verified) |
| Activity FIT → GPX conversion (`download-activity type=gpx`) | yes (live-verified on BSC200) |
| Bulk activity pull (`download-all-activities`) | yes (live-verified, idempotent re-runs) |
| Synthetic activity generator (`sim-activity`)  | wire path verified — BSC200 firmware acks but silently no-ops |
| Real-time status streaming (`status --watch`) | yes         |
| GPX / geoJSON route parsing + GPX emission    | yes (stdlib only) |
| BlueZ-direct backend with MTU negotiation     | yes (`--backend bluez`) |
| Route upload — wire protocol                  | yes — FILE_OPERATION ADD (smali-verified + btsnoop-captured) |
| Route upload — file format                    | local GPX → CNX conversion (stdlib only, no cloud round-trip); **live-verified on BSC200 firmware 2024-05-14** |
| Start navigation after upload (`FILE_USE`)    | yes — pass `start` to `upload-route` |
| Map / theme upload                            | not yet (wire format known; pending btsnoop capture) |
| Firmware upgrade                              | not yet     |
| Live tracking (REAL_TIME_TRACE)               | not yet     |

`nix build .#default` runs ruff + format + 50 unit tests. The
optional `nix flake check` adds a strict mypy pass.

### Terminology: rides vs. activities

The CYCLING_DATA service (PROTOCOL.md §6.4) stores each recorded
ride as a Garmin **FIT** file the iGPSPORT app calls an *Activity*
(``HistoryActivity``, ``readActivityFitFile``, ...). v1.0–v1.3 of
this library shipped CLI commands named after "rides" (``rides``,
``get-ride``, ``delete-ride``, ``delete-all-rides``); v1.4
introduced the matching ``list-activities`` / ``download-activity`` /
``del-activity`` names that align with the upstream vocabulary. Both
spellings hit the exact same wire ops on the exact same service and
are interchangeable — pick whichever reads better. The
``activities`` spelling is preferred in new docs and scripts.

## Quickstart

```sh
# Scan for the device (filters on iGPSPORT name prefixes).
nix run . -- discover

# One-time persistence of the MAC + friendly name.
nix run . -- pair <ADDRESS> --name bike --device-name BSC200

# Read commands.
nix run . -- command --name bike version
nix run . -- command --name bike firmware
nix run . -- command --name bike status
nix run . -- command --name bike user
nix run . -- command --name bike rides
nix run . -- command --name bike sensors
nix run . -- command --name bike routes

# Stream live ride status at 1Hz for 30 seconds.
nix run . -- command --name bike status --watch 30

# Download a ride file (BSC200 must have a recorded ride first).
nix run . -- command --name bike list-activities
nix run . -- command --name bike download-activity <timestamp> /tmp/ride.fit

# Convert the FIT to GPX on the way down (one trkpt per FIT record).
nix run . -- command --name bike download-activity <timestamp> /tmp/ride.gpx type=gpx

# Or write to a directory and let the library pick the filename
# (<YYYYMMDDTHHMMSSZ>_<model>.<ext>, UTC from file_id.time_created).
nix run . -- command --name bike download-activity <timestamp> /tmp/

# Bulk pull every activity on the device into a directory.
# Skips files that already exist on a re-run.
nix run . -- command --name bike download-all-activities /tmp/bsc200/ type=gpx

# Write commands.
nix run . -- command --name bike set-rtc                     # sets clock to now
nix run . -- command --name bike set-user weight_kg=72 age=30 height_cm=178

# Destructive commands require explicit opt-in.
nix run . -- command --name bike delete-ride <timestamp> \
    --allow-destructive-commands

# Generate fake activity files (FACTORY/SIM_FIT_SET). Useful on
# simulators / iGS models that honour the op; the BSC200 firmware
# acks status=0 but silently no-ops.
nix run . -- command --name bike sim-activity count=1 size=4096 \
    --allow-destructive-commands
```

JSON output for scripting:

```sh
nix run . -- command --name bike --json version
nix run . -- discover --json
```

## Library API

```python
import asyncio

from ligpsport.ble import BleakTransport
from ligpsport.client import IgpsportClient
from ligpsport.commands import run_named

async def main():
    async with BleakTransport("F7:11:62:07:1F:F5") as t, IgpsportClient(t) as c:
        result = await run_named(c, "version")
        print(result.value.compile_time)
        # ride file:
        from ligpsport import file_transfer
        data = await file_transfer.download_cycling_data(c, timestamp=...)

asyncio.run(main())
```

The simulator (`ligpsport.simulator.Simulator`) implements the same
services in-process over a loopback transport pair, so library
consumers can develop and test without a real device.

## Development

```sh
# Single QA gate (lint + format + tests; excludes the live `bsc200` marker).
nix build .#default --print-build-logs

# Add the strict mypy run on top.
nix flake check

# Dev shell with python + pytest + bleak + ruff + protoc + bluez.
nix develop

# Regenerate protobuf modules after touching reference/*.proto.
nix run .#gen-proto

# Live-device tests (gated on env var).
LIGPSPORT_DEVICE_ADDRESS=AA:BB:CC:DD:EE:FF \
  nix develop --command pytest -q -m bsc200
```

See [`AGENTS.md`](AGENTS.md) for contributor conventions,
[`docs/PROTOCOL.md`](docs/PROTOCOL.md) for the wire spec, and
[`docs/CAPTURE.md`](docs/CAPTURE.md) for the btsnoop / Wireshark
recipes used to reverse-engineer it.

## Backends

The library ships two interchangeable transports:

* **`bleak`** (default) — cross-platform (Linux / macOS / Windows);
  the safe choice. On Linux it sits on top of BlueZ but doesn't
  expose the negotiated MTU, which can hurt performance for large
  uploads.
* **`bluez`** (Linux-only) — talks to BlueZ via DBus directly using
  `AcquireWrite` / `AcquireNotify`. Returns the *negotiated* ATT MTU
  (247 bytes on the BSC200 instead of the 23-byte default) and uses
  per-FD socket I/O so each `os.write` becomes exactly one ATT
  Write Command of up to MTU size.

Select via the CLI flag:

```sh
nix run . -- command --name bike --backend bluez version
```

Both backends satisfy the same `ligpsport.transport.Transport` ABC;
all commands work with either one.

## License

MIT — see [`LICENSE`](LICENSE).

The GPX→CNX conversion in `ligpsport.cnx` is derived from
[GPXtoCNXConverter](https://github.com/LudvvigB/GPXtoCNXConverter)
(Apache License 2.0). Attribution and the verbatim upstream license
are preserved in [`NOTICE`](NOTICE) and
[`LICENSES/GPXtoCNXConverter-LICENSE`](LICENSES/GPXtoCNXConverter-LICENSE).

# ligpsport

Python BLE library and CLI for **iGPSPORT** cycling computers,
primarily targeting the **BSC200** (other models in the BSC100 /
iGS family share the same protobuf-over-BLE protocol and should
work, but only the BSC200 is exercised against a live device here).

The protocol is reverse-engineered from the iGPSPORT Android APK
(see [`docs/PROTOCOL.md`](docs/PROTOCOL.md)).

## Status

This README is regenerated as functionality lands. Today the
package is being bootstrapped; see `CHANGELOG.md` for current
state and `docs/PROTOCOL.md` for the protocol findings.

## Quickstart

```sh
# Scan for the device
nix run . -- discover

# Pair once (writes credentials under $XDG_DATA_HOME/ligpsport/)
nix run . -- pair <ADDRESS> --name bike

# Read live status
nix run . -- command --name bike status

# Download a ride file
nix run . -- command --name bike rides
nix run . -- command --name bike get-ride <FILE_ID> --out ride.fit
```

## Development

```sh
# Single QA gate (lint + format + tests, no live device)
nix build .#default --print-build-logs

# Add the mypy run
nix flake check

# Dev shell with python + pytest + bleak + ruff + protoc + bluez
nix develop

# Regenerate protobuf modules after touching reference/*.proto
nix run .#gen-proto

# Live-device tests against the BSC200
LIGPSPORT_DEVICE_ADDRESS=AA:BB:CC:DD:EE:FF \
  nix develop --command pytest -q -m bsc200
```

See [`AGENTS.md`](AGENTS.md) for contributor conventions.

## License

MIT.

# Changelog

All notable changes to `ligpsport` are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- ``ligpsport.routes`` — stdlib-only GPX and geoJSON parsing, plus a
  canonical GPX serialiser. Handles tracks, routes, and waypoints
  from GPX; handles bare LineString, MultiLineString, Feature, and
  FeatureCollection from geoJSON. 13 unit tests on round-trip and
  edge cases.
- ``ligpsport.file_transfer.upload_route_plan`` — sends a
  :class:`RouteData` to the device using the bespoke
  ``FILE_OPERATION ADD`` envelope discovered in
  ``IGPDeviceManager.sendRoutePlanFileSingleChannel``: 20-byte
  header + 4-byte BE length + ``general_file_operation`` pb + raw
  file bytes. Documented in ``docs/PROTOCOL.md`` §7.
- ``upload-route`` CLI command:
  ``ligpsport command --name bike upload-route <path> [file_id]``.
  Auto-detects GPX vs geoJSON by extension and content sniff.

### Known issues
- The upload completes without a device reply against the live
  BSC200. The likely cause is BlueZ negotiating only the 23-byte
  default ATT MTU; the iGPSPORT Android app raises the MTU to ~244
  bytes before every upload via ``ConfigureMTUOperation``, which
  bleak's ``_acquire_mtu()`` does not appear to trigger on this
  link. A btsnoop capture of the app's working upload is the next
  investigation step.

## [0.1.0] — 2026-05-12

Initial reverse-engineering pass against the iGPSPORT BSC200.

### Added
- Repository skeleton: Nix flake, pyproject, lint/format/type/test gate.
- Protobuf compilation pipeline (`nix run .#gen-proto`) producing
  `ligpsport/proto/*_pb2.py` from `reference/*.proto`.
- 20-byte header + CRC8 framing codec.
- `LoopbackTransport` and in-process simulator for hermetic tests.
- Async `BleakTransport` and BLE discovery.
- BLE pairing flow with persistent credential storage.
- Read commands: device info, version, status, config, sensors,
  rides list, routes list, capabilities.
- File transfer: rides download, route/map/theme/firmware upload.
- Write commands and destructive-op gating.
- Real-time data stream (`DEV_STATUS`, `REAL_TIME_TRACE`, `INS`).
- CLI: `discover`, `pair`, `creds`, `command`.

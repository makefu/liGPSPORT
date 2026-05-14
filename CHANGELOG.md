# Changelog

All notable changes to `ligpsport` are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] — 2026-05-15

Route upload lands on the BSC200. The library now performs the full
GPX/geoJSON → CNX conversion locally and ships the result via the
FILE_OPERATION ADD path the iGPSPORT Android app uses internally — no
iGPSPORT cloud round-trip required.

### Added
- ``ligpsport.cnx`` — stdlib-only GPX/geoJSON → CNX encoder for
  iGPSPORT's proprietary route format. The ``<Tracks>`` second-
  difference delta encoding is derived from LudvvigB/GPXtoCNXConverter
  (Apache 2.0; attribution in ``NOTICE`` / ``LICENSES/``); the XML
  wrapper matches a btsnoop-captured cloud upload byte-for-byte
  (fixture: ``tests/fixtures/cnx_cloud_capture.cnx``). GPX waypoints
  carry through to the CNX ``<Points>`` list as on-device POIs.
- ``ligpsport.file_transfer.upload_general_file`` — implements the
  FILE_OPERATION ADD wire protocol (service 21, ``file_tag = 0xaa``,
  20-byte head + 4-byte BE size + ``general_file_operation``
  protobuf + raw file bytes), documented in ``docs/PROTOCOL.md``
  §7.1.2. This is the upload path the Android app uses for CNX
  route uploads.
- ``ligpsport.file_transfer.upload_route_plan`` — high-level route
  upload entry point. Accepts a :class:`routes.RouteData` plus a
  target file format; converts GPX/geoJSON to CNX automatically
  before dispatching to ``upload_general_file``. Also implements the
  legacy ROUTE_PLAN / FILE_SEND chunked path (per
  ``IGPDeviceManager.sendRoutePlanFile`` in the smali) for callers
  who want to test newer iGPSPORT firmwares — with the device's
  ``DeviceReturnStatus`` decoded into human-readable error strings
  on :class:`RouteUploadError`, ``FILE_USE`` commit, generation-
  aware data-channel selection, and an end-to-end hermetic test in
  ``tests/test_upload_route_plan.py``.
- ``upload-route`` CLI command:
  ``ligpsport command --name bike upload-route <path> [file_id]
  [format=gpx|fit|cnx]``. Defaults to converting GPX/geoJSON inputs
  to CNX locally (the BSC200's only accepted format). Accepts
  ``.cnx`` bytes verbatim for callers who already hold a
  cloud-converted file.
- ``ligpsport.routes`` — stdlib-only GPX and geoJSON parsing plus a
  canonical GPX serialiser. Handles tracks, routes, and waypoints
  from GPX; bare LineString, MultiLineString, Feature, and
  FeatureCollection from geoJSON.
- ``ligpsport.fit_course`` — minimal Garmin FIT Course encoder
  (stdlib only). Emits a protocol-2.0 FIT file with
  ``file_id.type=Course``, one lap, N records (position_lat/long in
  semicircles, distance in cm, altitude in 0.2 m units). Verified
  by round-tripping through ``fitparse``. Note: the BSC200
  rejects FIT with the same ``DataError`` it returns for GPX, so
  FIT is only useful against iGPSPORT models with looser firmware
  validation — the path stays in the tree for sanity-checking new
  devices.
- ``ligpsport.bluez.BluezTransport`` — second BLE backend that
  speaks to BlueZ via DBus (``dbus-fast``). Bypasses bleak's
  abstraction and uses ``AcquireWrite`` / ``AcquireNotify`` to
  obtain Unix file descriptors plus the *negotiated* ATT MTU. On
  BSC200 this raises the per-write payload from 23 bytes (bleak's
  BlueZ default) to 247. Select via the CLI's ``--backend bluez``
  flag, or instantiate directly. Linux-only.
- Multi-channel ``Transport`` API: ``send(frame, *, channel=...)``
  accepts a three-valued literal (``"control"`` / ``"data"`` /
  ``"fourth"``). Both BLE backends and ``LoopbackTransport`` route
  writes to the right Nordic-UART characteristic. Default
  ``"control"`` preserves the previous behaviour for every read
  command.
- ``IgpsportClient.open_subscription`` / ``close_subscription`` —
  eager subscription registration to close the race between
  subscriber setup and the peer's first frame. The previous
  ``subscribe()`` async generator is now a thin wrapper.
- ``docs/CAPTURE.md`` — Android HCI snoop log and Linux btmon
  recipes for capturing BLE traffic, plus the Wireshark filters
  used to extract the frame vectors in ``docs/PROTOCOL.md``, and
  the MAC-anonymisation procedure for the published capture.
- ``docs/btsnoop_hci.log`` — the route-upload capture used to
  reverse-engineer FILE_OPERATION ADD, filtered to the BSC200
  connection handle and MAC-anonymised.
- ``docs/PROTOCOL.md`` §12-§14 — AGPS / ephemeris pre-seeding,
  position-prior injection via FACTORY, and the locale gotcha for
  CNX coordinate emitters.

### Changed
- **Breaking**: ``Transport.send`` now requires keyword-only
  ``channel``; any third-party transport implementation must adopt
  the new signature.
- ``LoopbackTransport`` queue items are now ``(channel, bytes)``
  tuples. The new ``receive_with_channel`` method exposes the tag
  to multi-channel handlers (the simulator's route-upload paths);
  ``receive`` still returns only bytes to match the BLE transports.

### Known issues
- mypy ``--strict`` reports ~160 false-positive ``attr-defined``
  errors against the protobuf-generated modules. ``ruff`` and the
  test suite pass cleanly; mypy gating is deferred until the proto
  modules ship hand-written ``.pyi`` stubs.

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

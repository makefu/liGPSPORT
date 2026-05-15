# Changelog

All notable changes to `ligpsport` are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.0] — 2026-05-15

The v1.1.0 ``start_navigation`` flag didn't actually start
navigation on the device — three independent bugs in the wire format
made the BSC200 firmware silently drop the FILE_USE. This release
fixes them and adds a focused ``nav-status`` command so end-to-end
tests can verify the device actually switched into navigation mode.

### Fixed
- **FILE_USE wire format**: send a single merged write of
  (20-byte head ‖ protobuf body) to the ``fourth`` characteristic,
  matching the gen-4 path in ``setRoutePlanFile`` smali +
  ``send$lambda-135``. The previous two-write split (body on
  ``fourth``, header on ``control``) was the gen-3 path and the
  BSC200 firmware silently ignored it. Verified byte-for-byte
  against frames 35405 / 35545 of a captured "Start navigation"
  tap in the iGPSPORT Android app.
- **FILE_USE protobuf**: include the required ``name`` and
  ``total_distance`` fields in the nested ``route_plan_info_msg``.
  The BSC200 firmware validates ``name`` (the live capture shows
  ``str(file_id)`` for unnamed routes) and drops requests that
  omit it. ``upload_route_plan`` plumbs the truncated upload
  filename and ``route.distance_m`` through to the FILE_USE.
- **Default device generation** for ``upload_route_plan`` /
  ``upload_general_file`` raised from 3 to 4 — the BSC200 reports
  ``getGeneration() == 4`` and takes the merged-write path. The
  earlier default of 3 routed FILE_USE through the legacy
  two-channel split.
- **DeviceReturnStatus wire-value mapping**: the WiFi block lives at
  16-23 and the Navigation block at 65-66 (not 7-16 as earlier
  releases mapped them). Sourced from
  ``DeviceReturnStatus.smali``'s constructor calls. Affects every
  ``RouteUploadError`` / ``NavigationStartError`` message — most
  visibly, a FILE_USE for a not-yet-uploaded route returns
  wire byte 0x42 (66), which now decodes to
  ``NavigationRouteDoesNotExist`` rather than the wrong
  ``unknown(66)``.

### Added
- ``nav-status`` CLI command + :class:`commands.NavStatus`
  dataclass: read just the ``navi_status`` byte from
  ``DEV_STATUS``. Returns ``is_navigating=True`` when the device
  is on the navigation screen (after a successful
  ``upload-route ... start`` or any other FILE_USE). Targeted at
  automation and e2e tests that don't need the full status block.
- Simulator: ``_looks_like_route_plan_file_use_merged`` +
  ``_handle_route_use`` updates that recognise the new
  single-write FILE_USE pattern, flip
  ``SimulatorState.navi_status`` to ``DEV_NAVI_STATUS_ON`` on a
  successful activation, and ACK with status=66
  (``NavigationRouteDoesNotExist``) when the requested file_id
  hasn't been uploaded yet. Faithfully mirrors the firmware
  behaviour observed in ``snoop_start.log``.
- Simulator: ``_handle_dev_status`` accepts both the framing-level
  ``OP_GET = 2`` and the proto-level
  ``enum_DEV_STATUS_OPERATE_TYPE_GET = 1`` (and falls back to
  ``msg.op_type``) so the existing ``status`` runner finally works
  against the simulator. Tests for the new ``nav-status`` command
  depend on this.
- Tests: ``test_upload_with_start_navigation_gen4_e2e`` exercises
  the full upload → FILE_USE → ``DEV_STATUS GET`` round-trip
  through the simulator and asserts ``state.navi_status == 1``
  plus ``nav-status`` reporting ``is_navigating=True``;
  ``test_file_use_not_exist_returns_status_66`` covers the
  pre-upload speculative FILE_USE path.
- ``docs/PROTOCOL.md`` §7.2 rewritten with the gen-4 wire-format
  table, the full ``route_plan_info_msg`` field list, the
  corrected status-byte semantics, and a new §7.3 documenting the
  read-side ``DEV_STATUS.navi_status`` path.

### Notes
- There is still no BLE-level "stop navigation" operation; the
  ``DEV_NAVI_STATUS`` enum is read-only and the proto has no
  ``FILE_UNUSE``. For unattended e2e against the real device,
  expect to either rely on a long enough navigation timeout or
  end navigation manually on the bike computer. Simulator tests
  can reset ``state.navi_status`` directly.

## [1.1.0] — 2026-05-15

Upload-and-go: the library can now end the route upload by also
flipping the device into navigation mode, mirroring what the
iGPSPORT Android app does when the user picks "send and use" on a
route. Reverse-engineered from
``IGPDeviceManager.setRoutePlanFile`` and
``RoadBookSearchActivity.useRoutePlan`` / ``sendFileToDevice``.

### Added
- ``upload_route_plan(..., start_navigation=True)`` and
  ``upload_general_file(..., start_navigation=True, generation=...)``
  — after a successful upload, issue a ``ROUTE_PLAN FILE_USE``
  (operate_type=5) carrying the new ``file_id`` and the file
  extension. The device activates the route and switches its UI
  into navigation mode; the iGPSPORT app waits ~5 s here before
  dismissing its progress dialog. Default ``False`` — opt-in, same
  as the app's ``sendOnly = true`` path that skips FILE_USE.
- ``ligpsport.file_transfer.NavigationStartError`` — raised when
  the FILE_USE step is requested but the device returns a non-zero
  ``DeviceReturnStatus``. The upload itself is still considered
  successful (the file landed); the route just isn't active. The
  exception surfaces ``status``, ``status_name`` (e.g.
  ``"NavigationRouteDoesNotExist"``) and ``file_id``.
- ``ligpsport.file_transfer._send_file_use`` — internal helper
  factored out of the existing chunked-path FILE_USE block. The
  same routine now drives the FILE_OPERATION (CNX) path. Carries
  the gen-aware channel choice (``"fourth"`` for gen ≥ 3,
  ``"data"`` otherwise) and the two-channel split (body on the
  data-bearing UART, 20-byte header on control) the smali emits.
- ``upload-route ... start`` CLI flag: appending the bare token
  ``start`` (or ``start=true`` / ``--start``) to an ``upload-route``
  invocation triggers the FILE_USE step. Without it the file
  uploads but the user must pick the route on-device.

  ```sh
  ligpsport command --name bike upload-route trip.gpx 1 start
  ligpsport command --name bike upload-route trip.cnx 7 start
  ```
- ``docs/PROTOCOL.md`` §7.2 — wire format for ``ROUTE_PLAN
  FILE_USE``, the channel split per device generation, and notes
  on the absence of a "stop navigation" inverse op.
- Simulator: ``Simulator._absorb_general_upload_chunk`` reassembles
  multi-write FILE_OPERATION ADD streams on the ``fourth`` channel
  by reading the head + 4-byte pb-size prefix + protobuf
  ``file_size`` field, then records the upload in
  ``state.uploaded_routes`` and acks on the FILE_OPERATION service.
  This makes the new ``test_file_operation_upload_starts_navigation``
  hermetic end-to-end test possible.

### Changed
- ``upload_route_plan``'s chunked path now respects
  ``start_navigation`` in addition to the existing ``send_file_use``
  parameter (both trigger FILE_USE; ``start_navigation`` further
  promotes a refusal into ``NavigationStartError``). Existing
  callers that relied on ``send_file_use=True`` keep working
  unchanged.

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

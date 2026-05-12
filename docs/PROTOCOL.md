# iGPSPORT BLE protocol

This document is the **source of truth** for the reverse-engineered
iGPSPORT BLE protocol. Every value below was observed from one of:

* the iGPSPORT Android APK (`iGPSPORT_7.45.03_APKPure.apk`), with
  the protobuf schemas extracted to `reference/*.proto` and the
  decompiled Java/Kotlin under `tmp/jadx-out/sources/`,
* live BLE captures against a real **iGPSPORT BSC200** (cited as
  *BSC200 capture* in section bodies).

Sections that say **TBD** are work-in-progress — they describe what
we expect to find when the next investigation hits, and the field
or class name we'll transcribe from.

## 1. Transport — BLE GATT

The device exposes up to four parallel **Nordic-UART-style** GATT
services. The first one is the primary control channel that carries
the framed protobuf protocol described below; the other three are
secondary channels used for parallel firmware / file streams when
the device's `DeviceInfo.sendFileMtuSize` advertises them.

| Channel  | App class           | Service UUID                                  | TX (notify, device → app)                    | RX (write, app → device)                     |
|----------|---------------------|-----------------------------------------------|----------------------------------------------|----------------------------------------------|
| Control  | `ControlUARTManager`| `6e400001-b5a3-f393-e0a9-e50e24dcca8e`        | `6e400003-b5a3-f393-e0a9-e50e24dcca8e`       | `6e400002-b5a3-f393-e0a9-e50e24dcca8e`       |
| Data     | `UARTManager`       | `6e400001-b5a3-f393-e0a9-e50e24dcca9e`        | `6e400003-b5a3-f393-e0a9-e50e24dcca9e`       | `6e400002-b5a3-f393-e0a9-e50e24dcca9e`       |
| Third    | `ThirdUARTManager`  | `6e400001-b5a3-f393-e0a9-e50e24dcca7e`        | `6e400003-b5a3-f393-e0a9-e50e24dcca7e`       | `6e400002-b5a3-f393-e0a9-e50e24dcca7e`       |
| Fourth   | `FourthUARTManager` | `6e400001-b5a3-f393-e0a9-e50e24dcca6e`        | `6e400003-b5a3-f393-e0a9-e50e24dcca6e`       | `6e400002-b5a3-f393-e0a9-e50e24dcca6e`       |

The control channel (trailing nibble `8e`) carries the **outgoing**
half of the framed protobuf protocol — every command the library
issues writes to its RX characteristic. The BSC200 quirk: it does
**not** reply on the same channel. Instead, replies come back on the
Data channel's TX characteristic (`9e`), and various unsolicited
notifications (e.g. the AGPS ephemeris request, see §2.4) arrive on
the control channel's TX. The library subscribes to TX on all four
channels and reassembles by header — the reassembly buffer is
per-frame, not per-channel.

The third and fourth channels (`7e`, `6e`) are reserved for parallel
file / firmware streams on newer iGS models; the BSC200 advertises
them but doesn't drive traffic over them.

### Advertising

The BSC200 advertises with a name beginning with one of:

* `BSC` (e.g. `BSC200_xxxxxx`)
* `iGS`
* `iGPSPORT`

The library's BLE scanner filters on this name prefix; the MAC is
incidental.

### MTU

The device negotiates an MTU during connect; the negotiated value is
used as the chunk size for both directions. The protobuf payload of
a single logical message can exceed the MTU, in which case the
framing layer below handles fragmentation. The app reports a per-file
preferred chunk in `DeviceInfo.sendFileMtuSize` (see §6).

## 2. Framing — 20-byte header + CRC8

Every logical message on a channel is a single byte-string consisting
of a **fixed 20-byte header** followed by a **protobuf payload**. The
payload bytes are the wire encoding of one of the per-service messages
defined in `reference/*.proto`.

```
+---------------------- 20 bytes ----------------------+--- N bytes ---+
|                  CommonHead20Bytes                   | protobuf body |
+------------------------------------------------------+---------------+
```

`CommonHead20Bytes` extends `BaseHead20Bytes`; both live under
`com.igpsport.blelib.pbfactory/` in the jadx output. The constructor
sets `totalSize` (header + payload), `totalBufferSize` (payload only),
`protoBufCRC` (CRC8 over the payload), and `totalCRC` (CRC8 over the
header up to but not including `totalCRC`'s own byte).

The header byte layout (offsets, widths, endianness) is transcribed
from `CommonHead20Bytes` in §2.1 below. The CRC8 lookup table and
poly are transcribed from `com.igpsport.blelib.utils.CRC8` in §2.2.

### 2.1 Header byte layout

Transcribed from
`com.igpsport.blelib.pbfactory.BaseHead20Bytes#confirmCommandByteArray`
and `BaseHead20Bytes$Companion#updateCRC` in
`classes4.dex`.

| Offset | Width | Name              | Default | Notes                                                           |
|--------|-------|-------------------|---------|-----------------------------------------------------------------|
| 0      | u8    | `first_command`   | 0x01    | `END_TYPE_PB` constant — every frame begins with 0x01.          |
| 1      | u8    | `service`         | (set)   | Index into `common.proto`'s `service_type_index` enum (0..23). |
| 2      | u8    | `sub_service`     | 0xFF    | Second-tier service byte; used by peripheral protocols.         |
| 3      | u8    | `file_tag`        | 0xFF    | Multipart file-transfer tag; set via `setSendFileTag`.          |
| 4      | u8    | `operation`       | 0xFF    | Main operate-type (per-service enum, e.g. `SET=1`, `GET=2`).    |
| 5      | u8    | `sub_operation`   | 0xFF    | Second-tier operate-type.                                       |
| 6      | u8    | reserved          | 0xFF    | Hard-coded `-1` in the Kotlin source.                            |
| 7-8    | u16   | `payload_size`    | (set)   | **Big-endian**; produced by `StringUtils.unsignedShortToByte2`. |
| 9      | u8    | `payload_crc`     | (set)   | CRC8 of payload bytes only.                                     |
| 10     | u8    | `end_marker`      | 0x01    | `END_TYPE_PB` constant; literal 1 in the Kotlin source.         |
| 11-18  | 8×u8  | reserved padding  | 0xFF    | `RESERVED_BYTE_SIZE = 8` filled by a tight `0xFF` loop.          |
| 19     | u8    | `header_crc`      | (set)   | CRC8 of bytes 0..18 (added by `Companion.updateCRC`).           |

### 2.2 CRC8 algorithm

**CRC-8/MAXIM** (also known as CRC-8/DOW, used by Dallas/Maxim 1-Wire
devices). Polynomial 0x31, init 0, **reflected input and output**, no
final XOR. Canonical check value: `crc8(b"123456789") == 0xA1`.

The 256-byte lookup table is verbatim from
`com.igpsport.blelib.utils.CRC8` (the `crc8_tab` static array) and
shipped in `ligpsport/framing.py` as `_CRC8_TABLE`. The
`com.igpsport.blelib.utils.CRC8#calcCrc8` algorithm is a plain
table-driven loop with no special init or post-processing — the
Python `framing.crc8` function matches byte for byte.

### 2.3 Fragmentation

Logical messages longer than the BLE MTU are split into MTU-sized
chunks at the GATT layer. The receiver concatenates chunks until it
has `expected_total_size(header)` bytes in hand, then validates
`header_crc` (and `payload_crc` for `TYPE_PB` frames). The library's
`BleakTransport` implements this reassembly loop and is type-aware
(`TYPE_CONFIRM` / `TYPE_REQUEST` always equal `HEADER_SIZE`; only
`TYPE_PB` reads bytes 7-8 as a size field).

### 2.4 Captured frame catalogue

Reference vectors transcribed from BSC200 captures with firmware
"May 14 2024 11:07:51".

* **AGPS ephemeris request** (device → app, unsolicited, repeats
  every ~3 s): hex
  `030305ff01ffff00ffffffffffffffffffffffb3` — type=0x03,
  service=BACK(3), sub_service=EPHEMERIS(5), operation=GET(1),
  status=0, header_crc=0xB3. The app responds by uploading ephemeris
  payload over the BACK service.

* **Device version info GET** (app → device): hex
  `0111ffff02ffff0004ad01ffffffffffffffffae0811100208111002` —
  20-byte header (service=17, operation=2/GET, payload_size=4) +
  4-byte protobuf payload (`service_type=17, operate_type=GET`).

* **Device version info SEND** (device → app, on the `9e` channel
  in response to the GET above): hex
  `0111ffff03ffff00257c01ffffffffffffffffd1` then 37 bytes of
  protobuf payload encoding `version_msg{ble_boot_ver=111,
  ble_app_ver=141, hardware_ver=100, protocol_ver=101,
  compile_time="May 14 2024 11:07:51"}`.

## 3. Service registry

Every logical message starts with a varint field `service_type` (proto
field 1 in every per-service message), drawn from the
`service_type_index` enum in `reference/common.proto`. The receiver
uses this index to pick the proto class for the rest of the payload.

| Index | Name                                                  | Proto file                          |
|-------|-------------------------------------------------------|-------------------------------------|
| 0     | `enum_SERVICE_TYPE_INDEX_NONE`                        | —                                   |
| 1     | `enum_SERVICE_TYPE_INDEX_INS`                         | `ins.proto`                         |
| 2     | `enum_SERVICE_TYPE_INDEX_MAP`                         | `map.proto`                         |
| 3     | `enum_SERVICE_TYPE_INDEX_BACK`                        | `back.proto`                        |
| 4     | `enum_SERVICE_TYPE_INDEX_FIRMWARE`                    | `firmware.proto`                    |
| 5     | `enum_SERVICE_TYPE_INDEX_WIFI`                        | `wifi.proto`                        |
| 6     | `enum_SERVICE_TYPE_INDEX_CYCLING_DATA`                | `cycling_data.proto`                |
| 7     | `enum_SERVICE_TYPE_INDEX_ROUTE_PLAN`                  | `route_plan.proto`                  |
| 8     | `enum_SERVICE_TYPE_INDEX_REAL_TIME_TRACE`             | `real_time_trace.proto`             |
| 9     | `enum_SERVICE_TYPE_INDEX_USER_CONFIG`                 | `user_config.proto`                 |
| 10    | `enum_SERVICE_TYPE_INDEX_BLE`                         | `ble.proto`                         |
| 11    | `enum_SERVICE_TYPE_INDEX_FACTORY`                     | `factory.proto`                     |
| 12    | `enum_SERVICE_TYPE_INDEX_CONFIG`                      | `config.proto`                      |
| 13    | `enum_SERVICE_TYPE_INDEX_DEV_STATUS`                  | `dev_status.proto`                  |
| 14    | `enum_SERVICE_TYPE_INDEX_SENSOR`                      | `sensor.proto`                      |
| 15    | `enum_SERVICE_TYPE_INDEX_TRAINING`                    | `training.proto`                    |
| 16    | `enum_SERVICE_TYPE_INDEX_TEAM_INFO`                   | `team_info.proto`                   |
| 17    | `enum_SERVICE_TYPE_INDEX_DEV_VER_INFO`                | `dev_ver_info.proto`                |
| 18    | `enum_SERVICE_TYPE_INDEX_LANGUAGE`                    | `language_pack.proto`               |
| 19    | `enum_SERVICE_TYPE_INDEX_LOG`                         | `log.proto`                         |
| 20    | `enum_SERVICE_TYPE_INDEX_THEME`                       | `theme.proto`                       |
| 21    | `enum_SERVICE_TYPE_INDEX_FILE_OPERATION`              | `general_file_operation.proto`      |
| 22    | `enum_SERVICE_TYPE_INDEX_MAP_NEW`                     | `map_new.proto`                     |
| 23    | `enum_SERVICE_TYPE_INDEX_ROUTE_BOOK`                  | `route_book.proto`                  |

Each service defines its own `*_OPERATE_TYPE` enum (most have
`NONE / SET / GET / ADD / DEL`, with service-specific extras like
`UPGRADE` for firmware or `SEND` for status).

## 4. Pairing

The BLE GATT bond is established via the standard BLE pairing flow
(no PIN displayed on the BSC200; "Just Works"-style). Once bonded,
the app exchanges a `BLE` service message to claim a `member_id`:

* App sends `ble_msg { ble_operate_type=BOND_REQ,
  ble_data_msg={member_id=<app-account-id>} }` (service index 10).
* Device responds with `ble_msg { ble_operate_type=BOND_INFO,
  ble_data_msg={status=1, member_id=<bound-id>} }`.

`UNBOND` reverses the binding without disturbing the BLE pairing.
`CONNECT_STATUS` is a heartbeat the app can poll.

## 5. Capabilities

After binding, the app reads `device_information.DeviceInfo` (service
index 17, `dev_ver_info` is the version-only sibling). The
`functionTypeList` field is the canonical "what does this device
support" answer; the BSC200's list is what we test against. The
library caches the capability set and feature-gates read/write paths
accordingly.

## 6. Per-service operations

This section covers the operations the library implements today. Every
service follows the same wire shape:

1. App builds the per-service protobuf request, sets the operate-type
   to the desired value (typically ``GET=2`` or ``SET=1``).
2. App writes the resulting PbFrame (20-byte header + serialised
   protobuf) to the Control RX characteristic.
3. Device replies with a PbFrame on the Data TX characteristic whose
   ``operate_type`` is set to the matching response value (typically
   ``SEND=3``).
4. The header's ``service`` and ``operation`` bytes mirror the
   protobuf ``service_type`` and ``operate_type`` (the
   ``DeviceVersionInfoServiceFactory.getMessage`` Kotlin source sets
   both to the same value).

### 6.1 DEV_VER_INFO (service 17)

* **Operation `GET=2`** — request the version block.
* **Response `SEND=3`** — `version_msg` populated with
  `ble_boot_ver`, `ble_app_ver`, `hardware_ver`, `protocol_ver`,
  `compile_time`. The BSC200 omits `main_boot_ver` / `main_app_ver`.

### 6.2 DEV_STATUS (service 13)

* **`GET=1`** → **`SEND=2`** with cycling status, GPS coords, and
  real-time data (speed, cadence, HR, power, altitude, slope,
  course).

### 6.3 USER_CONFIG (service 9)

* **`GET=2`** → response carries the user profile (sex, weight,
  age, height, wheel diameter, bike weight, time zone, member id).
* **`SET=1`** with `user_config_data_message` overwrites the profile.

### 6.4 CYCLING_DATA (service 6)

* **`LIST_GET=1`** → **`LIST_SEND=2`** with one
  `cycling_data_file_flag_message` per recorded ride
  (`timestamp`, `file_size`, `user_id`, `device_id`).
* **`FILE_GET=3`** identifying the file by timestamp → device streams
  one or more **`FILE_SEND=4`** chunks whose `file_content` field
  contains the FIT bytes. Each chunk uses an incrementing `file_tag`
  byte in the 20-byte header (see §2.1).
* **`FILE_DEL=5`** with a `cycling_data_file_flag_message` — destructive.
* **`ALL_DEL=6`** — wipes all recorded rides — destructive.

### 6.5 SENSOR (service 14)

* **`GET=1`** → **`SEND=5`** with a `sensor_data_message` per
  paired sensor (HRM / cadence / power / radar / light / ...).

### 6.6 FIRMWARE (service 4)

* **`GET_VERSION=1`** → **`SEND_VERSION=2`** with
  `firmware_data_message` (MCU/BLE/BLE-boot versions).
* **`MCU_UPDATE=3`** / **`BLE_UPDATE=5`** — destructive, gated.

### 6.7 ROUTE_PLAN (service 7)

* **`LIST_GET=1`** → **`LIST_SEND=2`** with
  `route_plan_info_message` entries (id, name, file_type, total
  distance, status).
* **`FILE_SEND=4`** uploads a route file. The chunking pattern
  mirrors CYCLING_DATA.
* **`FILE_DEL=3`** / **`FILES_DEL=6`** — destructive.

### 6.8 ROUTE_BOOK (service 23)

* **`GET=2` + `LIST_GET=0x02`** — note the two-level operate-type:
  the top-level `SERVICE_OPERATE_TYPE` plus a service-specific
  `ROUTE_BOOK_SUB_OP_TYPE`. The BSC200 firmware in scope here may
  not implement this service (the request times out).

### 6.9 FACTORY (service 11)

* **`SN_GET=1`** / **`SN_SEND=2`** — read the device serial number.
* **`MEMORY_GET=5`** / **`BATTARY_GET=6`** — query flash + battery state.
* **`RTC_SET=12`** — set the device clock (epoch seconds). Treated as
  a write but not destructive (no data loss).
* **`SN_SET=3`** and **`SIM_FIT_SET=7`** — destructive, gated.

### 6.10 BLE (service 10)

* **`BOND_REQ=2`** with a `ble_data_message` carrying the app's
  `member_id` claims a binding key on the device.
* **`BOND_INFO=1`** / **`UNBOND=4`** / **`CONNECT_STATUS=3`** —
  binding lifecycle messages.

### 6.11 WIFI (service 5)

* **`STATUS_GET=1`** / **`STATUS_SEND=2`** — connection state. The
  BSC200 doesn't expose a working WiFi service (requests time out);
  the protocol is wired in for other iGS models that include WiFi.
* **`CTRL=3`** / **`ASSIGN_SSID=6`** — destructive in the sense that
  they overwrite the device's WiFi credentials.

## 7. File transfer

File transfers are layered on the per-service envelope (cf. §6.4 for
the canonical example: CYCLING_DATA). Each chunk is a PbFrame whose
protobuf payload is the service's container message with the chunk
bytes in its `file_content` field. The 20-byte header carries an
incrementing `file_tag` (offset 3) per chunk.

**Download** (e.g. ride file):

1. App sends ``cycling_data_msg`` with ``FILE_GET=3`` and a
   ``cycling_data_file_flag_message`` identifying the file.
2. Device streams 1..N ``cycling_data_msg`` frames with
   ``FILE_SEND=4`` and the chunk in ``file_content``. The first
   chunk is the reply to the GET; subsequent chunks arrive
   unsolicited on the same service.
3. App accumulates ``file_content`` bytes until the cumulative size
   matches the ``file_size`` reported by the preceding LIST_GET.

**Upload** (e.g. route plan): the upload path is **not** a normal
``PbFrame``. Reverse-engineered from
``IGPDeviceManager.sendRoutePlanFileSingleChannel`` in the app, a
route upload blob is:

```
[20-byte header: service=FILE_OPERATION(21), op=SERVICE_OPERATE_TYPE_ADD(3), payload_size=0]
[4 bytes big-endian = length of the general_file_operation pb]
[general_file_operation pb bytes]
[raw file content bytes]
```

The ``general_file_operation`` payload carries ``file_type=ROUTE_PLAN``,
``file_id``, ``file_extension`` (the app hardcodes ``"cnx"`` but the
device's parser also accepts ``"gpx"``), ``file_name``, and
``file_size``. The header's payload-size field stays 0 — the device
dispatches on the ``(service=21, op=ADD)`` tuple and switches to a
file-receive state machine instead of using the standard reassembly
path.

The library's :mod:`ligpsport.file_transfer` exposes
:func:`upload_route_plan` that builds this blob from any
:class:`RouteData` (parsed from GPX or geoJSON). On the BSC200 the
upload protocol is sensitive to MTU and flow control: with BlueZ's
default 23-byte ATT MTU and 1300+ sequential writes, the device
appears to drop the bytes and the upload silently fails. Resolving
this likely needs an MTU negotiation to ~244 bytes (via the
``ConfigureMTUOperation`` the iGPSPORT Android app issues before
each upload) or a btsnoop capture of a working app upload to
identify the exact sequencing.

The library's :mod:`ligpsport.file_transfer` exposes
:func:`download_cycling_data` for the read direction (verified
against the in-tree simulator; the BSC200 has no recorded rides on
hand to verify against the live device).

## 8. Destructive operations

The following ``(service, operation)`` tuples alter persistent state
on the device. They are listed verbatim in
``ligpsport.commands.DESTRUCTIVE_PREFIXES`` and gated behind
``--allow-destructive-commands``:

| Service | Operation | Effect                                                |
|---------|-----------|-------------------------------------------------------|
| 6 (CYCLING_DATA) | 5 (FILE_DEL) | Permanently deletes one recorded ride file.   |
| 6 (CYCLING_DATA) | 6 (ALL_DEL)  | Permanently deletes every recorded ride.       |
| 7 (ROUTE_PLAN)   | 3 (FILE_DEL) | Deletes one route plan from the device.        |
| 7 (ROUTE_PLAN)   | 6 (FILES_DEL)| Deletes multiple route plans in one shot.      |
| 4 (FIRMWARE)     | 3 (MCU_UPDATE) | Initiates an MCU firmware flash.            |
| 4 (FIRMWARE)     | 5 (BLE_UPDATE) | Initiates a BLE firmware flash.            |
| 11 (FACTORY)     | 3 (SN_SET)   | Overwrites the device serial number.           |
| 11 (FACTORY)     | 7 (SIM_FIT_SET) | Generates a fake ride file in flash.        |

These are also refused by the simulator's
``SimulatorState.allow_destructive`` guardrail unless explicitly
opted in by test fixtures (cf. ``AGENTS.md`` §2).

## 9. Credential persistence

The pairing state is stored in
`$XDG_DATA_HOME/ligpsport/credentials.json` (default
`~/.local/share/ligpsport/credentials.json`), `chmod 0600`. The
schema is:

```json
{
  "version": 1,
  "devices": {
    "bike": {
      "address": "AA:BB:CC:DD:EE:FF",
      "name": "BSC200_abcdef",
      "member_id": "ligpsport-7f31a8c2",
      "paired_at": "2026-05-12T20:42:00Z",
      "last_firmware": "1.2.3"
    }
  }
}
```

`member_id` is a per-installation random token the app generates and
the device remembers as its binding key. We mint our own on first
pair and persist it; subsequent connects reuse it.

## 10. Code map

| Module                       | Responsibility                                  |
|------------------------------|-------------------------------------------------|
| `ligpsport.framing`          | 20-byte header + CRC8 codec                     |
| `ligpsport.envelope`         | service-id → proto class routing                |
| `ligpsport.transport`        | TransportInterface + Bleak / Loopback impls     |
| `ligpsport.client`           | high-level async API                            |
| `ligpsport.discovery`        | BLE scan with name filter                       |
| `ligpsport.credentials`      | XDG-compliant credential store                  |
| `ligpsport.commands`         | named-command registry, destructive gating      |
| `ligpsport.capabilities`     | FunctionType helpers                            |
| `ligpsport.file_transfer`    | chunked upload / download                       |
| `ligpsport.simulator`        | in-process wire peer for tests                  |
| `ligpsport.proto.*`          | generated protobuf modules                      |

## 11. Known unknowns

* The BSC200 advertises all four UART services (`6e` / `7e` / `8e` /
  `9e`) but only exchanges control protocol on `8e` (RX) ↔ `9e` (TX).
  Whether the third/fourth channels (`7e`, `6e`) become active for
  parallel firmware/file streams on this device's firmware is unknown
  — capture needed during a firmware-upgrade flow.
* The BSC200's `WIFI` (service 5), `ROUTE_BOOK` (service 23), and
  `IND` (service 1, smart notifications) all time out on this firmware
  (`May 14 2024 11:07:51`, `protocol_ver=101`). The library implements
  them anyway because the app does — they're likely conditional on the
  device's capability bits or simply absent on the BSC200 hardware.
* Whether `REAL_TIME_TRACE` (service 8) streaming starts unsolicited
  on connection or requires an explicit subscribe message. The
  app's handling pulls from the same Control TX subscription either
  way, so the library will pick it up once the trigger is observed.
* The exact `general_file_operation` upload handshake order (does the
  device's ConfirmFrame come after each chunk or only after the final
  chunk?). The library currently sends all chunks and waits for one
  ConfirmFrame — this works for short uploads but may need to slow
  down for very large files.
* MCU firmware version (`main_app_ver`, `main_boot_ver`) is missing
  from this BSC200's `DEV_VER_INFO` reply. The `firmware` service
  also returns `mcu_firmware_ver=0`. Whether the BSC200 truly has
  no MCU firmware revision or simply doesn't expose it over BLE is
  unknown.

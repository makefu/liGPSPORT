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

**TBD** — populated phase-by-phase as the corresponding read/write
paths land. Each section will document:

* the exact protobuf request/response message,
* a captured hex example (header + payload) from the BSC200,
* the dataclass the library exposes,
* whether the operation is destructive (cf. §8).

## 7. File transfer

**TBD** — `general_file_operation.proto` envelope, plus per-file-type
streams for `cycling_data` (FIT rides), `route_plan`, `route_book`,
`map_new`, `theme`, `firmware`, `language_pack`. Documented once the
chunked download/upload loop is implemented and verified against the
real device.

## 8. Destructive operations

The following service+operation combinations alter persistent state
on the device. They are listed in `ligpsport.commands.DESTRUCTIVE_PREFIXES`
and gated behind `--allow-destructive-commands`:

**TBD** — final list lands with Phase 8.

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

* Whether the secondary UART channels are ever activated by the
  BSC200 in practice. The app supports them for newer / higher-end
  iGS models; the BSC200 may or may not advertise them. Capture
  needed.
* Whether the `wifi` service is functional on the BSC200 hardware
  (the unit advertises `WIFI_MODULE` capability but the BSC200's
  hardware doesn't appear to include WiFi). The library exposes the
  service but the BSC200 capability list will gate it.
* The exact rules for `Real-time Trace` streaming start/stop —
  whether the device push starts on connection or only after an
  explicit subscribe.

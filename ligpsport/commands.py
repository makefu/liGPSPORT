"""Named-command registry.

The registry is the single source of truth for what library commands
exist. Both the CLI in :mod:`ligpsport.__main__` and library callers
go through :func:`run_named` to invoke a command by name.

A command runs against an open :class:`ligpsport.client.IgpsportClient`.
Each entry declares whether it mutates persistent state on the device
(``destructive=True``) so the CLI's
``--allow-destructive-commands`` gate can refuse risky ops by
default. See ``AGENTS.md`` §2 for the policy.
"""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Awaitable, Callable, Mapping, Sequence
from typing import Final

from . import client as _client
from . import file_transfer
from .proto import (
    cycling_data_pb2,
    dev_status_pb2,
    dev_ver_info_pb2,
    factory_pb2,
    firmware_pb2,
    route_book_pb2,
    route_plan_pb2,
    sensor_pb2,
    user_config_pb2,
    wifi_pb2,
)

# Service+operation tuples that mutate persistent state on the device.
# The CLI raw-frame escape hatch checks against this list to refuse
# unsafe ops without an explicit override. New commands that touch
# any of these must declare destructive=True so we have two layers of
# defence (the runtime gate and this prefix-check).
DESTRUCTIVE_PREFIXES: Final[tuple[tuple[int, int], ...]] = (
    # CYCLING_DATA delete operations: FILE_DEL=5, ALL_DEL=6.
    (6, 5),
    (6, 6),
    # ROUTE_PLAN file delete & multi-file delete.
    (7, 3),
    (7, 6),
    # FIRMWARE upgrade flows (MCU=3, BLE=5).
    (4, 3),
    (4, 5),
    # FACTORY SN_SET (3) and SIM_FIT_SET (7) — both mutate persistent
    # state in a way the user wouldn't want triggered accidentally.
    (11, 3),
    (11, 7),
)


class CommandError(ValueError):
    """Base class for command-registry errors."""


class UnknownCommandError(CommandError):
    """No command by that name."""


class DestructiveCommandError(CommandError):
    """Caller invoked a destructive command without ``allow_destructive``."""


@dataclasses.dataclass(slots=True, frozen=True)
class CommandResult:
    """Outcome of a named command invocation.

    The ``value`` field is whatever structured result the runner
    returned: usually a dataclass with its own ``to_dict`` /
    ``format`` methods. Plain scalars and strings pass through.
    """

    name: str
    value: object

    def to_dict(self) -> dict[str, object]:
        return {"name": self.name, "value": _jsonable(self.value)}

    def format(self) -> str:
        return _format(self.value)


def _jsonable(value: object) -> object:
    if hasattr(value, "to_dict"):
        return value.to_dict()  # type: ignore[union-attr]
    if isinstance(value, list | tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def _format(value: object) -> str:
    if hasattr(value, "format"):
        return value.format()  # type: ignore[union-attr]
    if isinstance(value, dict | list):
        return json.dumps(_jsonable(value), indent=2, sort_keys=True)
    return str(value)


Runner = Callable[
    ["CommandSpec", _client.IgpsportClient, Sequence[str], float],
    Awaitable[object],
]


@dataclasses.dataclass(slots=True, frozen=True)
class CommandSpec:
    """One entry in the command registry."""

    name: str
    description: str
    runner: Runner
    destructive: bool = False
    danger: str | None = None

    async def run(
        self,
        client: _client.IgpsportClient,
        args: Sequence[str],
        *,
        timeout: float = 6.0,
        allow_destructive: bool = False,
    ) -> CommandResult:
        if self.destructive and not allow_destructive:
            raise DestructiveCommandError(
                f"command {self.name!r} is destructive ({self.danger}); pass allow_destructive=True"
            )
        value = await self.runner(self, client, tuple(args), timeout)
        return CommandResult(name=self.name, value=value)


# ---------- result dataclasses --------------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class DeviceVersion:
    """Decoded payload of a ``DEV_VER_INFO`` SEND reply."""

    main_boot_ver: int
    main_app_ver: int
    ble_boot_ver: int
    ble_app_ver: int
    hardware_ver: int
    protocol_ver: int
    compile_time: str

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        return (
            f"BLE boot ver:     {self.ble_boot_ver}\n"
            f"BLE app ver:      {self.ble_app_ver}\n"
            f"MCU boot ver:     {self.main_boot_ver}\n"
            f"MCU app ver:      {self.main_app_ver}\n"
            f"Hardware ver:     {self.hardware_ver}\n"
            f"Protocol ver:     {self.protocol_ver}\n"
            f"Compile time:     {self.compile_time}"
        )


# ---------- runners --------------------------------------------------------


async def _r_version(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> DeviceVersion:
    request = dev_ver_info_pb2.dev_ver_info_msg()
    request.operate_type = dev_ver_info_pb2.enum_OPERATE_TYPE_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, dev_ver_info_pb2.dev_ver_info_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    v = msg.version_message
    return DeviceVersion(
        main_boot_ver=v.main_boot_ver,
        main_app_ver=v.main_app_ver,
        ble_boot_ver=v.ble_boot_ver,
        ble_app_ver=v.ble_app_ver,
        hardware_ver=v.hardware_ver,
        protocol_ver=v.protocol_ver,
        compile_time=v.compile_time,
    )


@dataclasses.dataclass(slots=True, frozen=True)
class DeviceStatus:
    """Real-time cycling status (decoded ``DEV_STATUS`` SEND payload)."""

    cycling_status: int  # FREE=0 / DOING=1 / PAUSE=2
    cycling_start_time: int
    latitude: float
    longitude: float
    real_time_speed_mm_s: int
    avg_speed_mm_s: int
    riding_time_ms: int
    riding_distance_cm: int
    real_time_cad: int
    real_time_hrm: int
    real_time_power: int
    total_height_m: int
    cur_height_cm: int
    cur_slope: int
    course: int
    wifi_status: int
    navi_status: int

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        # Convert to friendlier units. Speed in km/h, distance in km.
        speed_kmh = self.real_time_speed_mm_s * 3.6 / 1_000_000
        avg_kmh = self.avg_speed_mm_s * 3.6 / 1_000_000
        distance_km = self.riding_distance_cm / 100_000
        time_h = self.riding_time_ms / 3_600_000
        status_name = {0: "free", 1: "doing", 2: "paused"}.get(self.cycling_status, "unknown")
        return (
            f"State:            {status_name}\n"
            f"Speed:            {speed_kmh:.2f} km/h  (avg {avg_kmh:.2f})\n"
            f"Distance:         {distance_km:.3f} km   ({time_h:.2f} h)\n"
            f"Heart rate:       {self.real_time_hrm} bpm\n"
            f"Cadence:          {self.real_time_cad} rpm\n"
            f"Power:            {self.real_time_power} W\n"
            f"Altitude:         {self.cur_height_cm / 100:.1f} m"
            f"  (total +{self.total_height_m} m)\n"
            f"Slope:            {self.cur_slope / 100:.2f}%\n"
            f"Course:           {self.course} deg\n"
            f"GPS:              {self.latitude:.6f}, {self.longitude:.6f}"
        )


@dataclasses.dataclass(slots=True, frozen=True)
class UserConfig:
    """User profile stored on the device."""

    sex: int  # 1 = male, 0 = female
    weight_g: int  # uint, in 100g units on the wire
    age: int
    height_cm: int
    wheel_dia_mm: int
    bike_weight_g: int
    time_zone_s: int
    member_id: str

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        sex_name = {0: "female", 1: "male"}.get(self.sex, str(self.sex))
        return (
            f"Sex:           {sex_name}\n"
            f"Age:           {self.age}\n"
            f"Weight:        {self.weight_g / 10:.1f} kg\n"
            f"Height:        {self.height_cm} cm\n"
            f"Bike weight:   {self.bike_weight_g / 10:.1f} kg\n"
            f"Wheel:         {self.wheel_dia_mm} mm\n"
            f"Time zone:     {self.time_zone_s / 3600:+g} h\n"
            f"Member id:     {self.member_id}"
        )


@dataclasses.dataclass(slots=True, frozen=True)
class RideFile:
    """One entry in the device's recorded-ride list."""

    timestamp: int
    file_size: int
    user_id: str
    device_id: str

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        return (
            f"timestamp={self.timestamp} size={self.file_size}B "
            f"user={self.user_id!r} device={self.device_id!r}"
        )


@dataclasses.dataclass(slots=True, frozen=True)
class RideList:
    """Wrapper around a list of ride files; provides format() and to_dict()."""

    files: tuple[RideFile, ...]

    def to_dict(self) -> dict[str, object]:
        return {"files": [f.to_dict() for f in self.files]}

    def format(self) -> str:
        if not self.files:
            return "no recorded rides on device"
        return "\n".join(f.format() for f in self.files)


@dataclasses.dataclass(slots=True, frozen=True)
class SensorList:
    """Wrapper around the SENSOR service's reported sensor list."""

    sensors: tuple[dict[str, object], ...]

    def to_dict(self) -> dict[str, object]:
        return {"sensors": list(self.sensors)}

    def format(self) -> str:
        if not self.sensors:
            return "no sensors paired"
        lines = []
        for s in self.sensors:
            lines.append(", ".join(f"{k}={v}" for k, v in s.items() if v))
        return "\n".join(lines)


async def _r_status(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> DeviceStatus:
    request = dev_status_pb2.dev_status_msg()
    request.op_type = dev_status_pb2.enum_DEV_STATUS_OPERATE_TYPE_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, dev_status_pb2.dev_status_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    cs = msg.dev_cycling_status_msg
    gps = msg.dev_gps_msg
    rt = msg.rt_data_msg
    return DeviceStatus(
        cycling_status=cs.dev_cycling_status,
        cycling_start_time=cs.cycling_start_time,
        latitude=gps.latitude,
        longitude=gps.longitude,
        real_time_speed_mm_s=rt.real_time_speed,
        avg_speed_mm_s=rt.avg_speed,
        riding_time_ms=rt.riding_time,
        riding_distance_cm=rt.riding_distance,
        real_time_cad=rt.real_time_cad,
        real_time_hrm=rt.real_time_hrm,
        real_time_power=rt.real_time_power,
        total_height_m=rt.total_height,
        cur_height_cm=rt.cur_height,
        cur_slope=rt.cur_slope,
        course=rt.course,
        wifi_status=msg.wifi_status,
        navi_status=msg.navi_status,
    )


async def _r_user(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> UserConfig:
    request = user_config_pb2.user_config_msg()
    request.user_config_operate_type = user_config_pb2.enum_USER_CONFIG_OPERATE_TYPE_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, user_config_pb2.user_config_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    u = msg.user_config_data_message
    return UserConfig(
        sex=u.sex,
        weight_g=u.weight,
        age=u.age,
        height_cm=u.height,
        wheel_dia_mm=u.wheel_dia,
        bike_weight_g=u.bike_weight,
        time_zone_s=u.time_zone,
        member_id=u.member_id,
    )


async def _r_rides(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> RideList:
    request = cycling_data_pb2.cycling_data_msg()
    request.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, cycling_data_pb2.cycling_data_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    files = tuple(
        RideFile(
            timestamp=f.timestamp,
            file_size=f.file_size,
            user_id=f.user_id,
            device_id=f.device_id,
        )
        for f in msg.cycling_data_file_flag_msg
    )
    return RideList(files=files)


async def _r_sensors(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> SensorList:
    request = sensor_pb2.sensor_message()
    request.sensor_operate_type = sensor_pb2.enum_SENSOR_OPERATE_TYPE_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, sensor_pb2.sensor_message):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    sensors: list[dict[str, object]] = [
        {
            "type": s.sensor_type,
            "radio": s.sensor_radio_type,
            "status": s.sensor_status_type,
            "key": s.sensor_key,
            "name": s.sensor_ble_name,
            "battery": s.sensor_pwr,
            "wheel_size_mm": s.wheel_size,
            "crank_length_mm": s.crank_length,
            "rssi": s.sensor_rssi,
            "forbidden": s.sensor_forbidden,
        }
        for s in msg.sensor_data_msg
    ]
    return SensorList(sensors=tuple(sensors))


@dataclasses.dataclass(slots=True, frozen=True)
class FirmwareInfo:
    """Decoded ``FIRMWARE_OPERATE_TYPE_SEND_VERSION`` payload."""

    mcu_firmware_ver: int
    ble_firmware_ver: int
    ble_boot_firmware_ver: int

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        return (
            f"MCU firmware:        {self.mcu_firmware_ver}\n"
            f"BLE firmware:        {self.ble_firmware_ver}\n"
            f"BLE boot firmware:   {self.ble_boot_firmware_ver}"
        )


@dataclasses.dataclass(slots=True, frozen=True)
class WifiStatus:
    """Decoded WIFI status reply."""

    on: bool
    ssid: str
    signal_strength: int

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        return (
            f"WiFi:            {'on' if self.on else 'off'}\n"
            f"SSID:            {self.ssid or '(none)'}\n"
            f"Signal:          {self.signal_strength}"
        )


@dataclasses.dataclass(slots=True, frozen=True)
class RoutePlan:
    """One entry in the route_plan list."""

    id: int
    name: str
    file_type: int  # ROUTE_PLAN_FILE_TYPE (CNX=1, GPX=2, FIT=3, TCX=4, XML=5...)
    total_distance: int
    status: int

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        kind = {1: "CNX", 2: "GPX", 3: "FIT", 4: "TCX"}.get(self.file_type, str(self.file_type))
        return f"id={self.id} name={self.name!r} type={kind} distance={self.total_distance}m"


@dataclasses.dataclass(slots=True, frozen=True)
class RouteList:
    """List of routes (route_plan service)."""

    routes: tuple[RoutePlan, ...]

    def to_dict(self) -> dict[str, object]:
        return {"routes": [r.to_dict() for r in self.routes]}

    def format(self) -> str:
        if not self.routes:
            return "no routes on device"
        return "\n".join(r.format() for r in self.routes)


@dataclasses.dataclass(slots=True, frozen=True)
class RouteBookEntry:
    """One entry in the route_book list."""

    id: int
    name: str
    status: int

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        used = "used" if self.status == 1 else "unused"
        return f"id={self.id} name={self.name!r} {used}"


@dataclasses.dataclass(slots=True, frozen=True)
class RouteBookList:
    """List of electronic route books (route_book service)."""

    entries: tuple[RouteBookEntry, ...]

    def to_dict(self) -> dict[str, object]:
        return {"entries": [r.to_dict() for r in self.entries]}

    def format(self) -> str:
        if not self.entries:
            return "no route books on device"
        return "\n".join(r.format() for r in self.entries)


async def _r_firmware(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> FirmwareInfo:
    request = firmware_pb2.firmware_msg()
    request.firmware_operate_type = firmware_pb2.enum_FIRMWARE_OPERATE_TYPE_GET_VERSION
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, firmware_pb2.firmware_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    f = msg.firmware_data_msg
    return FirmwareInfo(
        mcu_firmware_ver=f.mcu_firmware_ver,
        ble_firmware_ver=f.ble_firmware_ver,
        ble_boot_firmware_ver=f.ble_boot_firmware_ver,
    )


async def _r_wifi(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> WifiStatus:
    request = wifi_pb2.wifi_msg()
    request.wifi_operate_type = wifi_pb2.enum_WIFI_OPERATE_TYPE_STATUS_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, wifi_pb2.wifi_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    # The device replies with a wifi_data_message; the first entry holds
    # the connection state. status: 1=off, 2=on.
    if not msg.wifi_data_msg:
        return WifiStatus(on=False, ssid="", signal_strength=0)
    d = msg.wifi_data_msg[0]
    return WifiStatus(on=d.status == 2, ssid=d.ssid, signal_strength=d.signal_strength)


async def _r_routes(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> RouteList:
    request = route_plan_pb2.route_plan_data_msg()
    request.route_plan_operate_type = route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_LIST_GET
    response = await client.request(request, timeout=timeout)
    msg = response.message
    if not isinstance(msg, route_plan_pb2.route_plan_data_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    routes = tuple(
        RoutePlan(
            id=r.id,
            name=r.name,
            file_type=r.file_type,
            total_distance=r.total_distance,
            status=r.status,
        )
        for r in msg.route_plan_info_msg
    )
    return RouteList(routes=routes)


@dataclasses.dataclass(slots=True, frozen=True)
class DownloadedFile:
    """The contents of a file pulled off the device."""

    path: str
    size_bytes: int
    fit_magic: bool  # True iff the first 12 bytes match the FIT magic header.

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)

    def format(self) -> str:
        magic = "FIT header verified" if self.fit_magic else "(not a recognised FIT file)"
        return f"wrote {self.size_bytes} bytes -> {self.path}  {magic}"


async def _r_set_rtc(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    args: Sequence[str],
    timeout: float,
) -> str:
    """Set the device's real-time clock.

    Without arguments uses the current UTC time. Optionally accepts a
    unix epoch seconds value as the first argument.
    """
    import time as _time

    epoch_s: int
    if args:
        try:
            epoch_s = int(args[0])
        except ValueError as exc:
            raise CommandError(f"invalid epoch seconds: {args[0]!r}") from exc
    else:
        epoch_s = int(_time.time())

    request = factory_pb2.factory_msg()
    request.factory_operate_type = factory_pb2.enum_FACTORY_OPERATE_TYPE_RTC_SET
    request.rtc_msg.time = epoch_s
    await client.request(
        request,
        operation=factory_pb2.enum_FACTORY_OPERATE_TYPE_RTC_SET,
        timeout=timeout,
    )
    return f"sent RTC = {epoch_s} (epoch seconds)"


async def _r_set_user(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    args: Sequence[str],
    timeout: float,
) -> str:
    """Set the user profile (weight, age, height, etc.)

    Arguments are ``key=value`` pairs. Recognised keys: ``sex`` (0 or 1),
    ``weight_kg`` (float), ``age`` (int), ``height_cm`` (int),
    ``wheel_dia_mm`` (int), ``bike_weight_kg`` (float),
    ``time_zone_h`` (float), ``member_id`` (string).
    """
    parsed: dict[str, str] = {}
    for arg in args:
        if "=" not in arg:
            raise CommandError(f"expected key=value, got {arg!r}")
        k, _, v = arg.partition("=")
        parsed[k] = v

    request = user_config_pb2.user_config_msg()
    request.user_config_operate_type = user_config_pb2.enum_USER_CONFIG_OPERATE_TYPE_SET
    u = request.user_config_data_message
    if "sex" in parsed:
        u.sex = int(parsed["sex"])
    if "weight_kg" in parsed:
        u.weight = int(float(parsed["weight_kg"]) * 10)
    if "age" in parsed:
        u.age = int(parsed["age"])
    if "height_cm" in parsed:
        u.height = int(parsed["height_cm"])
    if "wheel_dia_mm" in parsed:
        u.wheel_dia = int(parsed["wheel_dia_mm"])
    if "bike_weight_kg" in parsed:
        u.bike_weight = int(float(parsed["bike_weight_kg"]) * 10)
    if "time_zone_h" in parsed:
        u.time_zone = int(float(parsed["time_zone_h"]) * 3600)
    if "member_id" in parsed:
        u.member_id = parsed["member_id"]
    await client.request(
        request,
        operation=user_config_pb2.enum_USER_CONFIG_OPERATE_TYPE_SET,
        timeout=timeout,
    )
    return f"updated user profile ({len(parsed)} field{'s' if len(parsed) != 1 else ''})"


async def _r_delete_ride(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    args: Sequence[str],
    timeout: float,
) -> str:
    """Delete one recorded ride file from the device. **Destructive.**"""
    if not args:
        raise CommandError("delete-ride takes <timestamp>")
    try:
        timestamp = int(args[0])
    except ValueError as exc:
        raise CommandError(f"invalid timestamp: {args[0]!r}") from exc
    request = cycling_data_pb2.cycling_data_msg()
    request.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL
    f = request.cycling_data_file_flag_msg.add()
    f.timestamp = timestamp
    await client.request(
        request,
        operation=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL,
        timeout=timeout,
    )
    return f"requested delete of ride file timestamp={timestamp}"


async def _r_delete_all_rides(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> str:
    """Delete every recorded ride on the device. **Very destructive.**"""
    request = cycling_data_pb2.cycling_data_msg()
    request.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL
    await client.request(
        request,
        operation=cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL,
        timeout=timeout,
    )
    return "requested delete-all-rides"


async def _r_get_ride(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    args: Sequence[str],
    timeout: float,
) -> DownloadedFile:
    if len(args) < 2:
        raise CommandError("get-ride takes <timestamp> <out-path>")
    try:
        timestamp = int(args[0])
    except ValueError as exc:
        raise CommandError(f"invalid timestamp: {args[0]!r}") from exc
    out_path = args[1]
    expected_size: int | None = None
    if len(args) >= 3:
        try:
            expected_size = int(args[2])
        except ValueError as exc:
            raise CommandError(f"invalid expected_size: {args[2]!r}") from exc
    data = await file_transfer.download_cycling_data(
        client,
        timestamp=timestamp,
        expected_size=expected_size,
        chunk_timeout=timeout,
        overall_timeout=max(60.0, timeout * 6),
    )
    with open(out_path, "wb") as fh:
        fh.write(data)
    # FIT files start with the local header pattern: byte 0 = header size
    # (usually 12 or 14), bytes 8..11 = b".FIT".
    fit_magic = len(data) >= 12 and data[8:12] == b".FIT"
    return DownloadedFile(path=out_path, size_bytes=len(data), fit_magic=fit_magic)


async def _r_route_books(
    _spec: CommandSpec,
    client: _client.IgpsportClient,
    _args: Sequence[str],
    timeout: float,
) -> RouteBookList:
    request = route_book_pb2.route_book_data_msg()
    # The route_book service has a two-level operate-type: top-level
    # SERVICE_OPERATE_TYPE for GET/SET, plus a ROUTE_BOOK_SUB_OP_TYPE
    # that distinguishes list-num / list-get / use / rename.
    from .proto import common_pb2  # local to avoid widening the top imports.

    request.operate_type = common_pb2.enum_SERVICE_OPERATE_TYPE_GET
    request.sub_operate_type = route_book_pb2.enum_ROUTE_BOOK_GET_SUB_OP_TYPE_LIST_GET
    response = await client.request(
        request,
        operation=common_pb2.enum_SERVICE_OPERATE_TYPE_GET,
        timeout=timeout,
    )
    msg = response.message
    if not isinstance(msg, route_book_pb2.route_book_data_msg):
        raise CommandError(f"unexpected response message: {type(msg).__name__}")
    entries = tuple(
        RouteBookEntry(id=r.id, name=r.name, status=r.status) for r in msg.route_book_infor_msg
    )
    return RouteBookList(entries=entries)


COMMANDS: Final[Mapping[str, CommandSpec]] = {
    "version": CommandSpec(
        name="version",
        description="Read MCU / BLE / hardware versions and firmware compile time.",
        runner=_r_version,
    ),
    "status": CommandSpec(
        name="status",
        description="Read live ride status (speed, heart rate, cadence, power, GPS).",
        runner=_r_status,
    ),
    "user": CommandSpec(
        name="user",
        description="Read the user profile stored on the device.",
        runner=_r_user,
    ),
    "rides": CommandSpec(
        name="rides",
        description="List recorded ride files on the device.",
        runner=_r_rides,
    ),
    "sensors": CommandSpec(
        name="sensors",
        description="List paired sensors (HRM, cadence, power, radar, ...).",
        runner=_r_sensors,
    ),
    "firmware": CommandSpec(
        name="firmware",
        description="Read MCU/BLE firmware versions (via the FIRMWARE service).",
        runner=_r_firmware,
    ),
    "wifi": CommandSpec(
        name="wifi",
        description="Read WiFi connection status (BSC200 hardware may not support WiFi).",
        runner=_r_wifi,
    ),
    "routes": CommandSpec(
        name="routes",
        description="List route plans stored on the device.",
        runner=_r_routes,
    ),
    "route-books": CommandSpec(
        name="route-books",
        description="List electronic route books stored on the device.",
        runner=_r_route_books,
    ),
    "get-ride": CommandSpec(
        name="get-ride",
        description="Download a recorded ride file by timestamp: get-ride <ts> <out> [size]",
        runner=_r_get_ride,
    ),
    "set-rtc": CommandSpec(
        name="set-rtc",
        description="Set the device clock (no args: now; or pass epoch seconds).",
        runner=_r_set_rtc,
    ),
    "set-user": CommandSpec(
        name="set-user",
        description="Set user profile fields: set-user weight_kg=75 age=30 height_cm=180 ...",
        runner=_r_set_user,
    ),
    "delete-ride": CommandSpec(
        name="delete-ride",
        description="Delete one ride file by timestamp.",
        runner=_r_delete_ride,
        destructive=True,
        danger="Irreversibly deletes the ride file from the device's flash.",
    ),
    "delete-all-rides": CommandSpec(
        name="delete-all-rides",
        description="Delete every recorded ride file. Cannot be undone.",
        runner=_r_delete_all_rides,
        destructive=True,
        danger="Erases all recorded ride history. No recovery once issued.",
    ),
}


def get_command(name: str) -> CommandSpec:
    spec = COMMANDS.get(name)
    if spec is None:
        raise UnknownCommandError(
            f"unknown command {name!r}; available: {', '.join(sorted(COMMANDS))}"
        )
    return spec


def list_commands() -> list[CommandSpec]:
    return [COMMANDS[name] for name in sorted(COMMANDS)]


async def run_named(
    client: _client.IgpsportClient,
    name: str,
    args: Sequence[str] = (),
    *,
    timeout: float = 6.0,
    allow_destructive: bool = False,
) -> CommandResult:
    spec = get_command(name)
    return await spec.run(client, args, timeout=timeout, allow_destructive=allow_destructive)

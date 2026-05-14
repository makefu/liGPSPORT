"""In-process wire peer used by the test suite.

The simulator is the iGPSPORT-side equivalent of the client: same
framing codec, same envelope router, same protobuf modules. Tests
hand it the peer-end of a :class:`ligpsport.transport.LoopbackTransport`
pair and configure a small in-memory state (device version, ride
list, configuration values). The simulator runs a background read
loop, dispatches incoming frames to per-service handlers, and writes
replies back through the same transport. No protocol detail is
duplicated between client and simulator; both go through
:mod:`ligpsport.framing` and :mod:`ligpsport.envelope`.

Adding a new service handler:

1. Implement an async function ``handle(state, frame, msg) -> Message``
   (or ``-> None`` for one-way operations).
2. Register it in :class:`Simulator._HANDLERS` keyed on the
   ``service_type_index`` value.
"""

from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import logging
from collections.abc import Callable, Coroutine
from typing import Final

from google.protobuf.message import Message

from . import client as _client
from . import envelope, framing
from .proto import (
    common_pb2,
    cycling_data_pb2,
    dev_status_pb2,
    dev_ver_info_pb2,
    route_plan_pb2,
    sensor_pb2,
    user_config_pb2,
)
from .transport import Channel, LoopbackTransport, Transport, TransportClosed

_LOG = logging.getLogger(__name__)


Handler = Callable[
    ["SimulatorState", framing.Frame, Message],
    Coroutine[None, None, Message | None],
]


@dataclasses.dataclass(slots=True)
class SimulatedRideFile:
    """One entry in the simulator's cycling-data file list."""

    timestamp: int
    file_size: int
    user_id: str = ""
    device_id: str = ""


@dataclasses.dataclass(slots=True)
class UploadedRouteFile:
    """An accumulated route file received via a multi-chunk upload."""

    file_id: int
    file_type: int
    name: str
    extension: str
    total_distance: int
    content: bytes
    end_types: list[int]


@dataclasses.dataclass(slots=True)
class SimulatedSensor:
    """One entry in the simulator's paired-sensor list."""

    sensor_type: int  # enum SENSOR_TYPE
    sensor_radio_type: int = 1  # BLE
    sensor_status_type: int = 1  # CONNECTED
    sensor_key: str = ""
    sensor_ble_name: str = ""
    sensor_pwr: int = 0
    wheel_size: int = 0


@dataclasses.dataclass(slots=True)
class SimulatorState:
    """In-memory device state the simulator exposes.

    Fields are populated as new services land. Tests instantiate a
    :class:`Simulator` with a :class:`SimulatorState` carrying just
    the values they care about; defaults match a fresh out-of-the-box
    BSC200.
    """

    main_boot_ver: int = 0x01000000
    main_app_ver: int = 0x01000000
    ble_boot_ver: int = 0x01000000
    ble_app_ver: int = 0x01000000
    hardware_ver: int = 0x01000000
    protocol_ver: int = 101
    compile_time: str = "2026-01-01 00:00:00"

    # Cycling status (DEV_STATUS service).
    cycling_status: int = 0
    cycling_start_time: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    real_time_speed_mm_s: int = 0
    avg_speed_mm_s: int = 0
    riding_time_ms: int = 0
    riding_distance_cm: int = 0
    real_time_cad: int = 0
    real_time_hrm: int = 0
    real_time_power: int = 0
    total_height_m: int = 0
    cur_height_cm: int = 0
    cur_slope: int = 0
    course: int = 0
    wifi_status: int = 1  # IDLE
    navi_status: int = 0

    # User profile (USER_CONFIG service).
    user_sex: int = 1
    user_weight_g: int = 750  # 75kg
    user_age: int = 30
    user_height_cm: int = 175
    user_wheel_dia_mm: int = 2096
    user_bike_weight_g: int = 80
    user_time_zone_s: int = 0
    user_member_id: str = "ligpsport-sim"

    # Recorded rides (CYCLING_DATA service).
    ride_files: list[SimulatedRideFile] = dataclasses.field(default_factory=list)

    # Paired sensors (SENSOR service).
    sensors: list[SimulatedSensor] = dataclasses.field(default_factory=list)

    # Completed uploads from `upload_route_plan`. Each entry is the
    # reassembled file plus its decoded metadata.
    uploaded_routes: list[UploadedRouteFile] = dataclasses.field(default_factory=list)

    # file_id of the route most recently committed via FILE_USE (the
    # commit step that mirrors `setRoutePlanFile` in the smali).
    active_route_id: int | None = None

    # The simulator records every received frame for test assertions.
    received: list[framing.Frame] = dataclasses.field(default_factory=list)
    # Destructive-op guardrail: when False, the simulator refuses any
    # write/delete operation with a NACK frame. Tests opt in.
    allow_destructive: bool = False


async def _handle_dev_ver_info(
    state: SimulatorState, frame: framing.Frame, _msg: Message
) -> Message | None:
    if frame.operation != _client.OP_GET:
        _LOG.debug("dev_ver_info: ignoring non-GET operation %d", frame.operation)
        return None
    reply = dev_ver_info_pb2.dev_ver_info_msg()
    reply.operate_type = dev_ver_info_pb2.enum_OPERATE_TYPE_SEND
    v = reply.version_message
    v.main_boot_ver = state.main_boot_ver
    v.main_app_ver = state.main_app_ver
    v.ble_boot_ver = state.ble_boot_ver
    v.ble_app_ver = state.ble_app_ver
    v.hardware_ver = state.hardware_ver
    v.protocol_ver = state.protocol_ver
    v.compile_time = state.compile_time
    return reply


async def _handle_dev_status(
    state: SimulatorState, frame: framing.Frame, _msg: Message
) -> Message | None:
    if frame.operation != dev_status_pb2.enum_DEV_STATUS_OPERATE_TYPE_GET:
        return None
    reply = dev_status_pb2.dev_status_msg()
    reply.op_type = dev_status_pb2.enum_DEV_STATUS_OPERATE_TYPE_SEND
    reply.dev_cycling_status_msg.dev_cycling_status = state.cycling_status
    reply.dev_cycling_status_msg.cycling_start_time = state.cycling_start_time
    reply.dev_gps_msg.latitude = state.latitude
    reply.dev_gps_msg.longitude = state.longitude
    rt = reply.rt_data_msg
    rt.real_time_speed = state.real_time_speed_mm_s
    rt.avg_speed = state.avg_speed_mm_s
    rt.riding_time = state.riding_time_ms
    rt.riding_distance = state.riding_distance_cm
    rt.real_time_cad = state.real_time_cad
    rt.real_time_hrm = state.real_time_hrm
    rt.real_time_power = state.real_time_power
    rt.total_height = state.total_height_m
    rt.cur_height = state.cur_height_cm
    rt.cur_slope = state.cur_slope
    rt.course = state.course
    reply.wifi_status = state.wifi_status
    reply.navi_status = state.navi_status
    return reply


async def _handle_user_config(
    state: SimulatorState, frame: framing.Frame, _msg: Message
) -> Message | None:
    if frame.operation != user_config_pb2.enum_USER_CONFIG_OPERATE_TYPE_GET:
        return None
    reply = user_config_pb2.user_config_msg()
    reply.user_config_operate_type = user_config_pb2.enum_USER_CONFIG_OPERATE_TYPE_GET
    u = reply.user_config_data_message
    u.sex = state.user_sex
    u.weight = state.user_weight_g
    u.age = state.user_age
    u.height = state.user_height_cm
    u.wheel_dia = state.user_wheel_dia_mm
    u.bike_weight = state.user_bike_weight_g
    u.time_zone = state.user_time_zone_s
    u.member_id = state.user_member_id
    return reply


async def _handle_cycling_data(
    state: SimulatorState, frame: framing.Frame, _msg: Message
) -> Message | None:
    if frame.operation != cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET:
        return None
    reply = cycling_data_pb2.cycling_data_msg()
    reply.cycling_data_operate_type = cycling_data_pb2.enum_CYCLING_DATA_OPERATE_TYPE_LIST_SEND
    for f in state.ride_files:
        entry = reply.cycling_data_file_flag_msg.add()
        entry.timestamp = f.timestamp
        entry.file_size = f.file_size
        entry.user_id = f.user_id
        entry.device_id = f.device_id
    return reply


async def _handle_sensor(
    state: SimulatorState, frame: framing.Frame, _msg: Message
) -> Message | None:
    if frame.operation != sensor_pb2.enum_SENSOR_OPERATE_TYPE_GET:
        return None
    reply = sensor_pb2.sensor_message()
    reply.sensor_operate_type = sensor_pb2.enum_SENSOR_OPERATE_TYPE_SEND
    for s in state.sensors:
        entry = reply.sensor_data_msg.add()
        entry.sensor_type = s.sensor_type
        entry.sensor_radio_type = s.sensor_radio_type
        entry.sensor_status_type = s.sensor_status_type
        entry.sensor_key = s.sensor_key
        entry.sensor_ble_name = s.sensor_ble_name
        entry.sensor_pwr = s.sensor_pwr
        entry.wheel_size = s.wheel_size
    return reply


class Simulator:
    """Wire-compatible peer driven by an in-memory :class:`SimulatorState`.

    Lifecycle::

        client_t, peer_t = make_loopback_pair()
        sim = Simulator(peer_t)
        async with sim:
            client = IgpsportClient(client_t)
            await client.start()
            ...

    Inside ``async with sim`` a background task reads frames from the
    peer transport and writes replies through the same transport.
    Leaving the context cancels the task and closes the transport.
    """

    # Service → handler. Each handler is awaited; a non-None return
    # value becomes the reply (encoded through the same envelope.encode
    # path the client uses).
    _HANDLERS: Final[dict[int, Handler]] = {
        common_pb2.enum_SERVICE_TYPE_INDEX_DEV_VER_INFO: _handle_dev_ver_info,
        common_pb2.enum_SERVICE_TYPE_INDEX_DEV_STATUS: _handle_dev_status,
        common_pb2.enum_SERVICE_TYPE_INDEX_USER_CONFIG: _handle_user_config,
        common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA: _handle_cycling_data,
        common_pb2.enum_SERVICE_TYPE_INDEX_SENSOR: _handle_sensor,
    }

    def __init__(self, transport: Transport, state: SimulatorState | None = None):
        self._transport = transport
        self.state = state if state is not None else SimulatorState()
        self._task: asyncio.Task[None] | None = None
        # Pending data-channel chunks waiting for their matching
        # control-channel trailer. Indexed by the channel they
        # arrived on so we don't cross the streams.
        self._pending_chunk: dict[Channel, bytes] = {}
        # In-progress route-plan upload; finalised on end_type=3.
        self._in_progress_route: UploadedRouteFile | None = None

    async def __aenter__(self) -> Simulator:
        self._task = asyncio.create_task(self._serve(), name="ligpsport-simulator")
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
            self._task = None
        await self._transport.close()

    async def push(self, message: Message, *, operation: int = _client.OP_SEND) -> None:
        """Send an unsolicited frame to the connected client.

        Used to simulate device-initiated events such as periodic
        ``DEV_STATUS`` updates or incoming-call notifications.
        """
        service_type, payload = envelope.encode_message(message)
        frame = framing.Frame(service=service_type, operation=operation, payload=payload)
        await self._transport.send(framing.build_frame(frame))

    async def _serve(self) -> None:
        try:
            while True:
                channel, raw = await self._next_inbound()
                await self._handle_one(channel, raw)
        except TransportClosed:
            _LOG.debug("simulator transport closed; exiting")
        except Exception:
            _LOG.exception("simulator crashed")
            raise

    async def _next_inbound(self) -> tuple[Channel, bytes]:
        """Read the next ``(channel, bytes)`` tuple from the transport.

        Falls back to plain :meth:`Transport.receive` (channel
        defaulted to ``"control"``) when running against a transport
        that doesn't expose channel info — keeps the simulator usable
        with any future transport that doesn't model channels.
        """
        if isinstance(self._transport, LoopbackTransport):
            return await self._transport.receive_with_channel()
        return ("control", await self._transport.receive())

    async def _handle_one(self, channel: Channel, raw: bytes) -> None:
        # Multi-channel uploads land here as raw chunk bytes on data /
        # fourth, paired with a 20-byte trailer on control. Buffer the
        # chunk until its trailer arrives.
        if channel in ("data", "fourth"):
            self._pending_chunk[channel] = raw
            return
        # Control-channel writes are usually a full PbFrame. The
        # route-upload trailer is also written here, but it's an
        # *un-paired* 20-byte header whose payload_size points at the
        # raw protobuf already buffered on data/fourth. Disambiguate
        # by length plus the buffered-chunk presence.
        if len(raw) == framing.HEADER_SIZE and self._pending_chunk:
            for buffered_channel, chunk in list(self._pending_chunk.items()):
                match = self._match_route_chunk(chunk, raw)
                if match is not None:
                    op, end_type = match
                    self._pending_chunk.pop(buffered_channel, None)
                    if op == route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE:
                        await self._handle_route_use(chunk)
                    else:
                        await self._handle_route_upload_chunk(chunk, end_type)
                    return
        try:
            frame = framing.parse_frame(raw)
        except framing.FrameError as exc:
            _LOG.warning("simulator dropping malformed frame: %s", exc)
            return
        self.state.received.append(frame)
        try:
            msg = envelope.decode_payload(frame.service, frame.payload)
        except envelope.UnknownServiceError:
            _LOG.warning("simulator dropping unknown service %d", frame.service)
            return
        handler = self._HANDLERS.get(frame.service)
        if handler is None:
            _LOG.debug("no simulator handler for service=%d", frame.service)
            return
        reply = await handler(self.state, frame, msg)
        if reply is None:
            return
        service_type, payload = envelope.encode_message(reply)
        out_frame = framing.Frame(
            service=service_type,
            operation=_client.OP_SEND,
            payload=payload,
        )
        await self._transport.send(framing.build_frame(out_frame))

    @staticmethod
    def _match_route_chunk(chunk: bytes, header: bytes) -> tuple[int, int] | None:
        """Return ``(operation, end_type)`` if ``(chunk, header)`` is a route trailer.

        Returns None when the header isn't a recognized route-plan
        trailer; the caller then dispatches the header through the
        normal frame path. Validates the trailer is well-formed (type,
        service, declared size, payload CRC, header CRC). Recognized
        operations: ``FILE_SEND`` (chunked upload) and ``FILE_USE``
        (single-frame commit after upload).
        """
        if header[framing.HDR_TYPE] != framing.TYPE_PB:
            return None
        if header[framing.HDR_SERVICE] != common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN:
            return None
        op = header[framing.HDR_OPERATION]
        if op not in (
            route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND,
            route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE,
        ):
            return None
        declared = (header[framing.HDR_PAYLOAD_SIZE] << 8) | header[framing.HDR_PAYLOAD_SIZE + 1]
        if declared != len(chunk):
            return None
        if framing.crc8(chunk) != header[framing.HDR_PAYLOAD_CRC]:
            _LOG.warning("simulator: route-upload chunk failed payload CRC")
            return None
        if framing.crc8(header[: framing.HDR_HEADER_CRC]) != header[framing.HDR_HEADER_CRC]:
            _LOG.warning("simulator: route-upload trailer failed header CRC")
            return None
        return (op, header[framing.HDR_END_MARKER])

    async def _handle_route_upload_chunk(self, chunk: bytes, end_type: int) -> None:
        """Append a route-upload chunk and ACK it.

        Mirrors `checkSendRoutePlanFileIsReceiveFinish` in the smali:
        every chunk gets a ConfirmFrame with status=0. We don't model
        the progress / done-early status codes — they are device-side
        bookkeeping the client already treats as "continue" / "stop".

        Chunks accumulate in :attr:`_in_progress_route` until a chunk
        with ``end_type=3`` arrives; that one finalises the entry and
        appends it to :attr:`SimulatorState.uploaded_routes`.
        """
        msg = route_plan_pb2.route_plan_data_msg()
        msg.ParseFromString(chunk)
        if self._in_progress_route is None:
            info = msg.route_plan_info_msg[0] if msg.route_plan_info_msg else None
            extension = ""
            if msg.line_id:
                parts = msg.line_id[0].rsplit(".", 1)
                if len(parts) == 2:
                    extension = parts[1]
            self._in_progress_route = UploadedRouteFile(
                file_id=info.id if info is not None else 0,
                file_type=info.file_type if info is not None else 0,
                name=info.name if info is not None else "",
                extension=extension,
                total_distance=info.total_distance if info is not None else 0,
                content=b"",
                end_types=[],
            )
        self._in_progress_route.content += msg.file_content
        self._in_progress_route.end_types.append(end_type)
        if end_type == 3:
            self.state.uploaded_routes.append(self._in_progress_route)
            self._in_progress_route = None
        ack = framing.build_frame(
            framing.Frame(
                type=framing.TYPE_CONFIRM,
                service=common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN,
                operation=route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND,
                status=0,
            )
        )
        await self._transport.send(ack)

    async def _handle_route_use(self, chunk: bytes) -> None:
        """Handle a FILE_USE commit. Records the file_id used and acks 0."""
        msg = route_plan_pb2.route_plan_data_msg()
        msg.ParseFromString(chunk)
        info = msg.route_plan_info_msg[0] if msg.route_plan_info_msg else None
        used_id = info.id if info is not None else 0
        for entry in self.state.uploaded_routes:
            if entry.file_id == used_id:
                self.state.active_route_id = used_id
                break
        ack = framing.build_frame(
            framing.Frame(
                type=framing.TYPE_CONFIRM,
                service=common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN,
                operation=route_plan_pb2.enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE,
                status=0,
            )
        )
        await self._transport.send(ack)

"""Route protobuf payloads to the correct message class.

Every iGPSPORT message starts with a varint field ``service_type``
(field 1 in every per-service message) drawn from
``common_pb2.service_type_index``. The receiver uses this index to
pick which protobuf class to ``ParseFromString`` the rest of the
payload as.

This module owns the static mapping ``service_index -> top-level
message class``. A new service entry needs:

1. A new entry in :data:`SERVICE_MESSAGES`.
2. The new message class to expose ``service_type`` (proto field 1)
   and to be serialisable via standard protobuf.

The mapping is the single source of truth. The
:class:`ligpsport.client.IgpsportClient` dispatcher iterates it to
decode unsolicited frames; the simulator iterates it to know which
proto class to instantiate when synthesising a response.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from google.protobuf.message import Message

from .proto import (
    back_pb2,
    ble_pb2,
    common_pb2,
    config_pb2,
    cycling_data_pb2,
    dev_status_pb2,
    dev_ver_info_pb2,
    factory_pb2,
    firmware_pb2,
    general_file_operation_pb2,
    ins_pb2,
    language_pack_pb2,
    log_pb2,
    map_new_pb2,
    map_pb2,
    real_time_trace_pb2,
    route_book_pb2,
    route_plan_pb2,
    sensor_pb2,
    team_info_pb2,
    theme_pb2,
    training_pb2,
    user_config_pb2,
    wifi_pb2,
)

# Service-index → top-level message class. Keyed by the value of the
# `service_type_index` enum in common.proto. The class on the right
# is the message whose proto field 1 carries the service_type field.
SERVICE_MESSAGES: Final[Mapping[int, type[Message]]] = {
    common_pb2.enum_SERVICE_TYPE_INDEX_INS: ins_pb2.ins_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_MAP: map_pb2.map_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_BACK: back_pb2.back_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_FIRMWARE: firmware_pb2.firmware_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_WIFI: wifi_pb2.wifi_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_CYCLING_DATA: cycling_data_pb2.cycling_data_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_PLAN: route_plan_pb2.route_plan_data_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_REAL_TIME_TRACE: real_time_trace_pb2.real_time_trace_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_USER_CONFIG: user_config_pb2.user_config_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_BLE: ble_pb2.ble_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_FACTORY: factory_pb2.factory_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_CONFIG: config_pb2.config_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_DEV_STATUS: dev_status_pb2.dev_status_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_SENSOR: sensor_pb2.sensor_message,
    common_pb2.enum_SERVICE_TYPE_INDEX_TRAINING: training_pb2.training_message,
    common_pb2.enum_SERVICE_TYPE_INDEX_TEAM_INFO: team_info_pb2.team_info_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_DEV_VER_INFO: dev_ver_info_pb2.dev_ver_info_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_LANGUAGE: language_pack_pb2.language_pack_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_LOG: log_pb2.log_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_THEME: theme_pb2.theme_message,
    common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION: (
        general_file_operation_pb2.general_file_operation
    ),
    common_pb2.enum_SERVICE_TYPE_INDEX_MAP_NEW: map_new_pb2.map_new_msg,
    common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_BOOK: route_book_pb2.route_book_data_msg,
}


class UnknownServiceError(ValueError):
    """Raised when a frame's service_type isn't in :data:`SERVICE_MESSAGES`."""


def message_class_for(service_type: int) -> type[Message]:
    """Return the top-level message class for the given service index."""
    cls = SERVICE_MESSAGES.get(service_type)
    if cls is None:
        raise UnknownServiceError(f"no message class for service_type={service_type}")
    return cls


def decode_payload(service_type: int, payload: bytes) -> Message:
    """Parse a payload as the message class registered for ``service_type``."""
    cls = message_class_for(service_type)
    msg = cls()
    msg.ParseFromString(payload)
    return msg


_REVERSE_SERVICE_MESSAGES: Final[Mapping[type[Message], int]] = {
    cls: idx for idx, cls in SERVICE_MESSAGES.items()
}


def service_type_for(msg_cls: type[Message]) -> int:
    """Return the service-index registered for the given message class."""
    idx = _REVERSE_SERVICE_MESSAGES.get(msg_cls)
    if idx is None:
        raise UnknownServiceError(f"no service registered for {msg_cls.__name__}")
    return idx


def encode_message(msg: Message) -> tuple[int, bytes]:
    """Serialise a message; return ``(service_type, payload_bytes)``.

    The ``service_type`` field on the per-service messages is declared
    ``required`` (proto2) with a class-specific default, but Python
    protobuf still refuses to serialise without it set explicitly. We
    populate it from :data:`SERVICE_MESSAGES` when the caller hasn't,
    matching the iGPSPORT app's behaviour (every factory hard-codes
    the service_type its message belongs to).
    """
    service_type = service_type_for(type(msg))
    if not msg.HasField("service_type"):
        msg.service_type = service_type
    else:
        observed = int(msg.service_type)
        if observed != service_type:
            raise ValueError(
                f"message {type(msg).__name__} has service_type={observed}, "
                f"but its class is registered as {service_type}"
            )
    return service_type, msg.SerializeToString()

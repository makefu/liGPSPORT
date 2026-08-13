from . import peripheral_common_pb2 as _peripheral_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_CONFIG_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PCS_UNSPECIFIED: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_SHUTDOWN: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_SLEEP: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_LIGHT_MODE: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_DATA_BROADCAST: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_ALL_CONFIG: _ClassVar[PERIPHERAL_CONFIG_SERVICE]
    PCS_ALL_CONFIG_RESET: _ClassVar[PERIPHERAL_CONFIG_SERVICE]

class enum_PERIPHERAL_CONFIG_LIGHT_MODE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PCLM_UNSPECIFIED: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_OFF: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_DEFAULT: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_TEAM: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_GRADIENT: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_NIGHT: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]
    DEVICE_SCENE_DAYLIGHT: _ClassVar[enum_PERIPHERAL_CONFIG_LIGHT_MODE]

class PERIPHERAL_CONFIG_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PCO_UNSPECIFIED: _ClassVar[PERIPHERAL_CONFIG_OPERATE]
PCS_UNSPECIFIED: PERIPHERAL_CONFIG_SERVICE
PCS_SHUTDOWN: PERIPHERAL_CONFIG_SERVICE
PCS_SLEEP: PERIPHERAL_CONFIG_SERVICE
PCS_LIGHT_MODE: PERIPHERAL_CONFIG_SERVICE
PCS_DATA_BROADCAST: PERIPHERAL_CONFIG_SERVICE
PCS_ALL_CONFIG: PERIPHERAL_CONFIG_SERVICE
PCS_ALL_CONFIG_RESET: PERIPHERAL_CONFIG_SERVICE
PCLM_UNSPECIFIED: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_OFF: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_DEFAULT: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_TEAM: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_GRADIENT: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_NIGHT: enum_PERIPHERAL_CONFIG_LIGHT_MODE
DEVICE_SCENE_DAYLIGHT: enum_PERIPHERAL_CONFIG_LIGHT_MODE
PCO_UNSPECIFIED: PERIPHERAL_CONFIG_OPERATE

class peripheral_config_data_shutdown(_message.Message):
    __slots__ = ("shutdown_switch", "countdown")
    SHUTDOWN_SWITCH_FIELD_NUMBER: _ClassVar[int]
    COUNTDOWN_FIELD_NUMBER: _ClassVar[int]
    shutdown_switch: bool
    countdown: int
    def __init__(self, shutdown_switch: _Optional[bool] = ..., countdown: _Optional[int] = ...) -> None: ...

class peripheral_config_data_sleep(_message.Message):
    __slots__ = ("sleep_switch", "countdown")
    SLEEP_SWITCH_FIELD_NUMBER: _ClassVar[int]
    COUNTDOWN_FIELD_NUMBER: _ClassVar[int]
    sleep_switch: bool
    countdown: int
    def __init__(self, sleep_switch: _Optional[bool] = ..., countdown: _Optional[int] = ...) -> None: ...

class peripheral_config_light_mode(_message.Message):
    __slots__ = ("light_mode",)
    LIGHT_MODE_FIELD_NUMBER: _ClassVar[int]
    light_mode: enum_PERIPHERAL_CONFIG_LIGHT_MODE
    def __init__(self, light_mode: _Optional[_Union[enum_PERIPHERAL_CONFIG_LIGHT_MODE, str]] = ...) -> None: ...

class peripheral_config_data_broadcast(_message.Message):
    __slots__ = ("data_switch",)
    DATA_SWITCH_FIELD_NUMBER: _ClassVar[int]
    data_switch: bool
    def __init__(self, data_switch: _Optional[bool] = ...) -> None: ...

class peripheral_config_message(_message.Message):
    __slots__ = ("shutdown", "sleep", "light", "data_service")
    SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    SLEEP_FIELD_NUMBER: _ClassVar[int]
    LIGHT_FIELD_NUMBER: _ClassVar[int]
    DATA_SERVICE_FIELD_NUMBER: _ClassVar[int]
    shutdown: peripheral_config_data_shutdown
    sleep: peripheral_config_data_sleep
    light: peripheral_config_light_mode
    data_service: peripheral_config_data_broadcast
    def __init__(self, shutdown: _Optional[_Union[peripheral_config_data_shutdown, _Mapping]] = ..., sleep: _Optional[_Union[peripheral_config_data_sleep, _Mapping]] = ..., light: _Optional[_Union[peripheral_config_light_mode, _Mapping]] = ..., data_service: _Optional[_Union[peripheral_config_data_broadcast, _Mapping]] = ...) -> None: ...

class peripheral_config_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_CONFIG_SERVICE
    sub_operate_type: PERIPHERAL_CONFIG_OPERATE
    message: peripheral_config_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_CONFIG_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_CONFIG_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_config_message, _Mapping]] = ...) -> None: ...

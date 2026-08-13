from . import peripheral_common_pb2 as _peripheral_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_RADAR_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHS_NSPECIFIED_RADAR: _ClassVar[PERIPHERAL_RADAR_SERVICE]

class PERIPHERAL_RADAR_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHO_NSPECIFIED_RADAR: _ClassVar[PERIPHERAL_RADAR_OPERATE]
    PHO_RADAR_TARGET: _ClassVar[PERIPHERAL_RADAR_OPERATE]
    PHO_ACC_SAMPLE: _ClassVar[PERIPHERAL_RADAR_OPERATE]
PHS_NSPECIFIED_RADAR: PERIPHERAL_RADAR_SERVICE
PHO_NSPECIFIED_RADAR: PERIPHERAL_RADAR_OPERATE
PHO_RADAR_TARGET: PERIPHERAL_RADAR_OPERATE
PHO_ACC_SAMPLE: PERIPHERAL_RADAR_OPERATE

class peripheral_radar_target_message(_message.Message):
    __slots__ = ("level", "range", "speed")
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    level: int
    range: int
    speed: int
    def __init__(self, level: _Optional[int] = ..., range: _Optional[int] = ..., speed: _Optional[int] = ...) -> None: ...

class peripheral_acc_message(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    z: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., z: _Optional[int] = ...) -> None: ...

class peripheral_radar_message(_message.Message):
    __slots__ = ("radar_info", "acc_info")
    RADAR_INFO_FIELD_NUMBER: _ClassVar[int]
    ACC_INFO_FIELD_NUMBER: _ClassVar[int]
    radar_info: _containers.RepeatedCompositeFieldContainer[peripheral_radar_target_message]
    acc_info: _containers.RepeatedCompositeFieldContainer[peripheral_acc_message]
    def __init__(self, radar_info: _Optional[_Iterable[_Union[peripheral_radar_target_message, _Mapping]]] = ..., acc_info: _Optional[_Iterable[_Union[peripheral_acc_message, _Mapping]]] = ...) -> None: ...

class peripheral_radar_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "meaagse")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEAAGSE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_RADAR_SERVICE
    sub_operate_type: PERIPHERAL_RADAR_OPERATE
    meaagse: peripheral_radar_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_RADAR_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_RADAR_OPERATE, str]] = ..., meaagse: _Optional[_Union[peripheral_radar_message, _Mapping]] = ...) -> None: ...

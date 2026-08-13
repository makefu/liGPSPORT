from . import peripheral_common_pb2 as _peripheral_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_HR_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHS_NSPECIFIED: _ClassVar[PERIPHERAL_HR_SERVICE]
    PHS_HRM_WARN: _ClassVar[PERIPHERAL_HR_SERVICE]
    PHS_HRM_ZONE: _ClassVar[PERIPHERAL_HR_SERVICE]
    PHS_SPORT_MODE: _ClassVar[PERIPHERAL_HR_SERVICE]

class PERIPHERAL_HR_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHO_NSPECIFIED: _ClassVar[PERIPHERAL_HR_OPERATE]

class PERIPHERAL_HR_WARN_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHW_UNSPECIFIED: _ClassVar[PERIPHERAL_HR_WARN_TYPE]
    PHW_CUSTOM: _ClassVar[PERIPHERAL_HR_WARN_TYPE]
    PHW_ZONE: _ClassVar[PERIPHERAL_HR_WARN_TYPE]

class PERIPHERAL_HR_SPORT_MODE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHSM_UNSPECIFIED: _ClassVar[PERIPHERAL_HR_SPORT_MODE_TYPE]
    PHSM_DEFAULT: _ClassVar[PERIPHERAL_HR_SPORT_MODE_TYPE]
    PHSM_RUN: _ClassVar[PERIPHERAL_HR_SPORT_MODE_TYPE]
    PHSM_BIKE: _ClassVar[PERIPHERAL_HR_SPORT_MODE_TYPE]
    PHSM_FITNESS: _ClassVar[PERIPHERAL_HR_SPORT_MODE_TYPE]
PHS_NSPECIFIED: PERIPHERAL_HR_SERVICE
PHS_HRM_WARN: PERIPHERAL_HR_SERVICE
PHS_HRM_ZONE: PERIPHERAL_HR_SERVICE
PHS_SPORT_MODE: PERIPHERAL_HR_SERVICE
PHO_NSPECIFIED: PERIPHERAL_HR_OPERATE
PHW_UNSPECIFIED: PERIPHERAL_HR_WARN_TYPE
PHW_CUSTOM: PERIPHERAL_HR_WARN_TYPE
PHW_ZONE: PERIPHERAL_HR_WARN_TYPE
PHSM_UNSPECIFIED: PERIPHERAL_HR_SPORT_MODE_TYPE
PHSM_DEFAULT: PERIPHERAL_HR_SPORT_MODE_TYPE
PHSM_RUN: PERIPHERAL_HR_SPORT_MODE_TYPE
PHSM_BIKE: PERIPHERAL_HR_SPORT_MODE_TYPE
PHSM_FITNESS: PERIPHERAL_HR_SPORT_MODE_TYPE

class peripheral_hr_data_warn(_message.Message):
    __slots__ = ("warn_switch", "high_switch", "low_switch", "high_warn_type", "low_warn_type", "high_value", "low_value")
    WARN_SWITCH_FIELD_NUMBER: _ClassVar[int]
    HIGH_SWITCH_FIELD_NUMBER: _ClassVar[int]
    LOW_SWITCH_FIELD_NUMBER: _ClassVar[int]
    HIGH_WARN_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOW_WARN_TYPE_FIELD_NUMBER: _ClassVar[int]
    HIGH_VALUE_FIELD_NUMBER: _ClassVar[int]
    LOW_VALUE_FIELD_NUMBER: _ClassVar[int]
    warn_switch: bool
    high_switch: bool
    low_switch: bool
    high_warn_type: PERIPHERAL_HR_WARN_TYPE
    low_warn_type: PERIPHERAL_HR_WARN_TYPE
    high_value: int
    low_value: int
    def __init__(self, warn_switch: _Optional[bool] = ..., high_switch: _Optional[bool] = ..., low_switch: _Optional[bool] = ..., high_warn_type: _Optional[_Union[PERIPHERAL_HR_WARN_TYPE, str]] = ..., low_warn_type: _Optional[_Union[PERIPHERAL_HR_WARN_TYPE, str]] = ..., high_value: _Optional[int] = ..., low_value: _Optional[int] = ...) -> None: ...

class peripheral_hr_data_zone(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, value: _Optional[_Iterable[int]] = ...) -> None: ...

class peripheral_hr_data_sport_mode(_message.Message):
    __slots__ = ("key_switch", "mode")
    KEY_SWITCH_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    key_switch: bool
    mode: PERIPHERAL_HR_SPORT_MODE_TYPE
    def __init__(self, key_switch: _Optional[bool] = ..., mode: _Optional[_Union[PERIPHERAL_HR_SPORT_MODE_TYPE, str]] = ...) -> None: ...

class peripheral_hr_message(_message.Message):
    __slots__ = ("hrm_warn", "hr_zone", "sport_mode")
    HRM_WARN_FIELD_NUMBER: _ClassVar[int]
    HR_ZONE_FIELD_NUMBER: _ClassVar[int]
    SPORT_MODE_FIELD_NUMBER: _ClassVar[int]
    hrm_warn: peripheral_hr_data_warn
    hr_zone: peripheral_hr_data_zone
    sport_mode: peripheral_hr_data_sport_mode
    def __init__(self, hrm_warn: _Optional[_Union[peripheral_hr_data_warn, _Mapping]] = ..., hr_zone: _Optional[_Union[peripheral_hr_data_zone, _Mapping]] = ..., sport_mode: _Optional[_Union[peripheral_hr_data_sport_mode, _Mapping]] = ...) -> None: ...

class peripheral_hr_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_HR_SERVICE
    sub_operate_type: PERIPHERAL_HR_OPERATE
    message: peripheral_hr_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_HR_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_HR_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_hr_message, _Mapping]] = ...) -> None: ...

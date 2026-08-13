from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class USER_CONFIG_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_USER_CONFIG_OPERATE_TYPE_NONE: _ClassVar[USER_CONFIG_OPERATE_TYPE]
    enum_USER_CONFIG_OPERATE_TYPE_SET: _ClassVar[USER_CONFIG_OPERATE_TYPE]
    enum_USER_CONFIG_OPERATE_TYPE_GET: _ClassVar[USER_CONFIG_OPERATE_TYPE]
enum_USER_CONFIG_OPERATE_TYPE_NONE: USER_CONFIG_OPERATE_TYPE
enum_USER_CONFIG_OPERATE_TYPE_SET: USER_CONFIG_OPERATE_TYPE
enum_USER_CONFIG_OPERATE_TYPE_GET: USER_CONFIG_OPERATE_TYPE

class user_config_data_msg(_message.Message):
    __slots__ = ("sex", "weight", "age", "height", "wheel_dia", "bike_weight", "time_zone", "member_id")
    SEX_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WHEEL_DIA_FIELD_NUMBER: _ClassVar[int]
    BIKE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    sex: int
    weight: int
    age: int
    height: int
    wheel_dia: int
    bike_weight: int
    time_zone: int
    member_id: str
    def __init__(self, sex: _Optional[int] = ..., weight: _Optional[int] = ..., age: _Optional[int] = ..., height: _Optional[int] = ..., wheel_dia: _Optional[int] = ..., bike_weight: _Optional[int] = ..., time_zone: _Optional[int] = ..., member_id: _Optional[str] = ...) -> None: ...

class user_config_msg(_message.Message):
    __slots__ = ("service_type", "user_config_operate_type", "user_config_data_message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_CONFIG_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_CONFIG_DATA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    user_config_operate_type: USER_CONFIG_OPERATE_TYPE
    user_config_data_message: user_config_data_msg
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., user_config_operate_type: _Optional[_Union[USER_CONFIG_OPERATE_TYPE, str]] = ..., user_config_data_message: _Optional[_Union[user_config_data_msg, _Mapping]] = ...) -> None: ...

from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WIFI_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_WIFI_OPERATE_TYPE_NONE: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_STATUS_GET: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_STATUS_SEND: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_CTRL: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_LIST_GET: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_LIST_SEND: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_ASSIGN_SSID: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_AUTO_STATUS_GET: _ClassVar[WIFI_OPERATE_TYPE]
    enum_WIFI_OPERATE_TYPE_AUTO_STATUS_SEND: _ClassVar[WIFI_OPERATE_TYPE]
enum_WIFI_OPERATE_TYPE_NONE: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_STATUS_GET: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_STATUS_SEND: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_CTRL: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_LIST_GET: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_LIST_SEND: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_ASSIGN_SSID: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_AUTO_STATUS_GET: WIFI_OPERATE_TYPE
enum_WIFI_OPERATE_TYPE_AUTO_STATUS_SEND: WIFI_OPERATE_TYPE

class wifi_data_message(_message.Message):
    __slots__ = ("status", "ssid", "key", "open_status", "signal_strength")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    OPEN_STATUS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    status: int
    ssid: str
    key: str
    open_status: int
    signal_strength: int
    def __init__(self, status: _Optional[int] = ..., ssid: _Optional[str] = ..., key: _Optional[str] = ..., open_status: _Optional[int] = ..., signal_strength: _Optional[int] = ...) -> None: ...

class wifi_msg(_message.Message):
    __slots__ = ("service_type", "wifi_operate_type", "wifi_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    WIFI_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    WIFI_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    wifi_operate_type: WIFI_OPERATE_TYPE
    wifi_data_msg: _containers.RepeatedCompositeFieldContainer[wifi_data_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., wifi_operate_type: _Optional[_Union[WIFI_OPERATE_TYPE, str]] = ..., wifi_data_msg: _Optional[_Iterable[_Union[wifi_data_message, _Mapping]]] = ...) -> None: ...

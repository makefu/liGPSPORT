from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BLE_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_BLE_OPERATE_TYPE_NONE: _ClassVar[BLE_OPERATE_TYPE]
    enum_BLE_OPERATE_TYPE_BOND_INFO: _ClassVar[BLE_OPERATE_TYPE]
    enum_BLE_OPERATE_TYPE_BOND_REQ: _ClassVar[BLE_OPERATE_TYPE]
    enum_BLE_OPERATE_TYPE_CONNECT_STATUS: _ClassVar[BLE_OPERATE_TYPE]
    enum_BLE_OPERATE_TYPE_UNBOND: _ClassVar[BLE_OPERATE_TYPE]
enum_BLE_OPERATE_TYPE_NONE: BLE_OPERATE_TYPE
enum_BLE_OPERATE_TYPE_BOND_INFO: BLE_OPERATE_TYPE
enum_BLE_OPERATE_TYPE_BOND_REQ: BLE_OPERATE_TYPE
enum_BLE_OPERATE_TYPE_CONNECT_STATUS: BLE_OPERATE_TYPE
enum_BLE_OPERATE_TYPE_UNBOND: BLE_OPERATE_TYPE

class ble_data_message(_message.Message):
    __slots__ = ("status", "member_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    status: int
    member_id: str
    def __init__(self, status: _Optional[int] = ..., member_id: _Optional[str] = ...) -> None: ...

class ble_msg(_message.Message):
    __slots__ = ("service_type", "ble_operate_type", "ble_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BLE_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BLE_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    ble_operate_type: BLE_OPERATE_TYPE
    ble_data_msg: _containers.RepeatedCompositeFieldContainer[ble_data_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., ble_operate_type: _Optional[_Union[BLE_OPERATE_TYPE, str]] = ..., ble_data_msg: _Optional[_Iterable[_Union[ble_data_message, _Mapping]]] = ...) -> None: ...

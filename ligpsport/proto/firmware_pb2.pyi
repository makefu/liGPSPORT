from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FIRMWARE_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_FIRMWARE_OPERATE_TYPE_NONE: _ClassVar[FIRMWARE_OPERATE_TYPE]
    enum_FIRMWARE_OPERATE_TYPE_GET_VERSION: _ClassVar[FIRMWARE_OPERATE_TYPE]
    enum_FIRMWARE_OPERATE_TYPE_SEND_VERSION: _ClassVar[FIRMWARE_OPERATE_TYPE]
    enum_FIRMWARE_OPERATE_TYPE_MCU_UPDATE: _ClassVar[FIRMWARE_OPERATE_TYPE]
    enum_FIRMWARE_OPERATE_TYPE_PROGRESS: _ClassVar[FIRMWARE_OPERATE_TYPE]
    enum_FIRMWARE_OPERATE_TYPE_BLE_UPDATE: _ClassVar[FIRMWARE_OPERATE_TYPE]
enum_FIRMWARE_OPERATE_TYPE_NONE: FIRMWARE_OPERATE_TYPE
enum_FIRMWARE_OPERATE_TYPE_GET_VERSION: FIRMWARE_OPERATE_TYPE
enum_FIRMWARE_OPERATE_TYPE_SEND_VERSION: FIRMWARE_OPERATE_TYPE
enum_FIRMWARE_OPERATE_TYPE_MCU_UPDATE: FIRMWARE_OPERATE_TYPE
enum_FIRMWARE_OPERATE_TYPE_PROGRESS: FIRMWARE_OPERATE_TYPE
enum_FIRMWARE_OPERATE_TYPE_BLE_UPDATE: FIRMWARE_OPERATE_TYPE

class firmware_data_message(_message.Message):
    __slots__ = ("mcu_firmware_ver", "ble_firmware_ver", "firmware_size", "url", "process", "ble_boot_firmware_ver")
    MCU_FIRMWARE_VER_FIELD_NUMBER: _ClassVar[int]
    BLE_FIRMWARE_VER_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_SIZE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FIELD_NUMBER: _ClassVar[int]
    BLE_BOOT_FIRMWARE_VER_FIELD_NUMBER: _ClassVar[int]
    mcu_firmware_ver: int
    ble_firmware_ver: int
    firmware_size: int
    url: str
    process: int
    ble_boot_firmware_ver: int
    def __init__(self, mcu_firmware_ver: _Optional[int] = ..., ble_firmware_ver: _Optional[int] = ..., firmware_size: _Optional[int] = ..., url: _Optional[str] = ..., process: _Optional[int] = ..., ble_boot_firmware_ver: _Optional[int] = ...) -> None: ...

class firmware_msg(_message.Message):
    __slots__ = ("service_type", "firmware_operate_type", "firmware_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    firmware_operate_type: FIRMWARE_OPERATE_TYPE
    firmware_data_msg: firmware_data_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., firmware_operate_type: _Optional[_Union[FIRMWARE_OPERATE_TYPE, str]] = ..., firmware_data_msg: _Optional[_Union[firmware_data_message, _Mapping]] = ...) -> None: ...

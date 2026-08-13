from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_OPERATE_TYPE_NONE: _ClassVar[OPERATE_TYPE]
    enum_OPERATE_TYPE_SET: _ClassVar[OPERATE_TYPE]
    enum_OPERATE_TYPE_GET: _ClassVar[OPERATE_TYPE]
    enum_OPERATE_TYPE_SEND: _ClassVar[OPERATE_TYPE]
    enum_OPERATE_TYPE_ADD: _ClassVar[OPERATE_TYPE]
    enum_OPERATE_TYPE_DEL: _ClassVar[OPERATE_TYPE]
enum_OPERATE_TYPE_NONE: OPERATE_TYPE
enum_OPERATE_TYPE_SET: OPERATE_TYPE
enum_OPERATE_TYPE_GET: OPERATE_TYPE
enum_OPERATE_TYPE_SEND: OPERATE_TYPE
enum_OPERATE_TYPE_ADD: OPERATE_TYPE
enum_OPERATE_TYPE_DEL: OPERATE_TYPE

class version_msg(_message.Message):
    __slots__ = ("main_boot_ver", "main_app_ver", "ble_boot_ver", "ble_app_ver", "hardware_ver", "protocol_ver", "compile_time")
    MAIN_BOOT_VER_FIELD_NUMBER: _ClassVar[int]
    MAIN_APP_VER_FIELD_NUMBER: _ClassVar[int]
    BLE_BOOT_VER_FIELD_NUMBER: _ClassVar[int]
    BLE_APP_VER_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_VER_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VER_FIELD_NUMBER: _ClassVar[int]
    COMPILE_TIME_FIELD_NUMBER: _ClassVar[int]
    main_boot_ver: int
    main_app_ver: int
    ble_boot_ver: int
    ble_app_ver: int
    hardware_ver: int
    protocol_ver: int
    compile_time: str
    def __init__(self, main_boot_ver: _Optional[int] = ..., main_app_ver: _Optional[int] = ..., ble_boot_ver: _Optional[int] = ..., ble_app_ver: _Optional[int] = ..., hardware_ver: _Optional[int] = ..., protocol_ver: _Optional[int] = ..., compile_time: _Optional[str] = ...) -> None: ...

class dev_ver_info_msg(_message.Message):
    __slots__ = ("service_type", "operate_type", "version_message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    operate_type: OPERATE_TYPE
    version_message: version_msg
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate_type: _Optional[_Union[OPERATE_TYPE, str]] = ..., version_message: _Optional[_Union[version_msg, _Mapping]] = ...) -> None: ...

from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class service_type_index(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SERVICE_TYPE_INDEX_NONE: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_INS: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_MAP: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_BACK: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_FIRMWARE: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_WIFI: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_CYCLING_DATA: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_ROUTE_PLAN: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_REAL_TIME_TRACE: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_USER_CONFIG: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_BLE: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_FACTORY: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_CONFIG: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_DEV_STATUS: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_SENSOR: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_TRAINING: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_TEAM_INFO: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_DEV_VER_INFO: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_LANGUAGE: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_LOG: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_THEME: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_FILE_OPERATION: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_MAP_NEW: _ClassVar[service_type_index]
    enum_SERVICE_TYPE_INDEX_ROUTE_BOOK: _ClassVar[service_type_index]

class SERVICE_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SERVICE_OPERATE_TYPE_NONE: _ClassVar[SERVICE_OPERATE_TYPE]
    enum_SERVICE_OPERATE_TYPE_SET: _ClassVar[SERVICE_OPERATE_TYPE]
    enum_SERVICE_OPERATE_TYPE_GET: _ClassVar[SERVICE_OPERATE_TYPE]
    enum_SERVICE_OPERATE_TYPE_ADD: _ClassVar[SERVICE_OPERATE_TYPE]
    enum_SERVICE_OPERATE_TYPE_DEL: _ClassVar[SERVICE_OPERATE_TYPE]
enum_SERVICE_TYPE_INDEX_NONE: service_type_index
enum_SERVICE_TYPE_INDEX_INS: service_type_index
enum_SERVICE_TYPE_INDEX_MAP: service_type_index
enum_SERVICE_TYPE_INDEX_BACK: service_type_index
enum_SERVICE_TYPE_INDEX_FIRMWARE: service_type_index
enum_SERVICE_TYPE_INDEX_WIFI: service_type_index
enum_SERVICE_TYPE_INDEX_CYCLING_DATA: service_type_index
enum_SERVICE_TYPE_INDEX_ROUTE_PLAN: service_type_index
enum_SERVICE_TYPE_INDEX_REAL_TIME_TRACE: service_type_index
enum_SERVICE_TYPE_INDEX_USER_CONFIG: service_type_index
enum_SERVICE_TYPE_INDEX_BLE: service_type_index
enum_SERVICE_TYPE_INDEX_FACTORY: service_type_index
enum_SERVICE_TYPE_INDEX_CONFIG: service_type_index
enum_SERVICE_TYPE_INDEX_DEV_STATUS: service_type_index
enum_SERVICE_TYPE_INDEX_SENSOR: service_type_index
enum_SERVICE_TYPE_INDEX_TRAINING: service_type_index
enum_SERVICE_TYPE_INDEX_TEAM_INFO: service_type_index
enum_SERVICE_TYPE_INDEX_DEV_VER_INFO: service_type_index
enum_SERVICE_TYPE_INDEX_LANGUAGE: service_type_index
enum_SERVICE_TYPE_INDEX_LOG: service_type_index
enum_SERVICE_TYPE_INDEX_THEME: service_type_index
enum_SERVICE_TYPE_INDEX_FILE_OPERATION: service_type_index
enum_SERVICE_TYPE_INDEX_MAP_NEW: service_type_index
enum_SERVICE_TYPE_INDEX_ROUTE_BOOK: service_type_index
enum_SERVICE_OPERATE_TYPE_NONE: SERVICE_OPERATE_TYPE
enum_SERVICE_OPERATE_TYPE_SET: SERVICE_OPERATE_TYPE
enum_SERVICE_OPERATE_TYPE_GET: SERVICE_OPERATE_TYPE
enum_SERVICE_OPERATE_TYPE_ADD: SERVICE_OPERATE_TYPE
enum_SERVICE_OPERATE_TYPE_DEL: SERVICE_OPERATE_TYPE

class file_list_get_message(_message.Message):
    __slots__ = ("file_num", "file_list_support_num_max", "file_index_start", "file_index_end")
    FILE_NUM_FIELD_NUMBER: _ClassVar[int]
    FILE_LIST_SUPPORT_NUM_MAX_FIELD_NUMBER: _ClassVar[int]
    FILE_INDEX_START_FIELD_NUMBER: _ClassVar[int]
    FILE_INDEX_END_FIELD_NUMBER: _ClassVar[int]
    file_num: int
    file_list_support_num_max: int
    file_index_start: int
    file_index_end: int
    def __init__(self, file_num: _Optional[int] = ..., file_list_support_num_max: _Optional[int] = ..., file_index_start: _Optional[int] = ..., file_index_end: _Optional[int] = ...) -> None: ...

from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROUTE_PLAN_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_ROUTE_PLAN_OPERATE_TYPE_NONE: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_LIST_GET: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_LIST_SEND: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_FILE_DEL: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_FILES_DEL: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_LIST_NUM_GET: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]
    enum_ROUTE_PLAN_OPERATE_TYPE_RENAME: _ClassVar[ROUTE_PLAN_OPERATE_TYPE]

class ROUTE_PLAN_FILE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_ROUTE_PLAN_FILE_TYPE_INVALID: _ClassVar[ROUTE_PLAN_FILE_TYPE]
    enum_ROUTE_PLAN_FILE_TYPE_CNX: _ClassVar[ROUTE_PLAN_FILE_TYPE]
    enum_ROUTE_PLAN_FILE_TYPE_GPX: _ClassVar[ROUTE_PLAN_FILE_TYPE]
    enum_ROUTE_PLAN_FILE_TYPE_FIT: _ClassVar[ROUTE_PLAN_FILE_TYPE]
    enum_ROUTE_PLAN_FILE_TYPE_TCX: _ClassVar[ROUTE_PLAN_FILE_TYPE]
    enum_ROUTE_PLAN_FILE_TYPE_XML: _ClassVar[ROUTE_PLAN_FILE_TYPE]

class ROUTE_PLAN_FILE_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_INVALID_STATUS: _ClassVar[ROUTE_PLAN_FILE_STATUS]
    enum_USED_STATUS: _ClassVar[ROUTE_PLAN_FILE_STATUS]
    enum_UNUSED_STATUS: _ClassVar[ROUTE_PLAN_FILE_STATUS]
enum_ROUTE_PLAN_OPERATE_TYPE_NONE: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_LIST_GET: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_LIST_SEND: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_FILE_DEL: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_FILE_SEND: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_FILE_USE: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_FILES_DEL: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_LIST_NUM_GET: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_OPERATE_TYPE_RENAME: ROUTE_PLAN_OPERATE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_INVALID: ROUTE_PLAN_FILE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_CNX: ROUTE_PLAN_FILE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_GPX: ROUTE_PLAN_FILE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_FIT: ROUTE_PLAN_FILE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_TCX: ROUTE_PLAN_FILE_TYPE
enum_ROUTE_PLAN_FILE_TYPE_XML: ROUTE_PLAN_FILE_TYPE
enum_INVALID_STATUS: ROUTE_PLAN_FILE_STATUS
enum_USED_STATUS: ROUTE_PLAN_FILE_STATUS
enum_UNUSED_STATUS: ROUTE_PLAN_FILE_STATUS

class route_plan_info_message(_message.Message):
    __slots__ = ("id", "file_type", "name", "total_distance", "longitude_start", "latitude_start", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_START_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_START_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    file_type: ROUTE_PLAN_FILE_TYPE
    name: str
    total_distance: int
    longitude_start: float
    latitude_start: float
    status: ROUTE_PLAN_FILE_STATUS
    def __init__(self, id: _Optional[int] = ..., file_type: _Optional[_Union[ROUTE_PLAN_FILE_TYPE, str]] = ..., name: _Optional[str] = ..., total_distance: _Optional[int] = ..., longitude_start: _Optional[float] = ..., latitude_start: _Optional[float] = ..., status: _Optional[_Union[ROUTE_PLAN_FILE_STATUS, str]] = ...) -> None: ...

class route_plan_data_msg(_message.Message):
    __slots__ = ("service_type", "route_plan_operate_type", "line_id", "file_content", "route_plan_info_msg", "route_list_get_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PLAN_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    ROUTE_PLAN_INFO_MSG_FIELD_NUMBER: _ClassVar[int]
    ROUTE_LIST_GET_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    route_plan_operate_type: ROUTE_PLAN_OPERATE_TYPE
    line_id: _containers.RepeatedScalarFieldContainer[str]
    file_content: bytes
    route_plan_info_msg: _containers.RepeatedCompositeFieldContainer[route_plan_info_message]
    route_list_get_msg: _common_pb2.file_list_get_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., route_plan_operate_type: _Optional[_Union[ROUTE_PLAN_OPERATE_TYPE, str]] = ..., line_id: _Optional[_Iterable[str]] = ..., file_content: _Optional[bytes] = ..., route_plan_info_msg: _Optional[_Iterable[_Union[route_plan_info_message, _Mapping]]] = ..., route_list_get_msg: _Optional[_Union[_common_pb2.file_list_get_message, _Mapping]] = ...) -> None: ...

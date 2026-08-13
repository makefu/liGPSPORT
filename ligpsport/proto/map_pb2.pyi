from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MAP_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_MAP_OPERATE_TYPE_NONE: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_LIST_GET: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_LIST_SEND: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_ASSIGN_UPDATE: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_ALL_UPDATE: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_DOWNLOAD: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_SUCCESS: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_YPTE_CANCEL_DOWNLOAD: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_PROGRESS_GET: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_PROGRESS_UPLOAD: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_ASSIGN_DEL: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_OPERATE_TYPE_ALL_DEL: _ClassVar[MAP_OPERATE_TYPE]
    enum_MAP_CONFIG_CMD: _ClassVar[MAP_OPERATE_TYPE]
enum_MAP_OPERATE_TYPE_NONE: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_LIST_GET: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_LIST_SEND: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_ASSIGN_UPDATE: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_ALL_UPDATE: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_DOWNLOAD: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_SUCCESS: MAP_OPERATE_TYPE
enum_MAP_OPERATE_YPTE_CANCEL_DOWNLOAD: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_PROGRESS_GET: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_PROGRESS_UPLOAD: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_ASSIGN_DEL: MAP_OPERATE_TYPE
enum_MAP_OPERATE_TYPE_ALL_DEL: MAP_OPERATE_TYPE
enum_MAP_CONFIG_CMD: MAP_OPERATE_TYPE

class map_data_message(_message.Message):
    __slots__ = ("map_id", "area_id", "version", "url", "size", "area_type", "progress", "config")
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    AREA_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    AREA_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    map_id: int
    area_id: str
    version: int
    url: str
    size: int
    area_type: int
    progress: int
    config: int
    def __init__(self, map_id: _Optional[int] = ..., area_id: _Optional[str] = ..., version: _Optional[int] = ..., url: _Optional[str] = ..., size: _Optional[int] = ..., area_type: _Optional[int] = ..., progress: _Optional[int] = ..., config: _Optional[int] = ...) -> None: ...

class map_msg(_message.Message):
    __slots__ = ("service_type", "map_operate_type", "map_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    map_operate_type: MAP_OPERATE_TYPE
    map_data_msg: _containers.RepeatedCompositeFieldContainer[map_data_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., map_operate_type: _Optional[_Union[MAP_OPERATE_TYPE, str]] = ..., map_data_msg: _Optional[_Iterable[_Union[map_data_message, _Mapping]]] = ...) -> None: ...

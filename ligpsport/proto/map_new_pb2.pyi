from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class map_op_type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MAP_OP_INVALID: _ClassVar[map_op_type]
    MAP_OP_LIST_NUM_GET: _ClassVar[map_op_type]
    MAP_OP_LIST_GET: _ClassVar[map_op_type]
    MAP_OP_DOWNLOAD: _ClassVar[map_op_type]
    MAP_OP_UPDATE: _ClassVar[map_op_type]
    MAP_OP_DELETE: _ClassVar[map_op_type]
    MAP_OP_SET: _ClassVar[map_op_type]

class map_op_state(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MAP_OP_STATE_INVALID: _ClassVar[map_op_state]
    MAP_OP_STATE_START: _ClassVar[map_op_state]
    MAP_OP_STATE_END: _ClassVar[map_op_state]
MAP_OP_INVALID: map_op_type
MAP_OP_LIST_NUM_GET: map_op_type
MAP_OP_LIST_GET: map_op_type
MAP_OP_DOWNLOAD: map_op_type
MAP_OP_UPDATE: map_op_type
MAP_OP_DELETE: map_op_type
MAP_OP_SET: map_op_type
MAP_OP_STATE_INVALID: map_op_state
MAP_OP_STATE_START: map_op_state
MAP_OP_STATE_END: map_op_state

class map_list_message(_message.Message):
    __slots__ = ("map_country_name", "map_id", "map_coordinates")
    MAP_COUNTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    MAP_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    map_country_name: str
    map_id: int
    map_coordinates: str
    def __init__(self, map_country_name: _Optional[str] = ..., map_id: _Optional[int] = ..., map_coordinates: _Optional[str] = ...) -> None: ...

class map_new_msg(_message.Message):
    __slots__ = ("service_type", "map_op_type", "map_list_msg", "map_op_sta", "map_list_get_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_OP_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAP_LIST_MSG_FIELD_NUMBER: _ClassVar[int]
    MAP_OP_STA_FIELD_NUMBER: _ClassVar[int]
    MAP_LIST_GET_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    map_op_type: map_op_type
    map_list_msg: _containers.RepeatedCompositeFieldContainer[map_list_message]
    map_op_sta: map_op_state
    map_list_get_msg: _common_pb2.file_list_get_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., map_op_type: _Optional[_Union[map_op_type, str]] = ..., map_list_msg: _Optional[_Iterable[_Union[map_list_message, _Mapping]]] = ..., map_op_sta: _Optional[_Union[map_op_state, str]] = ..., map_list_get_msg: _Optional[_Union[_common_pb2.file_list_get_message, _Mapping]] = ...) -> None: ...

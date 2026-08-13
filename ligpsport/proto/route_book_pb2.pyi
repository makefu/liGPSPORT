from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROUTE_BOOK_SUB_OP_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_ROUTE_BOOK_GET_SUB_OP_TYPE_NONE: _ClassVar[ROUTE_BOOK_SUB_OP_TYPE]
    enum_ROUTE_BOOK_GET_SUB_OP_TYPE_LIST_NUM_GET: _ClassVar[ROUTE_BOOK_SUB_OP_TYPE]
    enum_ROUTE_BOOK_GET_SUB_OP_TYPE_LIST_GET: _ClassVar[ROUTE_BOOK_SUB_OP_TYPE]
    enum_ROUTE_BOOK_SET_SUB_OP_TYPE_USE: _ClassVar[ROUTE_BOOK_SUB_OP_TYPE]
    enum_ROUTE_BOOK_SET_SUB_OP_TYPE_RENAME: _ClassVar[ROUTE_BOOK_SUB_OP_TYPE]

class ROUTE_BOOK_FILE_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_ROUTE_BOOK_FILE_INVALID_STATUS: _ClassVar[ROUTE_BOOK_FILE_STATUS]
    enum_ROUTE_BOOK_FILE_USED_STATUS: _ClassVar[ROUTE_BOOK_FILE_STATUS]
    enum_ROUTE_BOOK_FILE_UNUSED_STATUS: _ClassVar[ROUTE_BOOK_FILE_STATUS]
enum_ROUTE_BOOK_GET_SUB_OP_TYPE_NONE: ROUTE_BOOK_SUB_OP_TYPE
enum_ROUTE_BOOK_GET_SUB_OP_TYPE_LIST_NUM_GET: ROUTE_BOOK_SUB_OP_TYPE
enum_ROUTE_BOOK_GET_SUB_OP_TYPE_LIST_GET: ROUTE_BOOK_SUB_OP_TYPE
enum_ROUTE_BOOK_SET_SUB_OP_TYPE_USE: ROUTE_BOOK_SUB_OP_TYPE
enum_ROUTE_BOOK_SET_SUB_OP_TYPE_RENAME: ROUTE_BOOK_SUB_OP_TYPE
enum_ROUTE_BOOK_FILE_INVALID_STATUS: ROUTE_BOOK_FILE_STATUS
enum_ROUTE_BOOK_FILE_USED_STATUS: ROUTE_BOOK_FILE_STATUS
enum_ROUTE_BOOK_FILE_UNUSED_STATUS: ROUTE_BOOK_FILE_STATUS

class route_book_infor_message(_message.Message):
    __slots__ = ("id", "name", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    status: ROUTE_BOOK_FILE_STATUS
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., status: _Optional[_Union[ROUTE_BOOK_FILE_STATUS, str]] = ...) -> None: ...

class route_book_data_msg(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_operate_type", "route_book_infor_msg", "route_book_list_get_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROUTE_BOOK_INFOR_MSG_FIELD_NUMBER: _ClassVar[int]
    ROUTE_BOOK_LIST_GET_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    operate_type: _common_pb2.SERVICE_OPERATE_TYPE
    sub_operate_type: ROUTE_BOOK_SUB_OP_TYPE
    route_book_infor_msg: _containers.RepeatedCompositeFieldContainer[route_book_infor_message]
    route_book_list_get_msg: _common_pb2.file_list_get_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate_type: _Optional[_Union[_common_pb2.SERVICE_OPERATE_TYPE, str]] = ..., sub_operate_type: _Optional[_Union[ROUTE_BOOK_SUB_OP_TYPE, str]] = ..., route_book_infor_msg: _Optional[_Iterable[_Union[route_book_infor_message, _Mapping]]] = ..., route_book_list_get_msg: _Optional[_Union[_common_pb2.file_list_get_message, _Mapping]] = ...) -> None: ...

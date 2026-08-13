from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LOG_SUB_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_LOG_INVALID: _ClassVar[LOG_SUB_OPERATE_TYPE]
    enum_LOG_NUMBER_GET: _ClassVar[LOG_SUB_OPERATE_TYPE]
    enum_LOG_GET: _ClassVar[LOG_SUB_OPERATE_TYPE]
enum_LOG_INVALID: LOG_SUB_OPERATE_TYPE
enum_LOG_NUMBER_GET: LOG_SUB_OPERATE_TYPE
enum_LOG_GET: LOG_SUB_OPERATE_TYPE

class log_msg(_message.Message):
    __slots__ = ("service", "operate", "sub_operate", "log_name", "content", "log_num")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_FIELD_NUMBER: _ClassVar[int]
    LOG_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LOG_NUM_FIELD_NUMBER: _ClassVar[int]
    service: _common_pb2.service_type_index
    operate: _common_pb2.SERVICE_OPERATE_TYPE
    sub_operate: LOG_SUB_OPERATE_TYPE
    log_name: str
    content: bytes
    log_num: int
    def __init__(self, service: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate: _Optional[_Union[_common_pb2.SERVICE_OPERATE_TYPE, str]] = ..., sub_operate: _Optional[_Union[LOG_SUB_OPERATE_TYPE, str]] = ..., log_name: _Optional[str] = ..., content: _Optional[bytes] = ..., log_num: _Optional[int] = ...) -> None: ...

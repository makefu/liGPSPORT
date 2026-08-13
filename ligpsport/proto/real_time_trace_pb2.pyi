from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class REAL_TIME_TRACE_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_REAL_TIME_TRACE_OPERATE_TYPE_NONE: _ClassVar[REAL_TIME_TRACE_OPERATE_TYPE]
    enum_REAL_TIME_TRACE_OPERATE_TYPE_GET: _ClassVar[REAL_TIME_TRACE_OPERATE_TYPE]
    enum_REAL_TIME_TRACE_OPERATE_TYPE_FIT: _ClassVar[REAL_TIME_TRACE_OPERATE_TYPE]
    enum_REAL_TIME_TRACE_OPERATE_TYPE_FINISH: _ClassVar[REAL_TIME_TRACE_OPERATE_TYPE]
    enum_REAL_TIME_TRACE_OPERATE_TYPE_END: _ClassVar[REAL_TIME_TRACE_OPERATE_TYPE]
enum_REAL_TIME_TRACE_OPERATE_TYPE_NONE: REAL_TIME_TRACE_OPERATE_TYPE
enum_REAL_TIME_TRACE_OPERATE_TYPE_GET: REAL_TIME_TRACE_OPERATE_TYPE
enum_REAL_TIME_TRACE_OPERATE_TYPE_FIT: REAL_TIME_TRACE_OPERATE_TYPE
enum_REAL_TIME_TRACE_OPERATE_TYPE_FINISH: REAL_TIME_TRACE_OPERATE_TYPE
enum_REAL_TIME_TRACE_OPERATE_TYPE_END: REAL_TIME_TRACE_OPERATE_TYPE

class real_time_trace_fit_message(_message.Message):
    __slots__ = ("timestamp", "fit_content")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FIT_CONTENT_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    fit_content: bytes
    def __init__(self, timestamp: _Optional[int] = ..., fit_content: _Optional[bytes] = ...) -> None: ...

class real_time_trace_msg(_message.Message):
    __slots__ = ("service_type", "real_time_trace_operate_type", "real_time_trace_fit_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_TRACE_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_TRACE_FIT_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    real_time_trace_operate_type: REAL_TIME_TRACE_OPERATE_TYPE
    real_time_trace_fit_msg: real_time_trace_fit_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., real_time_trace_operate_type: _Optional[_Union[REAL_TIME_TRACE_OPERATE_TYPE, str]] = ..., real_time_trace_fit_msg: _Optional[_Union[real_time_trace_fit_message, _Mapping]] = ...) -> None: ...

from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class file_operation_type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_FILE_TYPE_GENERAL: _ClassVar[file_operation_type]
    enum_FILE_TYPE_TRAINING: _ClassVar[file_operation_type]
    enum_FILE_TYPE_ROUTE_PLAN: _ClassVar[file_operation_type]
    enum_FILE_TYPE_MAP: _ClassVar[file_operation_type]
    enum_FILE_TYPE_THEME: _ClassVar[file_operation_type]
    enum_FILE_TYPE_FIRMWARE: _ClassVar[file_operation_type]
    enum_FILE_TYPE_LANGUAGE: _ClassVar[file_operation_type]
    enum_FILE_TYPE_AGPS: _ClassVar[file_operation_type]
    enum_FILE_TYPE_ROUTE_BOOK: _ClassVar[file_operation_type]
enum_FILE_TYPE_GENERAL: file_operation_type
enum_FILE_TYPE_TRAINING: file_operation_type
enum_FILE_TYPE_ROUTE_PLAN: file_operation_type
enum_FILE_TYPE_MAP: file_operation_type
enum_FILE_TYPE_THEME: file_operation_type
enum_FILE_TYPE_FIRMWARE: file_operation_type
enum_FILE_TYPE_LANGUAGE: file_operation_type
enum_FILE_TYPE_AGPS: file_operation_type
enum_FILE_TYPE_ROUTE_BOOK: file_operation_type

class general_file_operation(_message.Message):
    __slots__ = ("service_type", "operate_type", "file_type", "file_size", "file_id", "file_name", "file_extension", "file_md5")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILE_MD5_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    operate_type: _common_pb2.SERVICE_OPERATE_TYPE
    file_type: file_operation_type
    file_size: int
    file_id: int
    file_name: str
    file_extension: str
    file_md5: str
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate_type: _Optional[_Union[_common_pb2.SERVICE_OPERATE_TYPE, str]] = ..., file_type: _Optional[_Union[file_operation_type, str]] = ..., file_size: _Optional[int] = ..., file_id: _Optional[int] = ..., file_name: _Optional[str] = ..., file_extension: _Optional[str] = ..., file_md5: _Optional[str] = ...) -> None: ...

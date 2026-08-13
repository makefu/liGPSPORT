from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CYCLING_DATA_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_CYCLING_DATA_OPERATE_TYPE_NONE: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_LIST_SEND: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_FILE_GET: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_FILE_SEND: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_AUTO_UPLOAD: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
    enum_CYCLING_DATA_OPERATE_TYPE_LIST_NUM_GET: _ClassVar[CYCLING_DATA_OPERATE_TYPE]
enum_CYCLING_DATA_OPERATE_TYPE_NONE: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_LIST_GET: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_LIST_SEND: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_FILE_GET: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_FILE_SEND: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_FILE_DEL: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_ALL_DEL: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_AUTO_UPLOAD: CYCLING_DATA_OPERATE_TYPE
enum_CYCLING_DATA_OPERATE_TYPE_LIST_NUM_GET: CYCLING_DATA_OPERATE_TYPE

class cycling_data_file_flag_message(_message.Message):
    __slots__ = ("timestamp", "file_size", "user_id", "device_id")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    file_size: int
    user_id: str
    device_id: str
    def __init__(self, timestamp: _Optional[int] = ..., file_size: _Optional[int] = ..., user_id: _Optional[str] = ..., device_id: _Optional[str] = ...) -> None: ...

class cycling_data_auto_upload_message(_message.Message):
    __slots__ = ("status", "cycling_data_url", "cycling_data_check_url")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CYCLING_DATA_URL_FIELD_NUMBER: _ClassVar[int]
    CYCLING_DATA_CHECK_URL_FIELD_NUMBER: _ClassVar[int]
    status: int
    cycling_data_url: str
    cycling_data_check_url: str
    def __init__(self, status: _Optional[int] = ..., cycling_data_url: _Optional[str] = ..., cycling_data_check_url: _Optional[str] = ...) -> None: ...

class cycling_data_msg(_message.Message):
    __slots__ = ("service_type", "cycling_data_operate_type", "cycling_data_file_flag_msg", "file_content", "cycling_data_auto_upload_msg", "list_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CYCLING_DATA_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CYCLING_DATA_FILE_FLAG_MSG_FIELD_NUMBER: _ClassVar[int]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    CYCLING_DATA_AUTO_UPLOAD_MSG_FIELD_NUMBER: _ClassVar[int]
    LIST_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    cycling_data_operate_type: CYCLING_DATA_OPERATE_TYPE
    cycling_data_file_flag_msg: _containers.RepeatedCompositeFieldContainer[cycling_data_file_flag_message]
    file_content: bytes
    cycling_data_auto_upload_msg: cycling_data_auto_upload_message
    list_msg: _common_pb2.file_list_get_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., cycling_data_operate_type: _Optional[_Union[CYCLING_DATA_OPERATE_TYPE, str]] = ..., cycling_data_file_flag_msg: _Optional[_Iterable[_Union[cycling_data_file_flag_message, _Mapping]]] = ..., file_content: _Optional[bytes] = ..., cycling_data_auto_upload_msg: _Optional[_Union[cycling_data_auto_upload_message, _Mapping]] = ..., list_msg: _Optional[_Union[_common_pb2.file_list_get_message, _Mapping]] = ...) -> None: ...

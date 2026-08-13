from . import common_pb2 as _common_pb2
from . import config_pb2 as _config_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LANGUAGE_PACK_SUB_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_LANG_SUB_OPERATE_TYPE_INVALID: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    enum_LANG_SUB_OPERATE_TYPE_SET_DOWNLOAD_URL: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    enum_LANG_SUB_OPERATE_TYPE_GET_MODULE_INFO: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    enum_LANG_SUB_OPERATE_TYPE_GET_LIST: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    enum_LANG_SUB_OPERATE_TYPE_ADD_PACK: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    enum_LANG_SUB_OPERATE_TYPE_DEL_PACK: _ClassVar[LANGUAGE_PACK_SUB_OPERATE_TYPE]

class LANGUAGE_PACK_FONT_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_LANGUAGE_PACK_FONT_TYPE_INVALID: _ClassVar[LANGUAGE_PACK_FONT_TYPE]
    enum_DianDian: _ClassVar[LANGUAGE_PACK_FONT_TYPE]
enum_LANG_SUB_OPERATE_TYPE_INVALID: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANG_SUB_OPERATE_TYPE_SET_DOWNLOAD_URL: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANG_SUB_OPERATE_TYPE_GET_MODULE_INFO: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANG_SUB_OPERATE_TYPE_GET_LIST: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANG_SUB_OPERATE_TYPE_ADD_PACK: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANG_SUB_OPERATE_TYPE_DEL_PACK: LANGUAGE_PACK_SUB_OPERATE_TYPE
enum_LANGUAGE_PACK_FONT_TYPE_INVALID: LANGUAGE_PACK_FONT_TYPE
enum_DianDian: LANGUAGE_PACK_FONT_TYPE

class language_pack_module_info_msg(_message.Message):
    __slots__ = ("support_cmd", "language_pack_module_version")
    SUPPORT_CMD_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_PACK_MODULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    support_cmd: _containers.RepeatedScalarFieldContainer[LANGUAGE_PACK_SUB_OPERATE_TYPE]
    language_pack_module_version: int
    def __init__(self, support_cmd: _Optional[_Iterable[_Union[LANGUAGE_PACK_SUB_OPERATE_TYPE, str]]] = ..., language_pack_module_version: _Optional[int] = ...) -> None: ...

class language_pack_info_msg(_message.Message):
    __slots__ = ("language_type", "language_versin", "font_type", "font_size", "pack_size", "url", "md5_code")
    LANGUAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_VERSIN_FIELD_NUMBER: _ClassVar[int]
    FONT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FONT_SIZE_FIELD_NUMBER: _ClassVar[int]
    PACK_SIZE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    MD5_CODE_FIELD_NUMBER: _ClassVar[int]
    language_type: _config_pb2.LANGUAGE_TYPE
    language_versin: int
    font_type: LANGUAGE_PACK_FONT_TYPE
    font_size: int
    pack_size: int
    url: str
    md5_code: bytes
    def __init__(self, language_type: _Optional[_Union[_config_pb2.LANGUAGE_TYPE, str]] = ..., language_versin: _Optional[int] = ..., font_type: _Optional[_Union[LANGUAGE_PACK_FONT_TYPE, str]] = ..., font_size: _Optional[int] = ..., pack_size: _Optional[int] = ..., url: _Optional[str] = ..., md5_code: _Optional[bytes] = ...) -> None: ...

class language_pack_msg(_message.Message):
    __slots__ = ("service_type", "operate_type", "language_sub_operate", "language_pack_info_message", "content", "module_info_message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_SUB_OPERATE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_PACK_INFO_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    MODULE_INFO_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    operate_type: _common_pb2.SERVICE_OPERATE_TYPE
    language_sub_operate: LANGUAGE_PACK_SUB_OPERATE_TYPE
    language_pack_info_message: _containers.RepeatedCompositeFieldContainer[language_pack_info_msg]
    content: bytes
    module_info_message: language_pack_module_info_msg
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate_type: _Optional[_Union[_common_pb2.SERVICE_OPERATE_TYPE, str]] = ..., language_sub_operate: _Optional[_Union[LANGUAGE_PACK_SUB_OPERATE_TYPE, str]] = ..., language_pack_info_message: _Optional[_Iterable[_Union[language_pack_info_msg, _Mapping]]] = ..., content: _Optional[bytes] = ..., module_info_message: _Optional[_Union[language_pack_module_info_msg, _Mapping]] = ...) -> None: ...

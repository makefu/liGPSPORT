from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TRAINING_SUB_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TRAINING_SUB_OPERATE_TYPE_INAVLIDE: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_SET_USE: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_SET_NAME: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_SET_REMIND: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_GET_MODULE_INFO: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_GET_LIST: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_GET_LIST_NUM: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_ADD_FILE: _ClassVar[TRAINING_SUB_OPERATE_TYPE]
    enum_TRAINING_SUB_OPERATE_TYPE_DEL_FILE: _ClassVar[TRAINING_SUB_OPERATE_TYPE]

class TRAINING_FILE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TRAINING_FILE_TYPE_INVALIDE: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_JSON: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_XML: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_FIT: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_CSV: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_GPX: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_GZ: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_HRM: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_HST: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_PWPB: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_PWX: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_SDF: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_SRM: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_TCX: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_TXT: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_WKO: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_XLSX: _ClassVar[TRAINING_FILE_TYPE]
    enum_TRAINING_FILE_TYPE_CUSTOM: _ClassVar[TRAINING_FILE_TYPE]

class TRAINING_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TRAINING_TYPE_INVALID: _ClassVar[TRAINING_TYPE]
    enum_TRAINING_TYPE_WORKOUT: _ClassVar[TRAINING_TYPE]
    enum_TRAINING_TYPE_SEGMENT: _ClassVar[TRAINING_TYPE]
    enum_TRAINING_TYPE_INDOOR: _ClassVar[TRAINING_TYPE]
    enum_TRAINING_TYPE_CUSTOM: _ClassVar[TRAINING_TYPE]

class TRAINING_OBJECT(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TRAINING_OBJECT_INVALID: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_TIME: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_DISTANCE: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_SPD: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_CALORIE: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_CLIMB: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_PWR: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_PWR_ZONE: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_HRM: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_HRM_ZONE: _ClassVar[TRAINING_OBJECT]
    enum_TRAINING_OBJECT_CUSTOM: _ClassVar[TRAINING_OBJECT]

class TRAINING_FILE_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TRAINING_INVALID_STATUS: _ClassVar[TRAINING_FILE_STATUS]
    enum_TRAINING_USED_STATUS: _ClassVar[TRAINING_FILE_STATUS]
    enum_TRAINING_UNUSED_STATUS: _ClassVar[TRAINING_FILE_STATUS]
enum_TRAINING_SUB_OPERATE_TYPE_INAVLIDE: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_SET_USE: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_SET_NAME: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_SET_REMIND: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_GET_MODULE_INFO: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_GET_LIST: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_GET_LIST_NUM: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_ADD_FILE: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_SUB_OPERATE_TYPE_DEL_FILE: TRAINING_SUB_OPERATE_TYPE
enum_TRAINING_FILE_TYPE_INVALIDE: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_JSON: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_XML: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_FIT: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_CSV: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_GPX: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_GZ: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_HRM: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_HST: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_PWPB: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_PWX: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_SDF: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_SRM: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_TCX: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_TXT: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_WKO: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_XLSX: TRAINING_FILE_TYPE
enum_TRAINING_FILE_TYPE_CUSTOM: TRAINING_FILE_TYPE
enum_TRAINING_TYPE_INVALID: TRAINING_TYPE
enum_TRAINING_TYPE_WORKOUT: TRAINING_TYPE
enum_TRAINING_TYPE_SEGMENT: TRAINING_TYPE
enum_TRAINING_TYPE_INDOOR: TRAINING_TYPE
enum_TRAINING_TYPE_CUSTOM: TRAINING_TYPE
enum_TRAINING_OBJECT_INVALID: TRAINING_OBJECT
enum_TRAINING_OBJECT_TIME: TRAINING_OBJECT
enum_TRAINING_OBJECT_DISTANCE: TRAINING_OBJECT
enum_TRAINING_OBJECT_SPD: TRAINING_OBJECT
enum_TRAINING_OBJECT_CALORIE: TRAINING_OBJECT
enum_TRAINING_OBJECT_CLIMB: TRAINING_OBJECT
enum_TRAINING_OBJECT_PWR: TRAINING_OBJECT
enum_TRAINING_OBJECT_PWR_ZONE: TRAINING_OBJECT
enum_TRAINING_OBJECT_HRM: TRAINING_OBJECT
enum_TRAINING_OBJECT_HRM_ZONE: TRAINING_OBJECT
enum_TRAINING_OBJECT_CUSTOM: TRAINING_OBJECT
enum_TRAINING_INVALID_STATUS: TRAINING_FILE_STATUS
enum_TRAINING_USED_STATUS: TRAINING_FILE_STATUS
enum_TRAINING_UNUSED_STATUS: TRAINING_FILE_STATUS

class training_object_msg(_message.Message):
    __slots__ = ("trainning_obj", "data_max", "data_min")
    TRAINNING_OBJ_FIELD_NUMBER: _ClassVar[int]
    DATA_MAX_FIELD_NUMBER: _ClassVar[int]
    DATA_MIN_FIELD_NUMBER: _ClassVar[int]
    trainning_obj: TRAINING_OBJECT
    data_max: int
    data_min: int
    def __init__(self, trainning_obj: _Optional[_Union[TRAINING_OBJECT, str]] = ..., data_max: _Optional[int] = ..., data_min: _Optional[int] = ...) -> None: ...

class training_data_message(_message.Message):
    __slots__ = ("file_id", "file_name", "file_type", "training_period", "training_type", "training_object_message", "training_time", "file_content")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    TRAINING_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_OBJECT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_TIME_FIELD_NUMBER: _ClassVar[int]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    file_id: int
    file_name: str
    file_type: TRAINING_FILE_TYPE
    training_period: int
    training_type: TRAINING_TYPE
    training_object_message: training_object_msg
    training_time: int
    file_content: bytes
    def __init__(self, file_id: _Optional[int] = ..., file_name: _Optional[str] = ..., file_type: _Optional[_Union[TRAINING_FILE_TYPE, str]] = ..., training_period: _Optional[int] = ..., training_type: _Optional[_Union[TRAINING_TYPE, str]] = ..., training_object_message: _Optional[_Union[training_object_msg, _Mapping]] = ..., training_time: _Optional[int] = ..., file_content: _Optional[bytes] = ...) -> None: ...

class training_list_message(_message.Message):
    __slots__ = ("file_id", "file_type", "file_name", "status", "training_period")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAINING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    file_id: int
    file_type: TRAINING_FILE_TYPE
    file_name: str
    status: TRAINING_FILE_STATUS
    training_period: int
    def __init__(self, file_id: _Optional[int] = ..., file_type: _Optional[_Union[TRAINING_FILE_TYPE, str]] = ..., file_name: _Optional[str] = ..., status: _Optional[_Union[TRAINING_FILE_STATUS, str]] = ..., training_period: _Optional[int] = ...) -> None: ...

class training_module_info_message(_message.Message):
    __slots__ = ("sub_operate_type", "training_module_version")
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_MODULE_VERSION_FIELD_NUMBER: _ClassVar[int]
    sub_operate_type: _containers.RepeatedScalarFieldContainer[TRAINING_SUB_OPERATE_TYPE]
    training_module_version: int
    def __init__(self, sub_operate_type: _Optional[_Iterable[_Union[TRAINING_SUB_OPERATE_TYPE, str]]] = ..., training_module_version: _Optional[int] = ...) -> None: ...

class training_message(_message.Message):
    __slots__ = ("service_type", "operate_type", "training_sub_operate_type", "training_data_msg", "training_list_get_msg", "training_list_msg", "module_info_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRAINING_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    TRAINING_LIST_GET_MSG_FIELD_NUMBER: _ClassVar[int]
    TRAINING_LIST_MSG_FIELD_NUMBER: _ClassVar[int]
    MODULE_INFO_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    operate_type: _common_pb2.SERVICE_OPERATE_TYPE
    training_sub_operate_type: TRAINING_SUB_OPERATE_TYPE
    training_data_msg: training_data_message
    training_list_get_msg: _common_pb2.file_list_get_message
    training_list_msg: _containers.RepeatedCompositeFieldContainer[training_list_message]
    module_info_msg: training_module_info_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., operate_type: _Optional[_Union[_common_pb2.SERVICE_OPERATE_TYPE, str]] = ..., training_sub_operate_type: _Optional[_Union[TRAINING_SUB_OPERATE_TYPE, str]] = ..., training_data_msg: _Optional[_Union[training_data_message, _Mapping]] = ..., training_list_get_msg: _Optional[_Union[_common_pb2.file_list_get_message, _Mapping]] = ..., training_list_msg: _Optional[_Iterable[_Union[training_list_message, _Mapping]]] = ..., module_info_msg: _Optional[_Union[training_module_info_message, _Mapping]] = ...) -> None: ...

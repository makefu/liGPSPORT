from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class INS_SERVICE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_INS_SERVICE_TYPE_NONE: _ClassVar[INS_SERVICE_TYPE]
    enum_INS_SERVICE_TYPE_MAIN: _ClassVar[INS_SERVICE_TYPE]
    enum_INS_SERVICE_TYPE_CALL: _ClassVar[INS_SERVICE_TYPE]
    enum_INS_SERVICE_TYPE_NOTE: _ClassVar[INS_SERVICE_TYPE]

class INS_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_INS_OPERATE_TYPE_NONE: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_CTRL: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_INCOMING_CALL: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_ANSWER_CALL: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_REJECT_CALL: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_CHECK_CALL: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_INCOMING_NOTE: _ClassVar[INS_OPERATE_TYPE]
    enum_INS_OPERATE_TYPE_CHECK_NOTE: _ClassVar[INS_OPERATE_TYPE]

class ANCS_CATAGORY_ID(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OTHER: _ClassVar[ANCS_CATAGORY_ID]
    INCOMING_CALL: _ClassVar[ANCS_CATAGORY_ID]
    MISSED_CALL: _ClassVar[ANCS_CATAGORY_ID]
    VOICE_MAIL: _ClassVar[ANCS_CATAGORY_ID]
    SOCIAL: _ClassVar[ANCS_CATAGORY_ID]
    ID_SCHEDULE: _ClassVar[ANCS_CATAGORY_ID]
    ID_EMAIL: _ClassVar[ANCS_CATAGORY_ID]
    NEWS: _ClassVar[ANCS_CATAGORY_ID]
    HEALTH_AND_FITNESS: _ClassVar[ANCS_CATAGORY_ID]
    BUSINESS_AND_FINANCE: _ClassVar[ANCS_CATAGORY_ID]
    LOCATION: _ClassVar[ANCS_CATAGORY_ID]
    ENTERTAINMENT: _ClassVar[ANCS_CATAGORY_ID]
enum_INS_SERVICE_TYPE_NONE: INS_SERVICE_TYPE
enum_INS_SERVICE_TYPE_MAIN: INS_SERVICE_TYPE
enum_INS_SERVICE_TYPE_CALL: INS_SERVICE_TYPE
enum_INS_SERVICE_TYPE_NOTE: INS_SERVICE_TYPE
enum_INS_OPERATE_TYPE_NONE: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_CTRL: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_INCOMING_CALL: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_ANSWER_CALL: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_REJECT_CALL: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_CHECK_CALL: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_INCOMING_NOTE: INS_OPERATE_TYPE
enum_INS_OPERATE_TYPE_CHECK_NOTE: INS_OPERATE_TYPE
OTHER: ANCS_CATAGORY_ID
INCOMING_CALL: ANCS_CATAGORY_ID
MISSED_CALL: ANCS_CATAGORY_ID
VOICE_MAIL: ANCS_CATAGORY_ID
SOCIAL: ANCS_CATAGORY_ID
ID_SCHEDULE: ANCS_CATAGORY_ID
ID_EMAIL: ANCS_CATAGORY_ID
NEWS: ANCS_CATAGORY_ID
HEALTH_AND_FITNESS: ANCS_CATAGORY_ID
BUSINESS_AND_FINANCE: ANCS_CATAGORY_ID
LOCATION: ANCS_CATAGORY_ID
ENTERTAINMENT: ANCS_CATAGORY_ID

class ancs_filter_message(_message.Message):
    __slots__ = ("catagory_id", "app_identifier")
    CATAGORY_ID_FIELD_NUMBER: _ClassVar[int]
    APP_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    catagory_id: ANCS_CATAGORY_ID
    app_identifier: str
    def __init__(self, catagory_id: _Optional[_Union[ANCS_CATAGORY_ID, str]] = ..., app_identifier: _Optional[str] = ...) -> None: ...

class ins_data_message(_message.Message):
    __slots__ = ("tel_num", "name", "content", "time", "uid", "count")
    TEL_NUM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    tel_num: bytes
    name: str
    content: str
    time: str
    uid: int
    count: int
    def __init__(self, tel_num: _Optional[bytes] = ..., name: _Optional[str] = ..., content: _Optional[str] = ..., time: _Optional[str] = ..., uid: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class ins_msg(_message.Message):
    __slots__ = ("service_type", "ins_service_type", "ins_operate_type", "ins_data_msg", "config", "ancs_filter_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INS_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INS_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INS_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ANCS_FILTER_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    ins_service_type: INS_SERVICE_TYPE
    ins_operate_type: INS_OPERATE_TYPE
    ins_data_msg: ins_data_message
    config: int
    ancs_filter_msg: _containers.RepeatedCompositeFieldContainer[ancs_filter_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., ins_service_type: _Optional[_Union[INS_SERVICE_TYPE, str]] = ..., ins_operate_type: _Optional[_Union[INS_OPERATE_TYPE, str]] = ..., ins_data_msg: _Optional[_Union[ins_data_message, _Mapping]] = ..., config: _Optional[int] = ..., ancs_filter_msg: _Optional[_Iterable[_Union[ancs_filter_message, _Mapping]]] = ...) -> None: ...

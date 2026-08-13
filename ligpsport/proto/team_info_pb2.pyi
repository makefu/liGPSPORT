from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TEAM_INFO_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_TEAM_INFO_OPERATE_TYPE_NONE: _ClassVar[TEAM_INFO_OPERATE_TYPE]
    enum_TEAM_INFO_OPERATE_TYPE_SET: _ClassVar[TEAM_INFO_OPERATE_TYPE]

class MEMBER_STATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_MEMBER_STATE_TYPE_INVALID: _ClassVar[MEMBER_STATE_TYPE]
    enum_MEMBER_STATE_TYPE_NORMAL: _ClassVar[MEMBER_STATE_TYPE]
    enum_MEMBER_STATE_TYPE_ABNORMAL: _ClassVar[MEMBER_STATE_TYPE]
    enum_MEMBER_STATE_TYPE_OFFLINE: _ClassVar[MEMBER_STATE_TYPE]
    enum_MEMBER_STATE_TYPE_JOIN: _ClassVar[MEMBER_STATE_TYPE]
    enum_MEMBER_STATE_TYPE_QUIT: _ClassVar[MEMBER_STATE_TYPE]
enum_TEAM_INFO_OPERATE_TYPE_NONE: TEAM_INFO_OPERATE_TYPE
enum_TEAM_INFO_OPERATE_TYPE_SET: TEAM_INFO_OPERATE_TYPE
enum_MEMBER_STATE_TYPE_INVALID: MEMBER_STATE_TYPE
enum_MEMBER_STATE_TYPE_NORMAL: MEMBER_STATE_TYPE
enum_MEMBER_STATE_TYPE_ABNORMAL: MEMBER_STATE_TYPE
enum_MEMBER_STATE_TYPE_OFFLINE: MEMBER_STATE_TYPE
enum_MEMBER_STATE_TYPE_JOIN: MEMBER_STATE_TYPE
enum_MEMBER_STATE_TYPE_QUIT: MEMBER_STATE_TYPE

class team_info_data_msg(_message.Message):
    __slots__ = ("latitude", "longitude", "status", "nick_name", "course")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NICK_NAME_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    status: int
    nick_name: str
    course: int
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., status: _Optional[int] = ..., nick_name: _Optional[str] = ..., course: _Optional[int] = ...) -> None: ...

class team_info_msg(_message.Message):
    __slots__ = ("service_type", "team_info_operate_type", "member_num", "team_info_data_message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_INFO_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_NUM_FIELD_NUMBER: _ClassVar[int]
    TEAM_INFO_DATA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    team_info_operate_type: TEAM_INFO_OPERATE_TYPE
    member_num: int
    team_info_data_message: _containers.RepeatedCompositeFieldContainer[team_info_data_msg]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., team_info_operate_type: _Optional[_Union[TEAM_INFO_OPERATE_TYPE, str]] = ..., member_num: _Optional[int] = ..., team_info_data_message: _Optional[_Iterable[_Union[team_info_data_msg, _Mapping]]] = ...) -> None: ...

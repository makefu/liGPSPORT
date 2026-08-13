from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class enum_operate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_OP_INVALID: _ClassVar[enum_operate]
    THEME_OP_LIST_GET: _ClassVar[enum_operate]
    THEME_OP_SET: _ClassVar[enum_operate]
    THEME_OP_USE: _ClassVar[enum_operate]

class enum_theme_status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_STATUS_UNUSED: _ClassVar[enum_theme_status]
    THEME_STATUS_USED: _ClassVar[enum_theme_status]

class enum_theme_func_key(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_FUNC_KEY_INVALID: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_RIDE: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_WORKOUT: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_NAVI: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_THEME: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_HISTORY: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_SET: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_ROADBOOK: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_INS: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_SAFETY_TRACK: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_PM: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_SENSOR: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_SYSTEM: _ClassVar[enum_theme_func_key]
    THEME_FUNC_KEY_WEATHER: _ClassVar[enum_theme_func_key]

class enum_theme_uitype(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_UITYPE_SIX_GRID: _ClassVar[enum_theme_uitype]
    THEME_UITYPE_ROLLER: _ClassVar[enum_theme_uitype]
    THEME_UITYPE_SPIN_ROLLER: _ClassVar[enum_theme_uitype]

class enum_theme_dark_mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THEME_DARK_MODE_DAY: _ClassVar[enum_theme_dark_mode]
    THEME_DARK_MODE_NIGHT: _ClassVar[enum_theme_dark_mode]
    THEME_DARK_MODE_AUTO: _ClassVar[enum_theme_dark_mode]
THEME_OP_INVALID: enum_operate
THEME_OP_LIST_GET: enum_operate
THEME_OP_SET: enum_operate
THEME_OP_USE: enum_operate
THEME_STATUS_UNUSED: enum_theme_status
THEME_STATUS_USED: enum_theme_status
THEME_FUNC_KEY_INVALID: enum_theme_func_key
THEME_FUNC_KEY_RIDE: enum_theme_func_key
THEME_FUNC_KEY_WORKOUT: enum_theme_func_key
THEME_FUNC_KEY_NAVI: enum_theme_func_key
THEME_FUNC_KEY_THEME: enum_theme_func_key
THEME_FUNC_KEY_HISTORY: enum_theme_func_key
THEME_FUNC_KEY_SET: enum_theme_func_key
THEME_FUNC_KEY_ROADBOOK: enum_theme_func_key
THEME_FUNC_KEY_INS: enum_theme_func_key
THEME_FUNC_KEY_SAFETY_TRACK: enum_theme_func_key
THEME_FUNC_KEY_PM: enum_theme_func_key
THEME_FUNC_KEY_SENSOR: enum_theme_func_key
THEME_FUNC_KEY_SYSTEM: enum_theme_func_key
THEME_FUNC_KEY_WEATHER: enum_theme_func_key
THEME_UITYPE_SIX_GRID: enum_theme_uitype
THEME_UITYPE_ROLLER: enum_theme_uitype
THEME_UITYPE_SPIN_ROLLER: enum_theme_uitype
THEME_DARK_MODE_DAY: enum_theme_dark_mode
THEME_DARK_MODE_NIGHT: enum_theme_dark_mode
THEME_DARK_MODE_AUTO: enum_theme_dark_mode

class theme_infor_msg(_message.Message):
    __slots__ = ("theme_id", "theme_index", "theme_status", "func_key", "theme_uitype", "theme_color")
    THEME_ID_FIELD_NUMBER: _ClassVar[int]
    THEME_INDEX_FIELD_NUMBER: _ClassVar[int]
    THEME_STATUS_FIELD_NUMBER: _ClassVar[int]
    FUNC_KEY_FIELD_NUMBER: _ClassVar[int]
    THEME_UITYPE_FIELD_NUMBER: _ClassVar[int]
    THEME_COLOR_FIELD_NUMBER: _ClassVar[int]
    theme_id: int
    theme_index: int
    theme_status: enum_theme_status
    func_key: _containers.RepeatedScalarFieldContainer[enum_theme_func_key]
    theme_uitype: enum_theme_uitype
    theme_color: int
    def __init__(self, theme_id: _Optional[int] = ..., theme_index: _Optional[int] = ..., theme_status: _Optional[_Union[enum_theme_status, str]] = ..., func_key: _Optional[_Iterable[_Union[enum_theme_func_key, str]]] = ..., theme_uitype: _Optional[_Union[enum_theme_uitype, str]] = ..., theme_color: _Optional[int] = ...) -> None: ...

class theme_message(_message.Message):
    __slots__ = ("service_type", "op_code", "theme_info", "dark_mode")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_CODE_FIELD_NUMBER: _ClassVar[int]
    THEME_INFO_FIELD_NUMBER: _ClassVar[int]
    DARK_MODE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    op_code: enum_operate
    theme_info: _containers.RepeatedCompositeFieldContainer[theme_infor_msg]
    dark_mode: enum_theme_dark_mode
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., op_code: _Optional[_Union[enum_operate, str]] = ..., theme_info: _Optional[_Iterable[_Union[theme_infor_msg, _Mapping]]] = ..., dark_mode: _Optional[_Union[enum_theme_dark_mode, str]] = ...) -> None: ...

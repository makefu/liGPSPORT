from . import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DEV_STATUS_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_DEV_STATUS_OPERATE_TYPE_NONE: _ClassVar[DEV_STATUS_OPERATE_TYPE]
    enum_DEV_STATUS_OPERATE_TYPE_GET: _ClassVar[DEV_STATUS_OPERATE_TYPE]
    enum_DEV_STATUS_OPERATE_TYPE_SEND: _ClassVar[DEV_STATUS_OPERATE_TYPE]

class DEV_CYCLING_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEV_CYCLING_STATUS_FREE: _ClassVar[DEV_CYCLING_STATUS]
    DEV_CYCLING_STATUS_DOING: _ClassVar[DEV_CYCLING_STATUS]
    DEV_CYCLING_STATUS_PAUSE: _ClassVar[DEV_CYCLING_STATUS]

class DEV_WIFI_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEV_WIFI_STATUS_IDLE: _ClassVar[DEV_WIFI_STATUS]
    DEV_WIFI_STATUS_MAP: _ClassVar[DEV_WIFI_STATUS]
    DEV_WIFI_STATUS_FIRMWARE: _ClassVar[DEV_WIFI_STATUS]
    DEV_WIFI_STATUS_UPLOAD: _ClassVar[DEV_WIFI_STATUS]
    DEV_WIFI_STATUS_SET: _ClassVar[DEV_WIFI_STATUS]

class DEV_NAVI_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEV_NAVI_STATUS_OFF: _ClassVar[DEV_NAVI_STATUS]
    DEV_NAVI_STATUS_ON: _ClassVar[DEV_NAVI_STATUS]
enum_DEV_STATUS_OPERATE_TYPE_NONE: DEV_STATUS_OPERATE_TYPE
enum_DEV_STATUS_OPERATE_TYPE_GET: DEV_STATUS_OPERATE_TYPE
enum_DEV_STATUS_OPERATE_TYPE_SEND: DEV_STATUS_OPERATE_TYPE
DEV_CYCLING_STATUS_FREE: DEV_CYCLING_STATUS
DEV_CYCLING_STATUS_DOING: DEV_CYCLING_STATUS
DEV_CYCLING_STATUS_PAUSE: DEV_CYCLING_STATUS
DEV_WIFI_STATUS_IDLE: DEV_WIFI_STATUS
DEV_WIFI_STATUS_MAP: DEV_WIFI_STATUS
DEV_WIFI_STATUS_FIRMWARE: DEV_WIFI_STATUS
DEV_WIFI_STATUS_UPLOAD: DEV_WIFI_STATUS
DEV_WIFI_STATUS_SET: DEV_WIFI_STATUS
DEV_NAVI_STATUS_OFF: DEV_NAVI_STATUS
DEV_NAVI_STATUS_ON: DEV_NAVI_STATUS

class dev_cycling_status_massage(_message.Message):
    __slots__ = ("dev_cycling_status", "cycling_start_time")
    DEV_CYCLING_STATUS_FIELD_NUMBER: _ClassVar[int]
    CYCLING_START_TIME_FIELD_NUMBER: _ClassVar[int]
    dev_cycling_status: DEV_CYCLING_STATUS
    cycling_start_time: int
    def __init__(self, dev_cycling_status: _Optional[_Union[DEV_CYCLING_STATUS, str]] = ..., cycling_start_time: _Optional[int] = ...) -> None: ...

class dev_gps_massage(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class rt_data_message(_message.Message):
    __slots__ = ("real_time_speed", "avg_speed", "riding_time", "riding_distance", "real_time_cad", "real_time_hrm", "avg_hrm", "real_time_power", "total_height", "avg_rise", "cur_height", "cur_slope", "max_speed", "max_hrm", "avg_cad", "max_cad", "avg_power", "max_power", "course")
    REAL_TIME_SPEED_FIELD_NUMBER: _ClassVar[int]
    AVG_SPEED_FIELD_NUMBER: _ClassVar[int]
    RIDING_TIME_FIELD_NUMBER: _ClassVar[int]
    RIDING_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_CAD_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_HRM_FIELD_NUMBER: _ClassVar[int]
    AVG_HRM_FIELD_NUMBER: _ClassVar[int]
    REAL_TIME_POWER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    AVG_RISE_FIELD_NUMBER: _ClassVar[int]
    CUR_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CUR_SLOPE_FIELD_NUMBER: _ClassVar[int]
    MAX_SPEED_FIELD_NUMBER: _ClassVar[int]
    MAX_HRM_FIELD_NUMBER: _ClassVar[int]
    AVG_CAD_FIELD_NUMBER: _ClassVar[int]
    MAX_CAD_FIELD_NUMBER: _ClassVar[int]
    AVG_POWER_FIELD_NUMBER: _ClassVar[int]
    MAX_POWER_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    real_time_speed: int
    avg_speed: int
    riding_time: int
    riding_distance: int
    real_time_cad: int
    real_time_hrm: int
    avg_hrm: int
    real_time_power: int
    total_height: int
    avg_rise: int
    cur_height: int
    cur_slope: int
    max_speed: int
    max_hrm: int
    avg_cad: int
    max_cad: int
    avg_power: int
    max_power: int
    course: int
    def __init__(self, real_time_speed: _Optional[int] = ..., avg_speed: _Optional[int] = ..., riding_time: _Optional[int] = ..., riding_distance: _Optional[int] = ..., real_time_cad: _Optional[int] = ..., real_time_hrm: _Optional[int] = ..., avg_hrm: _Optional[int] = ..., real_time_power: _Optional[int] = ..., total_height: _Optional[int] = ..., avg_rise: _Optional[int] = ..., cur_height: _Optional[int] = ..., cur_slope: _Optional[int] = ..., max_speed: _Optional[int] = ..., max_hrm: _Optional[int] = ..., avg_cad: _Optional[int] = ..., max_cad: _Optional[int] = ..., avg_power: _Optional[int] = ..., max_power: _Optional[int] = ..., course: _Optional[int] = ...) -> None: ...

class dev_status_msg(_message.Message):
    __slots__ = ("service_type", "op_type", "dev_cycling_status_msg", "dev_gps_msg", "rt_data_msg", "wifi_status", "navi_status")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OP_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEV_CYCLING_STATUS_MSG_FIELD_NUMBER: _ClassVar[int]
    DEV_GPS_MSG_FIELD_NUMBER: _ClassVar[int]
    RT_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    WIFI_STATUS_FIELD_NUMBER: _ClassVar[int]
    NAVI_STATUS_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    op_type: DEV_STATUS_OPERATE_TYPE
    dev_cycling_status_msg: dev_cycling_status_massage
    dev_gps_msg: dev_gps_massage
    rt_data_msg: rt_data_message
    wifi_status: DEV_WIFI_STATUS
    navi_status: DEV_NAVI_STATUS
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., op_type: _Optional[_Union[DEV_STATUS_OPERATE_TYPE, str]] = ..., dev_cycling_status_msg: _Optional[_Union[dev_cycling_status_massage, _Mapping]] = ..., dev_gps_msg: _Optional[_Union[dev_gps_massage, _Mapping]] = ..., rt_data_msg: _Optional[_Union[rt_data_message, _Mapping]] = ..., wifi_status: _Optional[_Union[DEV_WIFI_STATUS, str]] = ..., navi_status: _Optional[_Union[DEV_NAVI_STATUS, str]] = ...) -> None: ...

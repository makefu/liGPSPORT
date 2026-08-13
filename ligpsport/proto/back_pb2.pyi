from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BACK_SERVICE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_BACK_SERVICE_TYPE_NONE: _ClassVar[BACK_SERVICE_TYPE]
    enum_BACK_SERVICE_TYPE_MAIN: _ClassVar[BACK_SERVICE_TYPE]
    enum_BACK_SERVICE_TYPE_WEATHER: _ClassVar[BACK_SERVICE_TYPE]
    enum_BACK_SERVICE_TYPE_AIR_PRESSURE: _ClassVar[BACK_SERVICE_TYPE]
    enum_BACK_SERVICE_TYPE_ELEVATION: _ClassVar[BACK_SERVICE_TYPE]
    enum_BACK_SERVICE_TYPE_EPHEMERIS: _ClassVar[BACK_SERVICE_TYPE]

class BACK_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_BACK_OPERATE_TYPE_NONE: _ClassVar[BACK_OPERATE_TYPE]
    enum_BACK_OPERATE_TYPE_GET: _ClassVar[BACK_OPERATE_TYPE]
    enum_BACK_OPERATE_TYPE_SEND: _ClassVar[BACK_OPERATE_TYPE]

class GPS_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_GPS_TYPE_INVALID: _ClassVar[GPS_TYPE]
    enum_GPS_TYPE_GPS: _ClassVar[GPS_TYPE]
    enum_GPS_TYPE_BD: _ClassVar[GPS_TYPE]
    enum_GPS_TYPE_GLONASS: _ClassVar[GPS_TYPE]
    enum_GPS_TYPE_GALILEO: _ClassVar[GPS_TYPE]

class AGPS_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_AGPS_FILE_TYPE_INVALID: _ClassVar[AGPS_TYPE]
    enum_AGPS_FILE_TYPE_ONLINE: _ClassVar[AGPS_TYPE]
    enum_AGPS_FILE_TYPE_ANO_OFFLINE: _ClassVar[AGPS_TYPE]
    enum_AGPS_FILE_TYPE_ALM_OFFLINE: _ClassVar[AGPS_TYPE]
enum_BACK_SERVICE_TYPE_NONE: BACK_SERVICE_TYPE
enum_BACK_SERVICE_TYPE_MAIN: BACK_SERVICE_TYPE
enum_BACK_SERVICE_TYPE_WEATHER: BACK_SERVICE_TYPE
enum_BACK_SERVICE_TYPE_AIR_PRESSURE: BACK_SERVICE_TYPE
enum_BACK_SERVICE_TYPE_ELEVATION: BACK_SERVICE_TYPE
enum_BACK_SERVICE_TYPE_EPHEMERIS: BACK_SERVICE_TYPE
enum_BACK_OPERATE_TYPE_NONE: BACK_OPERATE_TYPE
enum_BACK_OPERATE_TYPE_GET: BACK_OPERATE_TYPE
enum_BACK_OPERATE_TYPE_SEND: BACK_OPERATE_TYPE
enum_GPS_TYPE_INVALID: GPS_TYPE
enum_GPS_TYPE_GPS: GPS_TYPE
enum_GPS_TYPE_BD: GPS_TYPE
enum_GPS_TYPE_GLONASS: GPS_TYPE
enum_GPS_TYPE_GALILEO: GPS_TYPE
enum_AGPS_FILE_TYPE_INVALID: AGPS_TYPE
enum_AGPS_FILE_TYPE_ONLINE: AGPS_TYPE
enum_AGPS_FILE_TYPE_ANO_OFFLINE: AGPS_TYPE
enum_AGPS_FILE_TYPE_ALM_OFFLINE: AGPS_TYPE

class weather_three_days_data_message(_message.Message):
    __slots__ = ("weather_index", "max_temp", "min_temp", "rain_prob", "date")
    WEATHER_INDEX_FIELD_NUMBER: _ClassVar[int]
    MAX_TEMP_FIELD_NUMBER: _ClassVar[int]
    MIN_TEMP_FIELD_NUMBER: _ClassVar[int]
    RAIN_PROB_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    weather_index: int
    max_temp: int
    min_temp: int
    rain_prob: int
    date: str
    def __init__(self, weather_index: _Optional[int] = ..., max_temp: _Optional[int] = ..., min_temp: _Optional[int] = ..., rain_prob: _Optional[int] = ..., date: _Optional[str] = ...) -> None: ...

class weather_current_data_message(_message.Message):
    __slots__ = ("cur_temperature", "cur_weather", "cur_day_max_temp", "cur_day_min_temp", "time", "wind_deg", "wind_spd")
    CUR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    CUR_WEATHER_FIELD_NUMBER: _ClassVar[int]
    CUR_DAY_MAX_TEMP_FIELD_NUMBER: _ClassVar[int]
    CUR_DAY_MIN_TEMP_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    WIND_DEG_FIELD_NUMBER: _ClassVar[int]
    WIND_SPD_FIELD_NUMBER: _ClassVar[int]
    cur_temperature: int
    cur_weather: int
    cur_day_max_temp: int
    cur_day_min_temp: int
    time: str
    wind_deg: str
    wind_spd: str
    def __init__(self, cur_temperature: _Optional[int] = ..., cur_weather: _Optional[int] = ..., cur_day_max_temp: _Optional[int] = ..., cur_day_min_temp: _Optional[int] = ..., time: _Optional[str] = ..., wind_deg: _Optional[str] = ..., wind_spd: _Optional[str] = ...) -> None: ...

class weather_three_hour_data_memsage(_message.Message):
    __slots__ = ("wather_index", "temp", "rain_prob", "time", "wind_deg", "wind_spd")
    WATHER_INDEX_FIELD_NUMBER: _ClassVar[int]
    TEMP_FIELD_NUMBER: _ClassVar[int]
    RAIN_PROB_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    WIND_DEG_FIELD_NUMBER: _ClassVar[int]
    WIND_SPD_FIELD_NUMBER: _ClassVar[int]
    wather_index: int
    temp: int
    rain_prob: int
    time: str
    wind_deg: str
    wind_spd: str
    def __init__(self, wather_index: _Optional[int] = ..., temp: _Optional[int] = ..., rain_prob: _Optional[int] = ..., time: _Optional[str] = ..., wind_deg: _Optional[str] = ..., wind_spd: _Optional[str] = ...) -> None: ...

class air_pressure_data_message(_message.Message):
    __slots__ = ("air_pressure",)
    AIR_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    air_pressure: int
    def __init__(self, air_pressure: _Optional[int] = ...) -> None: ...

class ephemeris_data_message(_message.Message):
    __slots__ = ("file_name", "contents", "gps_type", "agps_type", "time")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    GPS_TYPE_FIELD_NUMBER: _ClassVar[int]
    AGPS_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    contents: bytes
    gps_type: GPS_TYPE
    agps_type: AGPS_TYPE
    time: int
    def __init__(self, file_name: _Optional[str] = ..., contents: _Optional[bytes] = ..., gps_type: _Optional[_Union[GPS_TYPE, str]] = ..., agps_type: _Optional[_Union[AGPS_TYPE, str]] = ..., time: _Optional[int] = ...) -> None: ...

class back_msg(_message.Message):
    __slots__ = ("service_type", "back_service_type", "back_operate_type", "three_days_msg", "cur_msg", "three_hours_msg", "air_pressure_msg", "ephemeris_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BACK_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BACK_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    THREE_DAYS_MSG_FIELD_NUMBER: _ClassVar[int]
    CUR_MSG_FIELD_NUMBER: _ClassVar[int]
    THREE_HOURS_MSG_FIELD_NUMBER: _ClassVar[int]
    AIR_PRESSURE_MSG_FIELD_NUMBER: _ClassVar[int]
    EPHEMERIS_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    back_service_type: BACK_SERVICE_TYPE
    back_operate_type: BACK_OPERATE_TYPE
    three_days_msg: _containers.RepeatedCompositeFieldContainer[weather_three_days_data_message]
    cur_msg: weather_current_data_message
    three_hours_msg: _containers.RepeatedCompositeFieldContainer[weather_three_hour_data_memsage]
    air_pressure_msg: air_pressure_data_message
    ephemeris_data_msg: ephemeris_data_message
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., back_service_type: _Optional[_Union[BACK_SERVICE_TYPE, str]] = ..., back_operate_type: _Optional[_Union[BACK_OPERATE_TYPE, str]] = ..., three_days_msg: _Optional[_Iterable[_Union[weather_three_days_data_message, _Mapping]]] = ..., cur_msg: _Optional[_Union[weather_current_data_message, _Mapping]] = ..., three_hours_msg: _Optional[_Iterable[_Union[weather_three_hour_data_memsage, _Mapping]]] = ..., air_pressure_msg: _Optional[_Union[air_pressure_data_message, _Mapping]] = ..., ephemeris_data_msg: _Optional[_Union[ephemeris_data_message, _Mapping]] = ...) -> None: ...

from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FACTORY_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_FACTORY_OPERATE_TYPE_NONE: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SN_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SN_SEND: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SN_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SENSOR_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_MEMORY_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_BATTARY_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SIM_FIT_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_COORDINATE_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SUN_TIME_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_SUN_TIME_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_POWER_SAVE_TIME_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_RTC_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_RTC_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_FILTER_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_FILTER_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_CONTROL_CMD_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_CONTROL_CMD_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_GNSS_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_GNSS_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_DYNAMIC_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_DYNAMIC_GET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_GPS_CMD_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_CONTROL_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_CONTROL_DATA_SET: _ClassVar[FACTORY_OPERATE_TYPE]
    enum_FACTORY_OPERATE_TYPE_ALL_GET: _ClassVar[FACTORY_OPERATE_TYPE]

class FACTORY_SENSOR_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SENSOR_INVALID: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_GPS: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_RTC: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_AIR: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_TEM: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_ACC: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_ANT: _ClassVar[FACTORY_SENSOR_TYPE]
    enum_KEY: _ClassVar[FACTORY_SENSOR_TYPE]

class CONTROL_CMD_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_CMD_INVALID: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_ENTER_CHECK: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_LOCK: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_FORMAT: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_LFORMAT: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_PARA_RESET: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_FACTORY_RESET: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_TEMPERATURE_LOG: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_VOLTAGE_LOG: _ClassVar[CONTROL_CMD_TYPE]
    enum_CMD_ANT_LOG: _ClassVar[CONTROL_CMD_TYPE]

class FILTER_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_FILTER_INVALID: _ClassVar[FILTER_TYPE]
    enum_FILTER_SMART_SAVE: _ClassVar[FILTER_TYPE]
    enum_FILTER_SPD: _ClassVar[FILTER_TYPE]
    enum_FILTER_CAD: _ClassVar[FILTER_TYPE]
    enum_FILTER_HRM: _ClassVar[FILTER_TYPE]
    enum_FILTER_GPS_ICON: _ClassVar[FILTER_TYPE]
    enum_FLTER_ANT_ICON: _ClassVar[FILTER_TYPE]

class GPS_CONTROL_CMD_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_GPS_CMD_INVALID: _ClassVar[GPS_CONTROL_CMD_TYPE]
    enum_GPS_CMD_POWER: _ClassVar[GPS_CONTROL_CMD_TYPE]
    enum_GPS_CMD_COLD_START: _ClassVar[GPS_CONTROL_CMD_TYPE]
    enum_GPS_CMD_POWER_SAVE: _ClassVar[GPS_CONTROL_CMD_TYPE]
    enum_GPS_CMD_GNSS: _ClassVar[GPS_CONTROL_CMD_TYPE]

class GNSS_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_GNSS_INVALID: _ClassVar[GNSS_TYPE]
    enum_GNSS_GPS: _ClassVar[GNSS_TYPE]
    enum_GNSS_BD: _ClassVar[GNSS_TYPE]
    enum_GNSS__GLONASS: _ClassVar[GNSS_TYPE]
    enum_GNSS__QZSS: _ClassVar[GNSS_TYPE]
    enum_GNSS_SBAS: _ClassVar[GNSS_TYPE]
    enum_GNSS_GALILEO: _ClassVar[GNSS_TYPE]
    enum_GNSS_IMES: _ClassVar[GNSS_TYPE]

class GPS_DYNAMIC_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_GPS_DYNAMIC_INVALID: _ClassVar[GPS_DYNAMIC_TYPE]
    euum_PORTABLE: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_STATIONARY: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_PEDESTRIAN: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_AUTOMOTIVE: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_SEA: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_1G: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_2G: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_4G: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_WRIST: _ClassVar[GPS_DYNAMIC_TYPE]
    enum_BIKE: _ClassVar[GPS_DYNAMIC_TYPE]

class ANT_DEV_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enumInvalid_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumHrm_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumCbsc_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumBpwr_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumCad_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumSpd_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumShft_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumDi2_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumFe_dev_type: _ClassVar[ANT_DEV_TYPE]
    enumMax_dev_type: _ClassVar[ANT_DEV_TYPE]
enum_FACTORY_OPERATE_TYPE_NONE: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SN_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SN_SEND: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SN_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SENSOR_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_MEMORY_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_BATTARY_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SIM_FIT_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_COORDINATE_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SUN_TIME_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_SUN_TIME_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_POWER_SAVE_TIME_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_RTC_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_RTC_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_FILTER_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_FILTER_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_CONTROL_CMD_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_CONTROL_CMD_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_GNSS_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_GNSS_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_DYNAMIC_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_DYNAMIC_GET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_GPS_CMD_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_CONTROL_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_CONTROL_DATA_SET: FACTORY_OPERATE_TYPE
enum_FACTORY_OPERATE_TYPE_ALL_GET: FACTORY_OPERATE_TYPE
enum_SENSOR_INVALID: FACTORY_SENSOR_TYPE
enum_GPS: FACTORY_SENSOR_TYPE
enum_RTC: FACTORY_SENSOR_TYPE
enum_AIR: FACTORY_SENSOR_TYPE
enum_TEM: FACTORY_SENSOR_TYPE
enum_ACC: FACTORY_SENSOR_TYPE
enum_ANT: FACTORY_SENSOR_TYPE
enum_KEY: FACTORY_SENSOR_TYPE
enum_CMD_INVALID: CONTROL_CMD_TYPE
enum_CMD_ENTER_CHECK: CONTROL_CMD_TYPE
enum_CMD_LOCK: CONTROL_CMD_TYPE
enum_CMD_FORMAT: CONTROL_CMD_TYPE
enum_CMD_LFORMAT: CONTROL_CMD_TYPE
enum_CMD_PARA_RESET: CONTROL_CMD_TYPE
enum_CMD_FACTORY_RESET: CONTROL_CMD_TYPE
enum_CMD_TEMPERATURE_LOG: CONTROL_CMD_TYPE
enum_CMD_VOLTAGE_LOG: CONTROL_CMD_TYPE
enum_CMD_ANT_LOG: CONTROL_CMD_TYPE
enum_FILTER_INVALID: FILTER_TYPE
enum_FILTER_SMART_SAVE: FILTER_TYPE
enum_FILTER_SPD: FILTER_TYPE
enum_FILTER_CAD: FILTER_TYPE
enum_FILTER_HRM: FILTER_TYPE
enum_FILTER_GPS_ICON: FILTER_TYPE
enum_FLTER_ANT_ICON: FILTER_TYPE
enum_GPS_CMD_INVALID: GPS_CONTROL_CMD_TYPE
enum_GPS_CMD_POWER: GPS_CONTROL_CMD_TYPE
enum_GPS_CMD_COLD_START: GPS_CONTROL_CMD_TYPE
enum_GPS_CMD_POWER_SAVE: GPS_CONTROL_CMD_TYPE
enum_GPS_CMD_GNSS: GPS_CONTROL_CMD_TYPE
enum_GNSS_INVALID: GNSS_TYPE
enum_GNSS_GPS: GNSS_TYPE
enum_GNSS_BD: GNSS_TYPE
enum_GNSS__GLONASS: GNSS_TYPE
enum_GNSS__QZSS: GNSS_TYPE
enum_GNSS_SBAS: GNSS_TYPE
enum_GNSS_GALILEO: GNSS_TYPE
enum_GNSS_IMES: GNSS_TYPE
enum_GPS_DYNAMIC_INVALID: GPS_DYNAMIC_TYPE
euum_PORTABLE: GPS_DYNAMIC_TYPE
enum_STATIONARY: GPS_DYNAMIC_TYPE
enum_PEDESTRIAN: GPS_DYNAMIC_TYPE
enum_AUTOMOTIVE: GPS_DYNAMIC_TYPE
enum_SEA: GPS_DYNAMIC_TYPE
enum_1G: GPS_DYNAMIC_TYPE
enum_2G: GPS_DYNAMIC_TYPE
enum_4G: GPS_DYNAMIC_TYPE
enum_WRIST: GPS_DYNAMIC_TYPE
enum_BIKE: GPS_DYNAMIC_TYPE
enumInvalid_dev_type: ANT_DEV_TYPE
enumHrm_dev_type: ANT_DEV_TYPE
enumCbsc_dev_type: ANT_DEV_TYPE
enumBpwr_dev_type: ANT_DEV_TYPE
enumCad_dev_type: ANT_DEV_TYPE
enumSpd_dev_type: ANT_DEV_TYPE
enumShft_dev_type: ANT_DEV_TYPE
enumDi2_dev_type: ANT_DEV_TYPE
enumFe_dev_type: ANT_DEV_TYPE
enumMax_dev_type: ANT_DEV_TYPE

class factory_sn_message(_message.Message):
    __slots__ = ("sn",)
    SN_FIELD_NUMBER: _ClassVar[int]
    sn: str
    def __init__(self, sn: _Optional[str] = ...) -> None: ...

class factory_sensor_message(_message.Message):
    __slots__ = ("sensor_type", "data", "status")
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    sensor_type: FACTORY_SENSOR_TYPE
    data: int
    status: int
    def __init__(self, sensor_type: _Optional[_Union[FACTORY_SENSOR_TYPE, str]] = ..., data: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class memory_message(_message.Message):
    __slots__ = ("total", "remain")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    REMAIN_FIELD_NUMBER: _ClassVar[int]
    total: int
    remain: int
    def __init__(self, total: _Optional[int] = ..., remain: _Optional[int] = ...) -> None: ...

class battary_message(_message.Message):
    __slots__ = ("voltage", "power_percent")
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    POWER_PERCENT_FIELD_NUMBER: _ClassVar[int]
    voltage: int
    power_percent: int
    def __init__(self, voltage: _Optional[int] = ..., power_percent: _Optional[int] = ...) -> None: ...

class sim_fit_message(_message.Message):
    __slots__ = ("num", "size")
    NUM_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    num: int
    size: int
    def __init__(self, num: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class control_message(_message.Message):
    __slots__ = ("cmd_type", "status")
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    cmd_type: CONTROL_CMD_TYPE
    status: int
    def __init__(self, cmd_type: _Optional[_Union[CONTROL_CMD_TYPE, str]] = ..., status: _Optional[int] = ...) -> None: ...

class gps_coordinate_message(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...

class sun_time_message(_message.Message):
    __slots__ = ("sunrise_time", "sunset_time")
    SUNRISE_TIME_FIELD_NUMBER: _ClassVar[int]
    SUNSET_TIME_FIELD_NUMBER: _ClassVar[int]
    sunrise_time: int
    sunset_time: int
    def __init__(self, sunrise_time: _Optional[int] = ..., sunset_time: _Optional[int] = ...) -> None: ...

class power_save_message(_message.Message):
    __slots__ = ("time",)
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: int
    def __init__(self, time: _Optional[int] = ...) -> None: ...

class rtc_message(_message.Message):
    __slots__ = ("time",)
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: int
    def __init__(self, time: _Optional[int] = ...) -> None: ...

class filter_message(_message.Message):
    __slots__ = ("filter_type", "status")
    FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    filter_type: FILTER_TYPE
    status: int
    def __init__(self, filter_type: _Optional[_Union[FILTER_TYPE, str]] = ..., status: _Optional[int] = ...) -> None: ...

class gps_control_cmd_message(_message.Message):
    __slots__ = ("gps_cmd_type", "status")
    GPS_CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    gps_cmd_type: GPS_CONTROL_CMD_TYPE
    status: int
    def __init__(self, gps_cmd_type: _Optional[_Union[GPS_CONTROL_CMD_TYPE, str]] = ..., status: _Optional[int] = ...) -> None: ...

class gps_gnss_message(_message.Message):
    __slots__ = ("gnss_gnss_cmd",)
    GNSS_GNSS_CMD_FIELD_NUMBER: _ClassVar[int]
    gnss_gnss_cmd: int
    def __init__(self, gnss_gnss_cmd: _Optional[int] = ...) -> None: ...

class gps_dynamic_message(_message.Message):
    __slots__ = ("gps_dynamic_type",)
    GPS_DYNAMIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    gps_dynamic_type: GPS_DYNAMIC_TYPE
    def __init__(self, gps_dynamic_type: _Optional[_Union[GPS_DYNAMIC_TYPE, str]] = ...) -> None: ...

class gps_cmd_message(_message.Message):
    __slots__ = ("gps_cmd",)
    GPS_CMD_FIELD_NUMBER: _ClassVar[int]
    gps_cmd: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, gps_cmd: _Optional[_Iterable[bytes]] = ...) -> None: ...

class data_set_message(_message.Message):
    __slots__ = ("data_type", "value")
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    data_type: int
    value: int
    def __init__(self, data_type: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...

class gps_snr_massage(_message.Message):
    __slots__ = ("gnss_type", "data")
    GNSS_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    gnss_type: GNSS_TYPE
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, gnss_type: _Optional[_Union[GNSS_TYPE, str]] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...

class ant_message(_message.Message):
    __slots__ = ("dev_type", "dev_connect_status", "data")
    DEV_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEV_CONNECT_STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    dev_type: ANT_DEV_TYPE
    dev_connect_status: int
    data: int
    def __init__(self, dev_type: _Optional[_Union[ANT_DEV_TYPE, str]] = ..., dev_connect_status: _Optional[int] = ..., data: _Optional[int] = ...) -> None: ...

class factory_msg(_message.Message):
    __slots__ = ("service_type", "factory_operate_type", "factory_sn_msg", "factory_sensor_msg", "memory_msg", "battary_msg", "sim_fit_msg", "control_msg", "gps_coordinate_msg", "sun_time_msg", "power_save_msg", "rtc_msg", "filter_msg", "gps_control_cmd_msg", "gps_gnss_msg", "gps_dynamic_msg", "gps_cmd_msg", "data_set_msg", "gps_snr_msg", "ant_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FACTORY_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FACTORY_SN_MSG_FIELD_NUMBER: _ClassVar[int]
    FACTORY_SENSOR_MSG_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MSG_FIELD_NUMBER: _ClassVar[int]
    BATTARY_MSG_FIELD_NUMBER: _ClassVar[int]
    SIM_FIT_MSG_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_COORDINATE_MSG_FIELD_NUMBER: _ClassVar[int]
    SUN_TIME_MSG_FIELD_NUMBER: _ClassVar[int]
    POWER_SAVE_MSG_FIELD_NUMBER: _ClassVar[int]
    RTC_MSG_FIELD_NUMBER: _ClassVar[int]
    FILTER_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_CONTROL_CMD_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_GNSS_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_DYNAMIC_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_CMD_MSG_FIELD_NUMBER: _ClassVar[int]
    DATA_SET_MSG_FIELD_NUMBER: _ClassVar[int]
    GPS_SNR_MSG_FIELD_NUMBER: _ClassVar[int]
    ANT_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    factory_operate_type: FACTORY_OPERATE_TYPE
    factory_sn_msg: _containers.RepeatedCompositeFieldContainer[factory_sn_message]
    factory_sensor_msg: _containers.RepeatedCompositeFieldContainer[factory_sensor_message]
    memory_msg: memory_message
    battary_msg: battary_message
    sim_fit_msg: sim_fit_message
    control_msg: control_message
    gps_coordinate_msg: gps_coordinate_message
    sun_time_msg: sun_time_message
    power_save_msg: power_save_message
    rtc_msg: rtc_message
    filter_msg: filter_message
    gps_control_cmd_msg: gps_control_cmd_message
    gps_gnss_msg: gps_gnss_message
    gps_dynamic_msg: gps_dynamic_message
    gps_cmd_msg: gps_cmd_message
    data_set_msg: _containers.RepeatedCompositeFieldContainer[data_set_message]
    gps_snr_msg: _containers.RepeatedCompositeFieldContainer[gps_snr_massage]
    ant_msg: _containers.RepeatedCompositeFieldContainer[ant_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., factory_operate_type: _Optional[_Union[FACTORY_OPERATE_TYPE, str]] = ..., factory_sn_msg: _Optional[_Iterable[_Union[factory_sn_message, _Mapping]]] = ..., factory_sensor_msg: _Optional[_Iterable[_Union[factory_sensor_message, _Mapping]]] = ..., memory_msg: _Optional[_Union[memory_message, _Mapping]] = ..., battary_msg: _Optional[_Union[battary_message, _Mapping]] = ..., sim_fit_msg: _Optional[_Union[sim_fit_message, _Mapping]] = ..., control_msg: _Optional[_Union[control_message, _Mapping]] = ..., gps_coordinate_msg: _Optional[_Union[gps_coordinate_message, _Mapping]] = ..., sun_time_msg: _Optional[_Union[sun_time_message, _Mapping]] = ..., power_save_msg: _Optional[_Union[power_save_message, _Mapping]] = ..., rtc_msg: _Optional[_Union[rtc_message, _Mapping]] = ..., filter_msg: _Optional[_Union[filter_message, _Mapping]] = ..., gps_control_cmd_msg: _Optional[_Union[gps_control_cmd_message, _Mapping]] = ..., gps_gnss_msg: _Optional[_Union[gps_gnss_message, _Mapping]] = ..., gps_dynamic_msg: _Optional[_Union[gps_dynamic_message, _Mapping]] = ..., gps_cmd_msg: _Optional[_Union[gps_cmd_message, _Mapping]] = ..., data_set_msg: _Optional[_Iterable[_Union[data_set_message, _Mapping]]] = ..., gps_snr_msg: _Optional[_Iterable[_Union[gps_snr_massage, _Mapping]]] = ..., ant_msg: _Optional[_Iterable[_Union[ant_message, _Mapping]]] = ...) -> None: ...

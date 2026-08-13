from . import peripheral_common_pb2 as _peripheral_common_pb2
from . import peripheral_info_pb2 as _peripheral_info_pb2
from . import peripheral_config_pb2 as _peripheral_config_pb2
from . import peripheral_hr_pb2 as _peripheral_hr_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_FACTORY_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FAS_UNSPECIFIED: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_SN: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_DEVICE_INFO: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_DEVICE_OPERATE: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_DEVICE_CONFIG: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_BSP_MEMORY: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_BSP_RTC: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_BSP_BATTARY: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_BSP_TEMPERATURE: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_BSP_ACC: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_ALL_FACTORY: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_LED_TEST_BUTTON: _ClassVar[PERIPHERAL_FACTORY_SERVICE]
    FAS_MOTOR_TEST_BUTTON: _ClassVar[PERIPHERAL_FACTORY_SERVICE]

class PERIPHERAL_FACTORY_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FAO_UNSPECIFIED: _ClassVar[PERIPHERAL_FACTORY_OPERATE]
FAS_UNSPECIFIED: PERIPHERAL_FACTORY_SERVICE
FAS_SN: PERIPHERAL_FACTORY_SERVICE
FAS_DEVICE_INFO: PERIPHERAL_FACTORY_SERVICE
FAS_DEVICE_OPERATE: PERIPHERAL_FACTORY_SERVICE
FAS_DEVICE_CONFIG: PERIPHERAL_FACTORY_SERVICE
FAS_BSP_MEMORY: PERIPHERAL_FACTORY_SERVICE
FAS_BSP_RTC: PERIPHERAL_FACTORY_SERVICE
FAS_BSP_BATTARY: PERIPHERAL_FACTORY_SERVICE
FAS_BSP_TEMPERATURE: PERIPHERAL_FACTORY_SERVICE
FAS_BSP_ACC: PERIPHERAL_FACTORY_SERVICE
FAS_ALL_FACTORY: PERIPHERAL_FACTORY_SERVICE
FAS_LED_TEST_BUTTON: PERIPHERAL_FACTORY_SERVICE
FAS_MOTOR_TEST_BUTTON: PERIPHERAL_FACTORY_SERVICE
FAO_UNSPECIFIED: PERIPHERAL_FACTORY_OPERATE

class peripheral_factory_data_sn(_message.Message):
    __slots__ = ("sn",)
    SN_FIELD_NUMBER: _ClassVar[int]
    sn: str
    def __init__(self, sn: _Optional[str] = ...) -> None: ...

class peripheral_factory_data_device_info(_message.Message):
    __slots__ = ("model", "name", "version", "id")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    model: _peripheral_info_pb2.PERIPHERAL_INFO_MODEL_TYPE
    name: _peripheral_info_pb2.peripheral_info_data_name
    version: _peripheral_info_pb2.peripheral_info_data_version
    id: _peripheral_info_pb2.peripheral_info_data_id
    def __init__(self, model: _Optional[_Union[_peripheral_info_pb2.PERIPHERAL_INFO_MODEL_TYPE, str]] = ..., name: _Optional[_Union[_peripheral_info_pb2.peripheral_info_data_name, _Mapping]] = ..., version: _Optional[_Union[_peripheral_info_pb2.peripheral_info_data_version, _Mapping]] = ..., id: _Optional[_Union[_peripheral_info_pb2.peripheral_info_data_id, _Mapping]] = ...) -> None: ...

class peripheral_factory_data_device_operate(_message.Message):
    __slots__ = ("hr_sport_mode",)
    HR_SPORT_MODE_FIELD_NUMBER: _ClassVar[int]
    hr_sport_mode: _peripheral_hr_pb2.PERIPHERAL_HR_SPORT_MODE_TYPE
    def __init__(self, hr_sport_mode: _Optional[_Union[_peripheral_hr_pb2.PERIPHERAL_HR_SPORT_MODE_TYPE, str]] = ...) -> None: ...

class peripheral_factory_data_device_config(_message.Message):
    __slots__ = ("shutdown", "sleep")
    SHUTDOWN_FIELD_NUMBER: _ClassVar[int]
    SLEEP_FIELD_NUMBER: _ClassVar[int]
    shutdown: _peripheral_config_pb2.peripheral_config_data_shutdown
    sleep: _peripheral_config_pb2.peripheral_config_data_sleep
    def __init__(self, shutdown: _Optional[_Union[_peripheral_config_pb2.peripheral_config_data_shutdown, _Mapping]] = ..., sleep: _Optional[_Union[_peripheral_config_pb2.peripheral_config_data_sleep, _Mapping]] = ...) -> None: ...

class peripheral_factory_data_bsp_memory(_message.Message):
    __slots__ = ("remain_internal_flash", "total_internal_flash", "remain_iexternal_flash", "total_external_flash")
    REMAIN_INTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    REMAIN_IEXTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EXTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    remain_internal_flash: int
    total_internal_flash: int
    remain_iexternal_flash: int
    total_external_flash: int
    def __init__(self, remain_internal_flash: _Optional[int] = ..., total_internal_flash: _Optional[int] = ..., remain_iexternal_flash: _Optional[int] = ..., total_external_flash: _Optional[int] = ...) -> None: ...

class peripheral_factory_data_bsp_rtc(_message.Message):
    __slots__ = ("zone", "rtc", "sunrise", "sunset")
    ZONE_FIELD_NUMBER: _ClassVar[int]
    RTC_FIELD_NUMBER: _ClassVar[int]
    SUNRISE_FIELD_NUMBER: _ClassVar[int]
    SUNSET_FIELD_NUMBER: _ClassVar[int]
    zone: int
    rtc: int
    sunrise: int
    sunset: int
    def __init__(self, zone: _Optional[int] = ..., rtc: _Optional[int] = ..., sunrise: _Optional[int] = ..., sunset: _Optional[int] = ...) -> None: ...

class peripheral_factory_data_bsp_battery(_message.Message):
    __slots__ = ("vol_cur", "percent")
    VOL_CUR_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    vol_cur: int
    percent: int
    def __init__(self, vol_cur: _Optional[int] = ..., percent: _Optional[int] = ...) -> None: ...

class peripheral_factory_data_bsp_temperature(_message.Message):
    __slots__ = ("temp_cur", "temp_max")
    TEMP_CUR_FIELD_NUMBER: _ClassVar[int]
    TEMP_MAX_FIELD_NUMBER: _ClassVar[int]
    temp_cur: int
    temp_max: int
    def __init__(self, temp_cur: _Optional[int] = ..., temp_max: _Optional[int] = ...) -> None: ...

class peripheral_factory_data_bsp_acc(_message.Message):
    __slots__ = ("x_axis_val", "y_axis_val", "z_axis_val")
    X_AXIS_VAL_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_VAL_FIELD_NUMBER: _ClassVar[int]
    Z_AXIS_VAL_FIELD_NUMBER: _ClassVar[int]
    x_axis_val: int
    y_axis_val: int
    z_axis_val: int
    def __init__(self, x_axis_val: _Optional[int] = ..., y_axis_val: _Optional[int] = ..., z_axis_val: _Optional[int] = ...) -> None: ...

class peripheral_factory_message(_message.Message):
    __slots__ = ("sn", "device_info", "device_operate", "device_config", "bsp_memory", "bsp_rtc", "bsp_battery", "bsp_temperature", "bsp_acc")
    SN_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    DEVICE_OPERATE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BSP_MEMORY_FIELD_NUMBER: _ClassVar[int]
    BSP_RTC_FIELD_NUMBER: _ClassVar[int]
    BSP_BATTERY_FIELD_NUMBER: _ClassVar[int]
    BSP_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    BSP_ACC_FIELD_NUMBER: _ClassVar[int]
    sn: peripheral_factory_data_sn
    device_info: peripheral_factory_data_device_info
    device_operate: peripheral_factory_data_device_operate
    device_config: peripheral_factory_data_device_config
    bsp_memory: peripheral_factory_data_bsp_memory
    bsp_rtc: peripheral_factory_data_bsp_rtc
    bsp_battery: peripheral_factory_data_bsp_battery
    bsp_temperature: peripheral_factory_data_bsp_temperature
    bsp_acc: peripheral_factory_data_bsp_acc
    def __init__(self, sn: _Optional[_Union[peripheral_factory_data_sn, _Mapping]] = ..., device_info: _Optional[_Union[peripheral_factory_data_device_info, _Mapping]] = ..., device_operate: _Optional[_Union[peripheral_factory_data_device_operate, _Mapping]] = ..., device_config: _Optional[_Union[peripheral_factory_data_device_config, _Mapping]] = ..., bsp_memory: _Optional[_Union[peripheral_factory_data_bsp_memory, _Mapping]] = ..., bsp_rtc: _Optional[_Union[peripheral_factory_data_bsp_rtc, _Mapping]] = ..., bsp_battery: _Optional[_Union[peripheral_factory_data_bsp_battery, _Mapping]] = ..., bsp_temperature: _Optional[_Union[peripheral_factory_data_bsp_temperature, _Mapping]] = ..., bsp_acc: _Optional[_Union[peripheral_factory_data_bsp_acc, _Mapping]] = ...) -> None: ...

class peripheral_factory_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_FACTORY_SERVICE
    sub_operate_type: PERIPHERAL_FACTORY_OPERATE
    message: peripheral_factory_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_FACTORY_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_FACTORY_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_factory_message, _Mapping]] = ...) -> None: ...

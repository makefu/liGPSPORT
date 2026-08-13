from . import peripheral_common_pb2 as _peripheral_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_INFO_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIS_UNSPECIFIED: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_MODEL: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_NAME: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_VERSION: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_ID: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_POWER: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_TEMPERATURE: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_MEMORY: _ClassVar[PERIPHERAL_INFO_SERVICE]
    PIS_ALL_INFO: _ClassVar[PERIPHERAL_INFO_SERVICE]

class PERIPHERAL_INFO_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIO_UNSPECIFIED: _ClassVar[PERIPHERAL_INFO_OPERATE]

class PERIPHERAL_INFO_MODEL_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIM_UNSPECIFIED: _ClassVar[PERIPHERAL_INFO_MODEL_TYPE]
    PIM_HR70: _ClassVar[PERIPHERAL_INFO_MODEL_TYPE]
PIS_UNSPECIFIED: PERIPHERAL_INFO_SERVICE
PIS_MODEL: PERIPHERAL_INFO_SERVICE
PIS_NAME: PERIPHERAL_INFO_SERVICE
PIS_VERSION: PERIPHERAL_INFO_SERVICE
PIS_ID: PERIPHERAL_INFO_SERVICE
PIS_POWER: PERIPHERAL_INFO_SERVICE
PIS_TEMPERATURE: PERIPHERAL_INFO_SERVICE
PIS_MEMORY: PERIPHERAL_INFO_SERVICE
PIS_ALL_INFO: PERIPHERAL_INFO_SERVICE
PIO_UNSPECIFIED: PERIPHERAL_INFO_OPERATE
PIM_UNSPECIFIED: PERIPHERAL_INFO_MODEL_TYPE
PIM_HR70: PERIPHERAL_INFO_MODEL_TYPE

class peripheral_info_data_name(_message.Message):
    __slots__ = ("device_name", "ble_name", "manufacturer_name")
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    BLE_NAME_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_NAME_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    ble_name: str
    manufacturer_name: str
    def __init__(self, device_name: _Optional[str] = ..., ble_name: _Optional[str] = ..., manufacturer_name: _Optional[str] = ...) -> None: ...

class peripheral_info_data_version(_message.Message):
    __slots__ = ("mcu_version", "app_version", "boot_version", "hard_version", "check_version")
    MCU_VERSION_FIELD_NUMBER: _ClassVar[int]
    APP_VERSION_FIELD_NUMBER: _ClassVar[int]
    BOOT_VERSION_FIELD_NUMBER: _ClassVar[int]
    HARD_VERSION_FIELD_NUMBER: _ClassVar[int]
    CHECK_VERSION_FIELD_NUMBER: _ClassVar[int]
    mcu_version: int
    app_version: int
    boot_version: int
    hard_version: int
    check_version: int
    def __init__(self, mcu_version: _Optional[int] = ..., app_version: _Optional[int] = ..., boot_version: _Optional[int] = ..., hard_version: _Optional[int] = ..., check_version: _Optional[int] = ...) -> None: ...

class peripheral_info_data_id(_message.Message):
    __slots__ = ("device_id", "manufacturer_id")
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_ID_FIELD_NUMBER: _ClassVar[int]
    device_id: int
    manufacturer_id: int
    def __init__(self, device_id: _Optional[int] = ..., manufacturer_id: _Optional[int] = ...) -> None: ...

class peripheral_info_data_power(_message.Message):
    __slots__ = ("vol_cur", "percent")
    VOL_CUR_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    vol_cur: int
    percent: int
    def __init__(self, vol_cur: _Optional[int] = ..., percent: _Optional[int] = ...) -> None: ...

class peripheral_info_data_temperature(_message.Message):
    __slots__ = ("temp_cur", "temp_max")
    TEMP_CUR_FIELD_NUMBER: _ClassVar[int]
    TEMP_MAX_FIELD_NUMBER: _ClassVar[int]
    temp_cur: int
    temp_max: int
    def __init__(self, temp_cur: _Optional[int] = ..., temp_max: _Optional[int] = ...) -> None: ...

class peripheral_info_data_memory(_message.Message):
    __slots__ = ("remain_internal_flash", "total_internal_flash", "remain_iexternal_flash", "total_external_flash", "remain_internal_ram", "total_internal_ram", "remain_external_ram", "total_external_ram")
    REMAIN_INTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    REMAIN_IEXTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EXTERNAL_FLASH_FIELD_NUMBER: _ClassVar[int]
    REMAIN_INTERNAL_RAM_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INTERNAL_RAM_FIELD_NUMBER: _ClassVar[int]
    REMAIN_EXTERNAL_RAM_FIELD_NUMBER: _ClassVar[int]
    TOTAL_EXTERNAL_RAM_FIELD_NUMBER: _ClassVar[int]
    remain_internal_flash: int
    total_internal_flash: int
    remain_iexternal_flash: int
    total_external_flash: int
    remain_internal_ram: int
    total_internal_ram: int
    remain_external_ram: int
    total_external_ram: int
    def __init__(self, remain_internal_flash: _Optional[int] = ..., total_internal_flash: _Optional[int] = ..., remain_iexternal_flash: _Optional[int] = ..., total_external_flash: _Optional[int] = ..., remain_internal_ram: _Optional[int] = ..., total_internal_ram: _Optional[int] = ..., remain_external_ram: _Optional[int] = ..., total_external_ram: _Optional[int] = ...) -> None: ...

class peripheral_info_message(_message.Message):
    __slots__ = ("model", "name", "version", "id", "power", "temperature", "memory")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    model: PERIPHERAL_INFO_MODEL_TYPE
    name: peripheral_info_data_name
    version: peripheral_info_data_version
    id: peripheral_info_data_id
    power: peripheral_info_data_power
    temperature: peripheral_info_data_temperature
    memory: peripheral_info_data_memory
    def __init__(self, model: _Optional[_Union[PERIPHERAL_INFO_MODEL_TYPE, str]] = ..., name: _Optional[_Union[peripheral_info_data_name, _Mapping]] = ..., version: _Optional[_Union[peripheral_info_data_version, _Mapping]] = ..., id: _Optional[_Union[peripheral_info_data_id, _Mapping]] = ..., power: _Optional[_Union[peripheral_info_data_power, _Mapping]] = ..., temperature: _Optional[_Union[peripheral_info_data_temperature, _Mapping]] = ..., memory: _Optional[_Union[peripheral_info_data_memory, _Mapping]] = ...) -> None: ...

class peripheral_info_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_INFO_SERVICE
    sub_operate_type: PERIPHERAL_INFO_OPERATE
    message: peripheral_info_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_INFO_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_INFO_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_info_message, _Mapping]] = ...) -> None: ...

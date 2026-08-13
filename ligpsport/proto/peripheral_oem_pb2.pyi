from . import peripheral_common_pb2 as _peripheral_common_pb2
from . import peripheral_info_pb2 as _peripheral_info_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_OEM_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POS_UNSPECIFIED: _ClassVar[PERIPHERAL_OEM_SERVICE]
    POS_BLE_INFO: _ClassVar[PERIPHERAL_OEM_SERVICE]
    POS_DEVICE_INFO: _ClassVar[PERIPHERAL_OEM_SERVICE]
    POS_MANUFACTURER_INFO: _ClassVar[PERIPHERAL_OEM_SERVICE]
    POS_ALL_OEM: _ClassVar[PERIPHERAL_OEM_SERVICE]

class PERIPHERAL_OEM_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POO_UNSPECIFIED: _ClassVar[PERIPHERAL_OEM_OPERATE]
POS_UNSPECIFIED: PERIPHERAL_OEM_SERVICE
POS_BLE_INFO: PERIPHERAL_OEM_SERVICE
POS_DEVICE_INFO: PERIPHERAL_OEM_SERVICE
POS_MANUFACTURER_INFO: PERIPHERAL_OEM_SERVICE
POS_ALL_OEM: PERIPHERAL_OEM_SERVICE
POO_UNSPECIFIED: PERIPHERAL_OEM_OPERATE

class peripheral_oem_data_ble(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class peripheral_oem_data_device(_message.Message):
    __slots__ = ("model", "name", "id")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    model: _peripheral_info_pb2.PERIPHERAL_INFO_MODEL_TYPE
    name: str
    id: int
    def __init__(self, model: _Optional[_Union[_peripheral_info_pb2.PERIPHERAL_INFO_MODEL_TYPE, str]] = ..., name: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class peripheral_oem_data_manufacturer(_message.Message):
    __slots__ = ("name", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: int
    def __init__(self, name: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...

class peripheral_oem_message(_message.Message):
    __slots__ = ("ble_info", "device_info", "manufacturer_info")
    BLE_INFO_FIELD_NUMBER: _ClassVar[int]
    DEVICE_INFO_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_INFO_FIELD_NUMBER: _ClassVar[int]
    ble_info: peripheral_oem_data_ble
    device_info: peripheral_oem_data_device
    manufacturer_info: peripheral_oem_data_manufacturer
    def __init__(self, ble_info: _Optional[_Union[peripheral_oem_data_ble, _Mapping]] = ..., device_info: _Optional[_Union[peripheral_oem_data_device, _Mapping]] = ..., manufacturer_info: _Optional[_Union[peripheral_oem_data_manufacturer, _Mapping]] = ...) -> None: ...

class peripheral_oem_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_OEM_SERVICE
    sub_operate_type: PERIPHERAL_OEM_OPERATE
    message: peripheral_oem_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_OEM_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_OEM_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_oem_message, _Mapping]] = ...) -> None: ...

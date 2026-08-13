from . import peripheral_common_pb2 as _peripheral_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PERIPHERAL_FIRMWARE_SERVICE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PFS_UNSPECIFIED: _ClassVar[PERIPHERAL_FIRMWARE_SERVICE]
    PFS_ENTER_DFU: _ClassVar[PERIPHERAL_FIRMWARE_SERVICE]
    PFS_MCU_UPDATE: _ClassVar[PERIPHERAL_FIRMWARE_SERVICE]

class PERIPHERAL_FIRMWARE_OPERATE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PFO_UNSPECIFIED: _ClassVar[PERIPHERAL_FIRMWARE_OPERATE]
    PFO_MCU_UPDATE_START: _ClassVar[PERIPHERAL_FIRMWARE_OPERATE]
    PFO_MCU_UPDATE_PROCESS: _ClassVar[PERIPHERAL_FIRMWARE_OPERATE]
    PFO_MCU_UPDATE_END: _ClassVar[PERIPHERAL_FIRMWARE_OPERATE]
    PFO_MCU_UPDATE_ERROR: _ClassVar[PERIPHERAL_FIRMWARE_OPERATE]
PFS_UNSPECIFIED: PERIPHERAL_FIRMWARE_SERVICE
PFS_ENTER_DFU: PERIPHERAL_FIRMWARE_SERVICE
PFS_MCU_UPDATE: PERIPHERAL_FIRMWARE_SERVICE
PFO_UNSPECIFIED: PERIPHERAL_FIRMWARE_OPERATE
PFO_MCU_UPDATE_START: PERIPHERAL_FIRMWARE_OPERATE
PFO_MCU_UPDATE_PROCESS: PERIPHERAL_FIRMWARE_OPERATE
PFO_MCU_UPDATE_END: PERIPHERAL_FIRMWARE_OPERATE
PFO_MCU_UPDATE_ERROR: PERIPHERAL_FIRMWARE_OPERATE

class peripheral_firmware_message(_message.Message):
    __slots__ = ("bin_packet_size", "bin_packet_data")
    BIN_PACKET_SIZE_FIELD_NUMBER: _ClassVar[int]
    BIN_PACKET_DATA_FIELD_NUMBER: _ClassVar[int]
    bin_packet_size: int
    bin_packet_data: bytes
    def __init__(self, bin_packet_size: _Optional[int] = ..., bin_packet_data: _Optional[bytes] = ...) -> None: ...

class peripheral_firmware_format(_message.Message):
    __slots__ = ("service_type", "operate_type", "sub_service_type", "sub_operate_type", "message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUB_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE
    operate_type: _peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE
    sub_service_type: PERIPHERAL_FIRMWARE_SERVICE
    sub_operate_type: PERIPHERAL_FIRMWARE_OPERATE
    message: peripheral_firmware_message
    def __init__(self, service_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_SERVICE_TYPE, str]] = ..., operate_type: _Optional[_Union[_peripheral_common_pb2.PERIPHERAL_OPERATE_TYPE, str]] = ..., sub_service_type: _Optional[_Union[PERIPHERAL_FIRMWARE_SERVICE, str]] = ..., sub_operate_type: _Optional[_Union[PERIPHERAL_FIRMWARE_OPERATE, str]] = ..., message: _Optional[_Union[peripheral_firmware_message, _Mapping]] = ...) -> None: ...

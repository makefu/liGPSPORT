from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SENSOR_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SENSOR_OPERATE_TYPE_NONE: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_GET: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_SET: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_DEL: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_CONNECT: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_SEND: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_EXIT: _ClassVar[SENSOR_OPERATE_TYPE]
    enum_SENSOR_OPERATE_TYPE_POW_CALIB: _ClassVar[SENSOR_OPERATE_TYPE]

class SENSOR_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SENSOR_TYPE_INVALID: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_HRM: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_CBSC: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_PEDAL_BPWR: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_OTHER_BPWR: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_CAD: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_SPD: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_SHFT: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_DI2: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_FEC: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_LEV: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_RD: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_RADAR: _ClassVar[SENSOR_TYPE]
    enum_SENSOR_TYPE_LIGHT: _ClassVar[SENSOR_TYPE]

class SENSOR_RADIO_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SENSOR_RADIO_TYPE_INVALID: _ClassVar[SENSOR_RADIO_TYPE]
    enum_SENSOR_RADIO_TYPE_BLE: _ClassVar[SENSOR_RADIO_TYPE]
    enum_SENSOR_RADIO_TYPE_ANT: _ClassVar[SENSOR_RADIO_TYPE]

class SENSOR_STATUS_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SENSOR_STATUS_TYPE_SAVED: _ClassVar[SENSOR_STATUS_TYPE]
    enum_SENSOR_STATUS_TYPE_CONNECTED: _ClassVar[SENSOR_STATUS_TYPE]
    enum_SENSOR_STATUS_TYPE_NO_SAVED: _ClassVar[SENSOR_STATUS_TYPE]

class DI2_CHN_NUM(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_DI2_CHN_NUM_0: _ClassVar[DI2_CHN_NUM]
    enum_DI2_CHN_NUM_1: _ClassVar[DI2_CHN_NUM]
    enum_DI2_CHN_NUM_2: _ClassVar[DI2_CHN_NUM]
    enum_DI2_CHN_NUM_3: _ClassVar[DI2_CHN_NUM]

class DI2_BUTTON_OP_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_DI2_BUTTON_OP_TYPE_LONG: _ClassVar[DI2_BUTTON_OP_TYPE]
    enum_DI2_BUTTON_OP_TYPE_SINGLE: _ClassVar[DI2_BUTTON_OP_TYPE]
    enum_DI2_BUTTON_OP_TYPE_DOUBLE: _ClassVar[DI2_BUTTON_OP_TYPE]

class DI2_FUNC_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_DI2_FUNC_INVALID: _ClassVar[DI2_FUNC_TYPE]
    enum_DI2_FUNC_PAGE_UP: _ClassVar[DI2_FUNC_TYPE]
    enum_DI2_FUNC_PAGE_DOWN: _ClassVar[DI2_FUNC_TYPE]
    enum_DI2_FUNC_LAP: _ClassVar[DI2_FUNC_TYPE]
    enum_DI2_FUNC_START_PAUSE: _ClassVar[DI2_FUNC_TYPE]
    enum_DI2_FUNC_UNDEFINE: _ClassVar[DI2_FUNC_TYPE]
enum_SENSOR_OPERATE_TYPE_NONE: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_GET: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_SET: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_DEL: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_CONNECT: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_SEND: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_EXIT: SENSOR_OPERATE_TYPE
enum_SENSOR_OPERATE_TYPE_POW_CALIB: SENSOR_OPERATE_TYPE
enum_SENSOR_TYPE_INVALID: SENSOR_TYPE
enum_SENSOR_TYPE_HRM: SENSOR_TYPE
enum_SENSOR_TYPE_CBSC: SENSOR_TYPE
enum_SENSOR_TYPE_PEDAL_BPWR: SENSOR_TYPE
enum_SENSOR_TYPE_OTHER_BPWR: SENSOR_TYPE
enum_SENSOR_TYPE_CAD: SENSOR_TYPE
enum_SENSOR_TYPE_SPD: SENSOR_TYPE
enum_SENSOR_TYPE_SHFT: SENSOR_TYPE
enum_SENSOR_TYPE_DI2: SENSOR_TYPE
enum_SENSOR_TYPE_FEC: SENSOR_TYPE
enum_SENSOR_TYPE_LEV: SENSOR_TYPE
enum_SENSOR_TYPE_RD: SENSOR_TYPE
enum_SENSOR_TYPE_RADAR: SENSOR_TYPE
enum_SENSOR_TYPE_LIGHT: SENSOR_TYPE
enum_SENSOR_RADIO_TYPE_INVALID: SENSOR_RADIO_TYPE
enum_SENSOR_RADIO_TYPE_BLE: SENSOR_RADIO_TYPE
enum_SENSOR_RADIO_TYPE_ANT: SENSOR_RADIO_TYPE
enum_SENSOR_STATUS_TYPE_SAVED: SENSOR_STATUS_TYPE
enum_SENSOR_STATUS_TYPE_CONNECTED: SENSOR_STATUS_TYPE
enum_SENSOR_STATUS_TYPE_NO_SAVED: SENSOR_STATUS_TYPE
enum_DI2_CHN_NUM_0: DI2_CHN_NUM
enum_DI2_CHN_NUM_1: DI2_CHN_NUM
enum_DI2_CHN_NUM_2: DI2_CHN_NUM
enum_DI2_CHN_NUM_3: DI2_CHN_NUM
enum_DI2_BUTTON_OP_TYPE_LONG: DI2_BUTTON_OP_TYPE
enum_DI2_BUTTON_OP_TYPE_SINGLE: DI2_BUTTON_OP_TYPE
enum_DI2_BUTTON_OP_TYPE_DOUBLE: DI2_BUTTON_OP_TYPE
enum_DI2_FUNC_INVALID: DI2_FUNC_TYPE
enum_DI2_FUNC_PAGE_UP: DI2_FUNC_TYPE
enum_DI2_FUNC_PAGE_DOWN: DI2_FUNC_TYPE
enum_DI2_FUNC_LAP: DI2_FUNC_TYPE
enum_DI2_FUNC_START_PAUSE: DI2_FUNC_TYPE
enum_DI2_FUNC_UNDEFINE: DI2_FUNC_TYPE

class radar_sensor_set_message(_message.Message):
    __slots__ = ("alert_bar_side", "alert_sound_open")
    ALERT_BAR_SIDE_FIELD_NUMBER: _ClassVar[int]
    ALERT_SOUND_OPEN_FIELD_NUMBER: _ClassVar[int]
    alert_bar_side: int
    alert_sound_open: int
    def __init__(self, alert_bar_side: _Optional[int] = ..., alert_sound_open: _Optional[int] = ...) -> None: ...

class di2_sensor_set_message(_message.Message):
    __slots__ = ("num", "button_op_type", "func")
    NUM_FIELD_NUMBER: _ClassVar[int]
    BUTTON_OP_TYPE_FIELD_NUMBER: _ClassVar[int]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    num: DI2_CHN_NUM
    button_op_type: DI2_BUTTON_OP_TYPE
    func: DI2_FUNC_TYPE
    def __init__(self, num: _Optional[_Union[DI2_CHN_NUM, str]] = ..., button_op_type: _Optional[_Union[DI2_BUTTON_OP_TYPE, str]] = ..., func: _Optional[_Union[DI2_FUNC_TYPE, str]] = ...) -> None: ...

class sensor_data_message(_message.Message):
    __slots__ = ("sensor_type", "sensor_radio_type", "sensor_status_type", "sensor_key", "sensor_ble_name", "sensor_rssi", "sensor_pwr", "wheel_size", "crank_length", "sensor_forbidden", "auto_wheel_size", "radar_sensor_set_msg", "di2_sensor_set_msg")
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_RADIO_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_STATUS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_KEY_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BLE_NAME_FIELD_NUMBER: _ClassVar[int]
    SENSOR_RSSI_FIELD_NUMBER: _ClassVar[int]
    SENSOR_PWR_FIELD_NUMBER: _ClassVar[int]
    WHEEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CRANK_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FORBIDDEN_FIELD_NUMBER: _ClassVar[int]
    AUTO_WHEEL_SIZE_FIELD_NUMBER: _ClassVar[int]
    RADAR_SENSOR_SET_MSG_FIELD_NUMBER: _ClassVar[int]
    DI2_SENSOR_SET_MSG_FIELD_NUMBER: _ClassVar[int]
    sensor_type: SENSOR_TYPE
    sensor_radio_type: SENSOR_RADIO_TYPE
    sensor_status_type: SENSOR_STATUS_TYPE
    sensor_key: str
    sensor_ble_name: str
    sensor_rssi: int
    sensor_pwr: int
    wheel_size: int
    crank_length: int
    sensor_forbidden: int
    auto_wheel_size: int
    radar_sensor_set_msg: radar_sensor_set_message
    di2_sensor_set_msg: _containers.RepeatedCompositeFieldContainer[di2_sensor_set_message]
    def __init__(self, sensor_type: _Optional[_Union[SENSOR_TYPE, str]] = ..., sensor_radio_type: _Optional[_Union[SENSOR_RADIO_TYPE, str]] = ..., sensor_status_type: _Optional[_Union[SENSOR_STATUS_TYPE, str]] = ..., sensor_key: _Optional[str] = ..., sensor_ble_name: _Optional[str] = ..., sensor_rssi: _Optional[int] = ..., sensor_pwr: _Optional[int] = ..., wheel_size: _Optional[int] = ..., crank_length: _Optional[int] = ..., sensor_forbidden: _Optional[int] = ..., auto_wheel_size: _Optional[int] = ..., radar_sensor_set_msg: _Optional[_Union[radar_sensor_set_message, _Mapping]] = ..., di2_sensor_set_msg: _Optional[_Iterable[_Union[di2_sensor_set_message, _Mapping]]] = ...) -> None: ...

class sensor_message(_message.Message):
    __slots__ = ("service_type", "sensor_operate_type", "sensor_data_msg")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_DATA_MSG_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    sensor_operate_type: SENSOR_OPERATE_TYPE
    sensor_data_msg: _containers.RepeatedCompositeFieldContainer[sensor_data_message]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., sensor_operate_type: _Optional[_Union[SENSOR_OPERATE_TYPE, str]] = ..., sensor_data_msg: _Optional[_Iterable[_Union[sensor_data_message, _Mapping]]] = ...) -> None: ...

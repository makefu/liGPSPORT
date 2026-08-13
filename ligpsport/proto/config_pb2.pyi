from . import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CONFIG_SERVICE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_CONFIG_SERVICE_TYPE_NONE: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_USER: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_PAGE: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_BIKE: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_UNIT: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_LANG: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_KEY: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_WHEEL: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_GPS: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_SOUND: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_POWER: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_DIS_COLOR: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_BK: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_ALARM: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_LAP: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_AUTO: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_MODE: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_ALTITUDE: _ClassVar[CONFIG_SERVICE_TYPE]
    enum_CONFIG_SERVICE_TYPE_DATA: _ClassVar[CONFIG_SERVICE_TYPE]

class CONFIG_OPERATE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_CONFIG_OPERATE_TYPE_NONE: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_SET: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_GET: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_SEND: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_ADD: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_DEL: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_GET_MODULE_INFO: _ClassVar[CONFIG_OPERATE_TYPE]
    enum_CONFIG_OPERATE_TYPE_CTRL: _ClassVar[CONFIG_OPERATE_TYPE]

class SOUND_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SOUND_TYPE_INVALID: _ClassVar[SOUND_TYPE]
    enum_SOUND_RECORD_START: _ClassVar[SOUND_TYPE]
    enum_SOUND_RECORD_PAUSE: _ClassVar[SOUND_TYPE]
    enum_SOUND_RECORD_SAVE: _ClassVar[SOUND_TYPE]
    enum_SOUND_LAP: _ClassVar[SOUND_TYPE]
    enum_SOUND_ALART: _ClassVar[SOUND_TYPE]
    enum_SOUND_KEY: _ClassVar[SOUND_TYPE]
    enum_SOUND_USB: _ClassVar[SOUND_TYPE]
    enum_SOUND_GPS: _ClassVar[SOUND_TYPE]
    enum_SOUND_SENSOR: _ClassVar[SOUND_TYPE]
    enum_SOUND_CALL: _ClassVar[SOUND_TYPE]
    enum_SOUND_SOCIAL: _ClassVar[SOUND_TYPE]
    enum_SOUND_BURGLAR_ALARM: _ClassVar[SOUND_TYPE]
    enum_SOUND_DEV_FIND: _ClassVar[SOUND_TYPE]

class SOUND_SCENE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_SOUND_SCENE_TYPE_INVALID: _ClassVar[SOUND_SCENE_TYPE]
    enum_ALL_SCENE: _ClassVar[SOUND_SCENE_TYPE]
    enum_RECORDING_SCENE: _ClassVar[SOUND_SCENE_TYPE]

class KEY_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_KEY_TYPE_INVALID: _ClassVar[KEY_TYPE]
    enum_KEY1: _ClassVar[KEY_TYPE]
    enum_KEY2: _ClassVar[KEY_TYPE]
    enum_KEY3: _ClassVar[KEY_TYPE]
    enum_KEY4: _ClassVar[KEY_TYPE]
    enum_KEY5: _ClassVar[KEY_TYPE]
    enum_KEY6: _ClassVar[KEY_TYPE]

class KEY_FUNCTION_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_KEY_FUNCTION_TYPE_INVALID: _ClassVar[KEY_FUNCTION_TYPE]
    enum_RECORD_STATUS_MANUAL_PAUSE: _ClassVar[KEY_FUNCTION_TYPE]
    enum_RECORD_STATUS_MANUAL_LAP: _ClassVar[KEY_FUNCTION_TYPE]

class AUTO_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_AUTO_TYPE_INVALID: _ClassVar[AUTO_TYPE]
    enum_PAUSE: _ClassVar[AUTO_TYPE]
    enum_RECORD_START: _ClassVar[AUTO_TYPE]
    enum_POWER_OFF: _ClassVar[AUTO_TYPE]
    enum_SLEEP: _ClassVar[AUTO_TYPE]
    enum_HOME_PAGE_BACK: _ClassVar[AUTO_TYPE]
    enum_SMART_SAVE: _ClassVar[AUTO_TYPE]
    enum_POWER_SAVE: _ClassVar[AUTO_TYPE]
    enum_PAGE_AUTO: _ClassVar[AUTO_TYPE]
    enum_MOTION_CHECK: _ClassVar[AUTO_TYPE]

class POWER_SAVE_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POWER_SAVE_STATUS_OFF: _ClassVar[POWER_SAVE_STATUS]
    POWER_SAVE_STATUS_ON: _ClassVar[POWER_SAVE_STATUS]
    POWER_SAVE_STATUS_SMART: _ClassVar[POWER_SAVE_STATUS]

class PAGE_AUTO_STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAGE_AUTO_STATUS_OFF: _ClassVar[PAGE_AUTO_STATUS]
    PAGE_AUTO_STATUS_ON: _ClassVar[PAGE_AUTO_STATUS]
    PAGE_AUTO_STATUS_FAST: _ClassVar[PAGE_AUTO_STATUS]
    PAGE_AUTO_STATUS_SLOW: _ClassVar[PAGE_AUTO_STATUS]
    PAGE_AUTO_STATUS_MAIN: _ClassVar[PAGE_AUTO_STATUS]

class ALARM_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALARM_TYPE_INVALID: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_RIDE_TIME: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_RIDE_DISTANCE: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_HRM: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_CAD: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_PWR: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_CALORIE: _ClassVar[ALARM_TYPE]
    ALARM_TYPE_SPEED: _ClassVar[ALARM_TYPE]

class LAP_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LAP_TYPE_INVALID: _ClassVar[LAP_TYPE]
    LAP_TYPE_LOCATION: _ClassVar[LAP_TYPE]
    LAP_TYPE_TIME: _ClassVar[LAP_TYPE]
    LAP_TYPE_DISTANCE: _ClassVar[LAP_TYPE]

class UNIT_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_UNIT_TYPE_INVALID: _ClassVar[UNIT_TYPE]
    enum_UNIT_TYPE_METRIC: _ClassVar[UNIT_TYPE]
    enum_UNIT_TYPE_INCH: _ClassVar[UNIT_TYPE]

class UNIT_ITEM(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_UNIT_ITEM_INVALID: _ClassVar[UNIT_ITEM]
    enum_UNIT_ITEM_DISTANCE: _ClassVar[UNIT_ITEM]
    enum_UNIT_ITEM_ELEVATION: _ClassVar[UNIT_ITEM]
    enum_UNIT_ITEM_WEIGHT: _ClassVar[UNIT_ITEM]
    enum_UNIT_ITEM_TEMPERATURE: _ClassVar[UNIT_ITEM]

class PAGE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_PAGE_TYPE_INVALID: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_DATA: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_ELEVATION: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_MAP: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_AREA: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_TRAINING_COURSE: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_TRAINING_FEC: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_COMPASS: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_LAP: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_ROADBOOK: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_CLIMB: _ClassVar[PAGE_TYPE]
    enum_PAGE_TYPE_AIPARTNER: _ClassVar[PAGE_TYPE]

class LCD_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INVALID: _ClassVar[LCD_TYPE]
    PIXEL_LCD: _ClassVar[LCD_TYPE]
    SECTION_LCD: _ClassVar[LCD_TYPE]

class LANGUAGE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_LANGUAGE_TYPE_INVALID: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_ENGLISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_SPANISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_FRENCH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_GERMAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_JAPANESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_ITALIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_PORTUGUESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_KOREAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_CHINESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_TAIWANESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_POLISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_CROATIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_CZECH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_DANISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_DUTCH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_FINNISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_GREEK: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_HUNGARIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_NORWEGIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_SLOVAKIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_SLOVENIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_SWEDISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_RUSSIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_TURKISH: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_LATVIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_UKRAINIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_ARABIC: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_FARSI: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_BULGARIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_ROMANIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_THAI: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_HEBREW: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_BRAZILIAN_PORTUGUESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_INDONESIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_MALAYSIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_VIETNAMESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_BURMESE: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_MONGOLIAN: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_ALL: _ClassVar[LANGUAGE_TYPE]
    enum_LANGUAGE_TYPE_CUSTOM: _ClassVar[LANGUAGE_TYPE]

class DATA_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    enum_DATA_TYPE_INVALID: _ClassVar[DATA_TYPE]
    enum_DATA_TYPE_PWR_WITH_ZERO: _ClassVar[DATA_TYPE]
    enum_DATA_TYPE_CAD_WITH_ZERO: _ClassVar[DATA_TYPE]
enum_CONFIG_SERVICE_TYPE_NONE: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_USER: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_PAGE: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_BIKE: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_UNIT: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_LANG: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_KEY: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_WHEEL: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_GPS: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_SOUND: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_POWER: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_DIS_COLOR: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_BK: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_ALARM: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_LAP: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_AUTO: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_MODE: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_ALTITUDE: CONFIG_SERVICE_TYPE
enum_CONFIG_SERVICE_TYPE_DATA: CONFIG_SERVICE_TYPE
enum_CONFIG_OPERATE_TYPE_NONE: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_SET: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_GET: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_SEND: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_ADD: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_DEL: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_GET_MODULE_INFO: CONFIG_OPERATE_TYPE
enum_CONFIG_OPERATE_TYPE_CTRL: CONFIG_OPERATE_TYPE
enum_SOUND_TYPE_INVALID: SOUND_TYPE
enum_SOUND_RECORD_START: SOUND_TYPE
enum_SOUND_RECORD_PAUSE: SOUND_TYPE
enum_SOUND_RECORD_SAVE: SOUND_TYPE
enum_SOUND_LAP: SOUND_TYPE
enum_SOUND_ALART: SOUND_TYPE
enum_SOUND_KEY: SOUND_TYPE
enum_SOUND_USB: SOUND_TYPE
enum_SOUND_GPS: SOUND_TYPE
enum_SOUND_SENSOR: SOUND_TYPE
enum_SOUND_CALL: SOUND_TYPE
enum_SOUND_SOCIAL: SOUND_TYPE
enum_SOUND_BURGLAR_ALARM: SOUND_TYPE
enum_SOUND_DEV_FIND: SOUND_TYPE
enum_SOUND_SCENE_TYPE_INVALID: SOUND_SCENE_TYPE
enum_ALL_SCENE: SOUND_SCENE_TYPE
enum_RECORDING_SCENE: SOUND_SCENE_TYPE
enum_KEY_TYPE_INVALID: KEY_TYPE
enum_KEY1: KEY_TYPE
enum_KEY2: KEY_TYPE
enum_KEY3: KEY_TYPE
enum_KEY4: KEY_TYPE
enum_KEY5: KEY_TYPE
enum_KEY6: KEY_TYPE
enum_KEY_FUNCTION_TYPE_INVALID: KEY_FUNCTION_TYPE
enum_RECORD_STATUS_MANUAL_PAUSE: KEY_FUNCTION_TYPE
enum_RECORD_STATUS_MANUAL_LAP: KEY_FUNCTION_TYPE
enum_AUTO_TYPE_INVALID: AUTO_TYPE
enum_PAUSE: AUTO_TYPE
enum_RECORD_START: AUTO_TYPE
enum_POWER_OFF: AUTO_TYPE
enum_SLEEP: AUTO_TYPE
enum_HOME_PAGE_BACK: AUTO_TYPE
enum_SMART_SAVE: AUTO_TYPE
enum_POWER_SAVE: AUTO_TYPE
enum_PAGE_AUTO: AUTO_TYPE
enum_MOTION_CHECK: AUTO_TYPE
POWER_SAVE_STATUS_OFF: POWER_SAVE_STATUS
POWER_SAVE_STATUS_ON: POWER_SAVE_STATUS
POWER_SAVE_STATUS_SMART: POWER_SAVE_STATUS
PAGE_AUTO_STATUS_OFF: PAGE_AUTO_STATUS
PAGE_AUTO_STATUS_ON: PAGE_AUTO_STATUS
PAGE_AUTO_STATUS_FAST: PAGE_AUTO_STATUS
PAGE_AUTO_STATUS_SLOW: PAGE_AUTO_STATUS
PAGE_AUTO_STATUS_MAIN: PAGE_AUTO_STATUS
ALARM_TYPE_INVALID: ALARM_TYPE
ALARM_TYPE_RIDE_TIME: ALARM_TYPE
ALARM_TYPE_RIDE_DISTANCE: ALARM_TYPE
ALARM_TYPE_HRM: ALARM_TYPE
ALARM_TYPE_CAD: ALARM_TYPE
ALARM_TYPE_PWR: ALARM_TYPE
ALARM_TYPE_CALORIE: ALARM_TYPE
ALARM_TYPE_SPEED: ALARM_TYPE
LAP_TYPE_INVALID: LAP_TYPE
LAP_TYPE_LOCATION: LAP_TYPE
LAP_TYPE_TIME: LAP_TYPE
LAP_TYPE_DISTANCE: LAP_TYPE
enum_UNIT_TYPE_INVALID: UNIT_TYPE
enum_UNIT_TYPE_METRIC: UNIT_TYPE
enum_UNIT_TYPE_INCH: UNIT_TYPE
enum_UNIT_ITEM_INVALID: UNIT_ITEM
enum_UNIT_ITEM_DISTANCE: UNIT_ITEM
enum_UNIT_ITEM_ELEVATION: UNIT_ITEM
enum_UNIT_ITEM_WEIGHT: UNIT_ITEM
enum_UNIT_ITEM_TEMPERATURE: UNIT_ITEM
enum_PAGE_TYPE_INVALID: PAGE_TYPE
enum_PAGE_TYPE_DATA: PAGE_TYPE
enum_PAGE_TYPE_ELEVATION: PAGE_TYPE
enum_PAGE_TYPE_MAP: PAGE_TYPE
enum_PAGE_TYPE_AREA: PAGE_TYPE
enum_PAGE_TYPE_TRAINING_COURSE: PAGE_TYPE
enum_PAGE_TYPE_TRAINING_FEC: PAGE_TYPE
enum_PAGE_TYPE_COMPASS: PAGE_TYPE
enum_PAGE_TYPE_LAP: PAGE_TYPE
enum_PAGE_TYPE_ROADBOOK: PAGE_TYPE
enum_PAGE_TYPE_CLIMB: PAGE_TYPE
enum_PAGE_TYPE_AIPARTNER: PAGE_TYPE
INVALID: LCD_TYPE
PIXEL_LCD: LCD_TYPE
SECTION_LCD: LCD_TYPE
enum_LANGUAGE_TYPE_INVALID: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_ENGLISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_SPANISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_FRENCH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_GERMAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_JAPANESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_ITALIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_PORTUGUESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_KOREAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_CHINESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_TAIWANESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_POLISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_CROATIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_CZECH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_DANISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_DUTCH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_FINNISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_GREEK: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_HUNGARIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_NORWEGIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_SLOVAKIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_SLOVENIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_SWEDISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_RUSSIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_TURKISH: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_LATVIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_UKRAINIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_ARABIC: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_FARSI: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_BULGARIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_ROMANIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_THAI: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_HEBREW: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_BRAZILIAN_PORTUGUESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_INDONESIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_MALAYSIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_VIETNAMESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_BURMESE: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_MONGOLIAN: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_ALL: LANGUAGE_TYPE
enum_LANGUAGE_TYPE_CUSTOM: LANGUAGE_TYPE
enum_DATA_TYPE_INVALID: DATA_TYPE
enum_DATA_TYPE_PWR_WITH_ZERO: DATA_TYPE
enum_DATA_TYPE_CAD_WITH_ZERO: DATA_TYPE

class sound_set_msg(_message.Message):
    __slots__ = ("sound_type", "sound_scene", "status")
    SOUND_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOUND_SCENE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    sound_type: int
    sound_scene: SOUND_SCENE_TYPE
    status: int
    def __init__(self, sound_type: _Optional[int] = ..., sound_scene: _Optional[_Union[SOUND_SCENE_TYPE, str]] = ..., status: _Optional[int] = ...) -> None: ...

class key_set_msg(_message.Message):
    __slots__ = ("key_type", "key_function_type")
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEY_FUNCTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    key_type: KEY_TYPE
    key_function_type: KEY_FUNCTION_TYPE
    def __init__(self, key_type: _Optional[_Union[KEY_TYPE, str]] = ..., key_function_type: _Optional[_Union[KEY_FUNCTION_TYPE, str]] = ...) -> None: ...

class auto_set_msg(_message.Message):
    __slots__ = ("auto_type", "status", "param1")
    AUTO_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PARAM1_FIELD_NUMBER: _ClassVar[int]
    auto_type: AUTO_TYPE
    status: int
    param1: int
    def __init__(self, auto_type: _Optional[_Union[AUTO_TYPE, str]] = ..., status: _Optional[int] = ..., param1: _Optional[int] = ...) -> None: ...

class alarm_params_set_msg(_message.Message):
    __slots__ = ("alarm_type", "value_max", "value_min", "status")
    ALARM_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_MAX_FIELD_NUMBER: _ClassVar[int]
    VALUE_MIN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    alarm_type: ALARM_TYPE
    value_max: int
    value_min: int
    status: int
    def __init__(self, alarm_type: _Optional[_Union[ALARM_TYPE, str]] = ..., value_max: _Optional[int] = ..., value_min: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class alarm_msg(_message.Message):
    __slots__ = ("set_msg", "alarm_interval_time")
    SET_MSG_FIELD_NUMBER: _ClassVar[int]
    ALARM_INTERVAL_TIME_FIELD_NUMBER: _ClassVar[int]
    set_msg: _containers.RepeatedCompositeFieldContainer[alarm_params_set_msg]
    alarm_interval_time: int
    def __init__(self, set_msg: _Optional[_Iterable[_Union[alarm_params_set_msg, _Mapping]]] = ..., alarm_interval_time: _Optional[int] = ...) -> None: ...

class lap_msg(_message.Message):
    __slots__ = ("lap_type", "value", "status")
    LAP_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    lap_type: LAP_TYPE
    value: int
    status: int
    def __init__(self, lap_type: _Optional[_Union[LAP_TYPE, str]] = ..., value: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class unit_msg(_message.Message):
    __slots__ = ("unit_item", "unit_type")
    UNIT_ITEM_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    unit_item: UNIT_ITEM
    unit_type: UNIT_TYPE
    def __init__(self, unit_item: _Optional[_Union[UNIT_ITEM, str]] = ..., unit_type: _Optional[_Union[UNIT_TYPE, str]] = ...) -> None: ...

class section_data_msg(_message.Message):
    __slots__ = ("hrm", "cad", "spd", "FTP", "power")
    HRM_FIELD_NUMBER: _ClassVar[int]
    CAD_FIELD_NUMBER: _ClassVar[int]
    SPD_FIELD_NUMBER: _ClassVar[int]
    FTP_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    hrm: _containers.RepeatedScalarFieldContainer[int]
    cad: _containers.RepeatedScalarFieldContainer[int]
    spd: _containers.RepeatedScalarFieldContainer[int]
    FTP: int
    power: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, hrm: _Optional[_Iterable[int]] = ..., cad: _Optional[_Iterable[int]] = ..., spd: _Optional[_Iterable[int]] = ..., FTP: _Optional[int] = ..., power: _Optional[_Iterable[int]] = ...) -> None: ...

class user_data_msg(_message.Message):
    __slots__ = ("sex", "weight", "age", "height", "time_zone", "member_id", "update_status", "section_data")
    SEX_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_STATUS_FIELD_NUMBER: _ClassVar[int]
    SECTION_DATA_FIELD_NUMBER: _ClassVar[int]
    sex: int
    weight: int
    age: int
    height: int
    time_zone: int
    member_id: str
    update_status: int
    section_data: section_data_msg
    def __init__(self, sex: _Optional[int] = ..., weight: _Optional[int] = ..., age: _Optional[int] = ..., height: _Optional[int] = ..., time_zone: _Optional[int] = ..., member_id: _Optional[str] = ..., update_status: _Optional[int] = ..., section_data: _Optional[_Union[section_data_msg, _Mapping]] = ...) -> None: ...

class mode_msg(_message.Message):
    __slots__ = ("mode_index", "mode_color", "valid", "inuse", "template_index", "mode_name")
    MODE_INDEX_FIELD_NUMBER: _ClassVar[int]
    MODE_COLOR_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    INUSE_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_INDEX_FIELD_NUMBER: _ClassVar[int]
    MODE_NAME_FIELD_NUMBER: _ClassVar[int]
    mode_index: int
    mode_color: int
    valid: int
    inuse: int
    template_index: int
    mode_name: str
    def __init__(self, mode_index: _Optional[int] = ..., mode_color: _Optional[int] = ..., valid: _Optional[int] = ..., inuse: _Optional[int] = ..., template_index: _Optional[int] = ..., mode_name: _Optional[str] = ...) -> None: ...

class page_msg(_message.Message):
    __slots__ = ("page_index", "status", "data", "data_site", "page_name", "page_type", "page_mode", "main_page_status", "line_width", "graphic_display")
    PAGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    DATA_SITE_FIELD_NUMBER: _ClassVar[int]
    PAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAGE_MODE_FIELD_NUMBER: _ClassVar[int]
    MAIN_PAGE_STATUS_FIELD_NUMBER: _ClassVar[int]
    LINE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    GRAPHIC_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    page_index: int
    status: int
    data: _containers.RepeatedScalarFieldContainer[int]
    data_site: int
    page_name: str
    page_type: PAGE_TYPE
    page_mode: int
    main_page_status: int
    line_width: int
    graphic_display: int
    def __init__(self, page_index: _Optional[int] = ..., status: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ..., data_site: _Optional[int] = ..., page_name: _Optional[str] = ..., page_type: _Optional[_Union[PAGE_TYPE, str]] = ..., page_mode: _Optional[int] = ..., main_page_status: _Optional[int] = ..., line_width: _Optional[int] = ..., graphic_display: _Optional[int] = ...) -> None: ...

class cur_page_status_msg(_message.Message):
    __slots__ = ("page_line_num_max", "page_line_data_max", "data_page_num_max", "unsupport_data", "lcd_type", "support_page_layout", "main_page_open")
    PAGE_LINE_NUM_MAX_FIELD_NUMBER: _ClassVar[int]
    PAGE_LINE_DATA_MAX_FIELD_NUMBER: _ClassVar[int]
    DATA_PAGE_NUM_MAX_FIELD_NUMBER: _ClassVar[int]
    UNSUPPORT_DATA_FIELD_NUMBER: _ClassVar[int]
    LCD_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_PAGE_LAYOUT_FIELD_NUMBER: _ClassVar[int]
    MAIN_PAGE_OPEN_FIELD_NUMBER: _ClassVar[int]
    page_line_num_max: int
    page_line_data_max: int
    data_page_num_max: int
    unsupport_data: _containers.RepeatedScalarFieldContainer[int]
    lcd_type: LCD_TYPE
    support_page_layout: _containers.RepeatedScalarFieldContainer[int]
    main_page_open: int
    def __init__(self, page_line_num_max: _Optional[int] = ..., page_line_data_max: _Optional[int] = ..., data_page_num_max: _Optional[int] = ..., unsupport_data: _Optional[_Iterable[int]] = ..., lcd_type: _Optional[_Union[LCD_TYPE, str]] = ..., support_page_layout: _Optional[_Iterable[int]] = ..., main_page_open: _Optional[int] = ...) -> None: ...

class bike_msg(_message.Message):
    __slots__ = ("bike_index", "bike_name", "bike_weigth", "wheel_dia", "odometer", "auto_dia", "bike_status")
    BIKE_INDEX_FIELD_NUMBER: _ClassVar[int]
    BIKE_NAME_FIELD_NUMBER: _ClassVar[int]
    BIKE_WEIGTH_FIELD_NUMBER: _ClassVar[int]
    WHEEL_DIA_FIELD_NUMBER: _ClassVar[int]
    ODOMETER_FIELD_NUMBER: _ClassVar[int]
    AUTO_DIA_FIELD_NUMBER: _ClassVar[int]
    BIKE_STATUS_FIELD_NUMBER: _ClassVar[int]
    bike_index: int
    bike_name: str
    bike_weigth: int
    wheel_dia: int
    odometer: int
    auto_dia: int
    bike_status: int
    def __init__(self, bike_index: _Optional[int] = ..., bike_name: _Optional[str] = ..., bike_weigth: _Optional[int] = ..., wheel_dia: _Optional[int] = ..., odometer: _Optional[int] = ..., auto_dia: _Optional[int] = ..., bike_status: _Optional[int] = ...) -> None: ...

class language_msg(_message.Message):
    __slots__ = ("cur_language", "supported_language")
    CUR_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    cur_language: LANGUAGE_TYPE
    supported_language: _containers.RepeatedScalarFieldContainer[LANGUAGE_TYPE]
    def __init__(self, cur_language: _Optional[_Union[LANGUAGE_TYPE, str]] = ..., supported_language: _Optional[_Iterable[_Union[LANGUAGE_TYPE, str]]] = ...) -> None: ...

class backlight_msg(_message.Message):
    __slots__ = ("backlight_night_on", "backling_time", "backlight_auto", "backlight_day_percent", "backlight_night_percent")
    BACKLIGHT_NIGHT_ON_FIELD_NUMBER: _ClassVar[int]
    BACKLING_TIME_FIELD_NUMBER: _ClassVar[int]
    BACKLIGHT_AUTO_FIELD_NUMBER: _ClassVar[int]
    BACKLIGHT_DAY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    BACKLIGHT_NIGHT_PERCENT_FIELD_NUMBER: _ClassVar[int]
    backlight_night_on: int
    backling_time: int
    backlight_auto: int
    backlight_day_percent: int
    backlight_night_percent: int
    def __init__(self, backlight_night_on: _Optional[int] = ..., backling_time: _Optional[int] = ..., backlight_auto: _Optional[int] = ..., backlight_day_percent: _Optional[int] = ..., backlight_night_percent: _Optional[int] = ...) -> None: ...

class data_msg(_message.Message):
    __slots__ = ("data_type", "status")
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data_type: DATA_TYPE
    status: int
    def __init__(self, data_type: _Optional[_Union[DATA_TYPE, str]] = ..., status: _Optional[int] = ...) -> None: ...

class config_msg(_message.Message):
    __slots__ = ("service_type", "config_sevice_type", "config_operate_type", "user_data_message", "page_message", "bike_message", "unit_message", "page_status_message", "altitude", "language_message", "backlight_message", "cur_operate_mode", "mode_message", "alarm_message", "lap_message", "auto_set_message", "key_set_message", "sound_set_message", "data_message")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_SEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_OPERATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DATA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    BIKE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    UNIT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    BACKLIGHT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CUR_OPERATE_MODE_FIELD_NUMBER: _ClassVar[int]
    MODE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ALARM_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAP_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AUTO_SET_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    KEY_SET_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOUND_SET_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DATA_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    service_type: _common_pb2.service_type_index
    config_sevice_type: CONFIG_SERVICE_TYPE
    config_operate_type: CONFIG_OPERATE_TYPE
    user_data_message: user_data_msg
    page_message: _containers.RepeatedCompositeFieldContainer[page_msg]
    bike_message: _containers.RepeatedCompositeFieldContainer[bike_msg]
    unit_message: _containers.RepeatedCompositeFieldContainer[unit_msg]
    page_status_message: cur_page_status_msg
    altitude: int
    language_message: language_msg
    backlight_message: backlight_msg
    cur_operate_mode: int
    mode_message: _containers.RepeatedCompositeFieldContainer[mode_msg]
    alarm_message: _containers.RepeatedCompositeFieldContainer[alarm_msg]
    lap_message: _containers.RepeatedCompositeFieldContainer[lap_msg]
    auto_set_message: _containers.RepeatedCompositeFieldContainer[auto_set_msg]
    key_set_message: _containers.RepeatedCompositeFieldContainer[key_set_msg]
    sound_set_message: _containers.RepeatedCompositeFieldContainer[sound_set_msg]
    data_message: _containers.RepeatedCompositeFieldContainer[data_msg]
    def __init__(self, service_type: _Optional[_Union[_common_pb2.service_type_index, str]] = ..., config_sevice_type: _Optional[_Union[CONFIG_SERVICE_TYPE, str]] = ..., config_operate_type: _Optional[_Union[CONFIG_OPERATE_TYPE, str]] = ..., user_data_message: _Optional[_Union[user_data_msg, _Mapping]] = ..., page_message: _Optional[_Iterable[_Union[page_msg, _Mapping]]] = ..., bike_message: _Optional[_Iterable[_Union[bike_msg, _Mapping]]] = ..., unit_message: _Optional[_Iterable[_Union[unit_msg, _Mapping]]] = ..., page_status_message: _Optional[_Union[cur_page_status_msg, _Mapping]] = ..., altitude: _Optional[int] = ..., language_message: _Optional[_Union[language_msg, _Mapping]] = ..., backlight_message: _Optional[_Union[backlight_msg, _Mapping]] = ..., cur_operate_mode: _Optional[int] = ..., mode_message: _Optional[_Iterable[_Union[mode_msg, _Mapping]]] = ..., alarm_message: _Optional[_Iterable[_Union[alarm_msg, _Mapping]]] = ..., lap_message: _Optional[_Iterable[_Union[lap_msg, _Mapping]]] = ..., auto_set_message: _Optional[_Iterable[_Union[auto_set_msg, _Mapping]]] = ..., key_set_message: _Optional[_Iterable[_Union[key_set_msg, _Mapping]]] = ..., sound_set_message: _Optional[_Iterable[_Union[sound_set_msg, _Mapping]]] = ..., data_message: _Optional[_Iterable[_Union[data_msg, _Mapping]]] = ...) -> None: ...

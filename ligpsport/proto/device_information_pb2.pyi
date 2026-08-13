from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FunctionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATA_MANAGEMENT_MODULE: _ClassVar[FunctionType]
    DATA_MANAGEMENT_ACTIVITIES_FUNCTION: _ClassVar[FunctionType]
    DATA_MANAGEMENT_ACTIVITIES_LIST_INFORMATION_FUNCTION: _ClassVar[FunctionType]
    DATA_MANAGEMENT_ROUTES_FUNCTION: _ClassVar[FunctionType]
    DATA_MANAGEMENT_WORKOUTS_FUNCTION: _ClassVar[FunctionType]
    DATA_MANAGEMENT_SYNC_SETTING_FUNCTION: _ClassVar[FunctionType]
    DEVICE_SETTINGS_MODULE: _ClassVar[FunctionType]
    PROMPT_FOR_DELETION_WHEN_THE_DEVICE_ACTIVE_FILE_IS_FULL: _ClassVar[FunctionType]
    NOTIFICATION_MODULE: _ClassVar[FunctionType]
    NOTIFICATION_INCOMING_CALL_FUNCTION: _ClassVar[FunctionType]
    NOTIFICATION_INCOMING_MESSAGE_FUNCTION: _ClassVar[FunctionType]
    NOTIFICATION_APP_FUNCTION: _ClassVar[FunctionType]
    NAVIGATION_MAP_MODULE: _ClassVar[FunctionType]
    UNIT_MODULE: _ClassVar[FunctionType]
    UNIT_METRIC_FUNCTION: _ClassVar[FunctionType]
    UNIT_IMPERIAL_FUNCTION: _ClassVar[FunctionType]
    UNIT_CUSTOMIZE_FUNCTION: _ClassVar[FunctionType]
    CYCLING_COMPUTER_CONFIG_MODULE: _ClassVar[FunctionType]
    KEY_FUNCTION_SET_SUB_MODULE: _ClassVar[FunctionType]
    AUTO_FUNCTION_SET_SUB_MODULE: _ClassVar[FunctionType]
    AUTO_PAUSE_FUNCTION: _ClassVar[FunctionType]
    AUTO_RECORD_START_FUNCTION: _ClassVar[FunctionType]
    AUTO_POWER_OFF_FUNCTION: _ClassVar[FunctionType]
    AUTO_SLEEP_FUNCTION: _ClassVar[FunctionType]
    AUTO_HOME_PAGE_BACK_FUNCTION: _ClassVar[FunctionType]
    SMART_SAVE_FUNCTION: _ClassVar[FunctionType]
    ALARM_SET_SUB_MODULE: _ClassVar[FunctionType]
    ALARM_RIDE_TIME_FUNCTION: _ClassVar[FunctionType]
    ALARM_RIDE_DISTANCE_FUNCTION: _ClassVar[FunctionType]
    ALARM_HRM_FUNCTION: _ClassVar[FunctionType]
    ALARM_CAD_FUNCTION: _ClassVar[FunctionType]
    ALARM_PWR_FUNCTION: _ClassVar[FunctionType]
    ALARM_CALORIE_FUNCTION: _ClassVar[FunctionType]
    LAP_SET_SUB_MODULE: _ClassVar[FunctionType]
    SOUND_MODULE: _ClassVar[FunctionType]
    SOUND_KEY_FUNCTION: _ClassVar[FunctionType]
    SOUND_BEEP_FUNCTION: _ClassVar[FunctionType]
    UPLOAD_LOG_MODULE: _ClassVar[FunctionType]
    AUTO_RECORD_START_SUPPORT_THRESHOLD: _ClassVar[FunctionType]
    AUTO_PAUSE_SUPPORT_THRESHOLD: _ClassVar[FunctionType]
    AUTO_FUNCTION_SET_SUB_MODULE_520: _ClassVar[FunctionType]
    WEATHER_TEST_MODULE: _ClassVar[FunctionType]
    ROUTES_MODULE: _ClassVar[FunctionType]
    ROUTE_SUPPORT_DIFFERENCE_ALGORITHM: _ClassVar[FunctionType]
    ROUTE_SUPPORT_ONLY_SINGLE_ROUTE: _ClassVar[FunctionType]
    ROUTE_SUPPORT_AUXILIARY_POINT: _ClassVar[FunctionType]
    BROADCAST_MODULE: _ClassVar[FunctionType]
    GROUP_TRACK_MODULE: _ClassVar[FunctionType]
    SENSORS_MODULE: _ClassVar[FunctionType]
    CRANK_LENGTH_PLUS: _ClassVar[FunctionType]
    POWER_CALIBRATION: _ClassVar[FunctionType]
    FIRMWARE_DETECTION_MODULE: _ClassVar[FunctionType]
    WIFI_MODULE: _ClassVar[FunctionType]
    PAGE_SETTING_MODULE: _ClassVar[FunctionType]
    PAGE_SETTING_NAME_MAPPING: _ClassVar[FunctionType]
    PAGE_COMPASS: _ClassVar[FunctionType]
    TRAINING_MODULE: _ClassVar[FunctionType]
    BIKE_SETTING_MODULE: _ClassVar[FunctionType]
    PERSONAL_SETTINGS_MODULE: _ClassVar[FunctionType]
    FONT_DOWNLOAD_MODULE: _ClassVar[FunctionType]
    ANTI_THEFT_ALARM_MODULE: _ClassVar[FunctionType]
    SEND_WEATHER_INFORMATION_MODULE: _ClassVar[FunctionType]
    SEND_AGPS_MODULE: _ClassVar[FunctionType]
    SEND_USER_INFORMATION_MODULE: _ClassVar[FunctionType]
    SEND_OFFLINE_AGPS_MODULE: _ClassVar[FunctionType]
    REMOVE_DEVICE_MODULE: _ClassVar[FunctionType]
    MODEL_MANAGEMENT_MODULE: _ClassVar[FunctionType]
    EDIT_MODEL_MANAGEMENT_MODULE: _ClassVar[FunctionType]
    THEME_MANAGEMENT_MODULE: _ClassVar[FunctionType]
    DISPLAY_SETTING_MODULE: _ClassVar[FunctionType]
    ALTITUDE_CALIBRATION_MODULE: _ClassVar[FunctionType]
    OTHER_SETTING_MODULE: _ClassVar[FunctionType]
    CALCULATE_AVERAGE_CADENCE_FILTER_0_VALUE: _ClassVar[FunctionType]
    CALCULATE_AVERAGE_POWER_FILTER_0_VALUE: _ClassVar[FunctionType]
    MOTION_STATE_DETECTION: _ClassVar[FunctionType]
    AUTO_START_CUSTOM: _ClassVar[FunctionType]
    AUTO_START_ALERT: _ClassVar[FunctionType]
    AUTO_PAGE_SLOW: _ClassVar[FunctionType]
    AUTO_PAGE_NORMAL: _ClassVar[FunctionType]
    POWER_SAVING_MODEL: _ClassVar[FunctionType]
    SMART_POWER_SAVING_FUNCTIONALITY: _ClassVar[FunctionType]
    BLE_MAP_MODULE: _ClassVar[FunctionType]
    ALARM_SPEED_FUNCTION: _ClassVar[FunctionType]
    READ_SN_FUNCTION: _ClassVar[FunctionType]
    HR_DEVICE: _ClassVar[FunctionType]
    SPD_DEVICE: _ClassVar[FunctionType]
    CAD_DEVICE: _ClassVar[FunctionType]
    ADVANCED_HR_DEVICE: _ClassVar[FunctionType]
    RADAR_DEVICE: _ClassVar[FunctionType]
DATA_MANAGEMENT_MODULE: FunctionType
DATA_MANAGEMENT_ACTIVITIES_FUNCTION: FunctionType
DATA_MANAGEMENT_ACTIVITIES_LIST_INFORMATION_FUNCTION: FunctionType
DATA_MANAGEMENT_ROUTES_FUNCTION: FunctionType
DATA_MANAGEMENT_WORKOUTS_FUNCTION: FunctionType
DATA_MANAGEMENT_SYNC_SETTING_FUNCTION: FunctionType
DEVICE_SETTINGS_MODULE: FunctionType
PROMPT_FOR_DELETION_WHEN_THE_DEVICE_ACTIVE_FILE_IS_FULL: FunctionType
NOTIFICATION_MODULE: FunctionType
NOTIFICATION_INCOMING_CALL_FUNCTION: FunctionType
NOTIFICATION_INCOMING_MESSAGE_FUNCTION: FunctionType
NOTIFICATION_APP_FUNCTION: FunctionType
NAVIGATION_MAP_MODULE: FunctionType
UNIT_MODULE: FunctionType
UNIT_METRIC_FUNCTION: FunctionType
UNIT_IMPERIAL_FUNCTION: FunctionType
UNIT_CUSTOMIZE_FUNCTION: FunctionType
CYCLING_COMPUTER_CONFIG_MODULE: FunctionType
KEY_FUNCTION_SET_SUB_MODULE: FunctionType
AUTO_FUNCTION_SET_SUB_MODULE: FunctionType
AUTO_PAUSE_FUNCTION: FunctionType
AUTO_RECORD_START_FUNCTION: FunctionType
AUTO_POWER_OFF_FUNCTION: FunctionType
AUTO_SLEEP_FUNCTION: FunctionType
AUTO_HOME_PAGE_BACK_FUNCTION: FunctionType
SMART_SAVE_FUNCTION: FunctionType
ALARM_SET_SUB_MODULE: FunctionType
ALARM_RIDE_TIME_FUNCTION: FunctionType
ALARM_RIDE_DISTANCE_FUNCTION: FunctionType
ALARM_HRM_FUNCTION: FunctionType
ALARM_CAD_FUNCTION: FunctionType
ALARM_PWR_FUNCTION: FunctionType
ALARM_CALORIE_FUNCTION: FunctionType
LAP_SET_SUB_MODULE: FunctionType
SOUND_MODULE: FunctionType
SOUND_KEY_FUNCTION: FunctionType
SOUND_BEEP_FUNCTION: FunctionType
UPLOAD_LOG_MODULE: FunctionType
AUTO_RECORD_START_SUPPORT_THRESHOLD: FunctionType
AUTO_PAUSE_SUPPORT_THRESHOLD: FunctionType
AUTO_FUNCTION_SET_SUB_MODULE_520: FunctionType
WEATHER_TEST_MODULE: FunctionType
ROUTES_MODULE: FunctionType
ROUTE_SUPPORT_DIFFERENCE_ALGORITHM: FunctionType
ROUTE_SUPPORT_ONLY_SINGLE_ROUTE: FunctionType
ROUTE_SUPPORT_AUXILIARY_POINT: FunctionType
BROADCAST_MODULE: FunctionType
GROUP_TRACK_MODULE: FunctionType
SENSORS_MODULE: FunctionType
CRANK_LENGTH_PLUS: FunctionType
POWER_CALIBRATION: FunctionType
FIRMWARE_DETECTION_MODULE: FunctionType
WIFI_MODULE: FunctionType
PAGE_SETTING_MODULE: FunctionType
PAGE_SETTING_NAME_MAPPING: FunctionType
PAGE_COMPASS: FunctionType
TRAINING_MODULE: FunctionType
BIKE_SETTING_MODULE: FunctionType
PERSONAL_SETTINGS_MODULE: FunctionType
FONT_DOWNLOAD_MODULE: FunctionType
ANTI_THEFT_ALARM_MODULE: FunctionType
SEND_WEATHER_INFORMATION_MODULE: FunctionType
SEND_AGPS_MODULE: FunctionType
SEND_USER_INFORMATION_MODULE: FunctionType
SEND_OFFLINE_AGPS_MODULE: FunctionType
REMOVE_DEVICE_MODULE: FunctionType
MODEL_MANAGEMENT_MODULE: FunctionType
EDIT_MODEL_MANAGEMENT_MODULE: FunctionType
THEME_MANAGEMENT_MODULE: FunctionType
DISPLAY_SETTING_MODULE: FunctionType
ALTITUDE_CALIBRATION_MODULE: FunctionType
OTHER_SETTING_MODULE: FunctionType
CALCULATE_AVERAGE_CADENCE_FILTER_0_VALUE: FunctionType
CALCULATE_AVERAGE_POWER_FILTER_0_VALUE: FunctionType
MOTION_STATE_DETECTION: FunctionType
AUTO_START_CUSTOM: FunctionType
AUTO_START_ALERT: FunctionType
AUTO_PAGE_SLOW: FunctionType
AUTO_PAGE_NORMAL: FunctionType
POWER_SAVING_MODEL: FunctionType
SMART_POWER_SAVING_FUNCTIONALITY: FunctionType
BLE_MAP_MODULE: FunctionType
ALARM_SPEED_FUNCTION: FunctionType
READ_SN_FUNCTION: FunctionType
HR_DEVICE: FunctionType
SPD_DEVICE: FunctionType
CAD_DEVICE: FunctionType
ADVANCED_HR_DEVICE: FunctionType
RADAR_DEVICE: FunctionType

class DeviceInfo(_message.Message):
    __slots__ = ("deviceImage", "devName", "devCustomName", "generation", "isSupportProtoBuf", "sendFileMtuSize", "dataReceiveTimeOut", "functionTypeList", "manufacturerSpecificData", "mapManual", "pagingInformation", "isAccessory", "ephemerisEffectiveTime", "deviceMaxActivityFileNum", "connectionMode", "androidSupportMinVersion")
    DEVICEIMAGE_FIELD_NUMBER: _ClassVar[int]
    DEVNAME_FIELD_NUMBER: _ClassVar[int]
    DEVCUSTOMNAME_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    ISSUPPORTPROTOBUF_FIELD_NUMBER: _ClassVar[int]
    SENDFILEMTUSIZE_FIELD_NUMBER: _ClassVar[int]
    DATARECEIVETIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONTYPELIST_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURERSPECIFICDATA_FIELD_NUMBER: _ClassVar[int]
    MAPMANUAL_FIELD_NUMBER: _ClassVar[int]
    PAGINGINFORMATION_FIELD_NUMBER: _ClassVar[int]
    ISACCESSORY_FIELD_NUMBER: _ClassVar[int]
    EPHEMERISEFFECTIVETIME_FIELD_NUMBER: _ClassVar[int]
    DEVICEMAXACTIVITYFILENUM_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONMODE_FIELD_NUMBER: _ClassVar[int]
    ANDROIDSUPPORTMINVERSION_FIELD_NUMBER: _ClassVar[int]
    deviceImage: _containers.RepeatedCompositeFieldContainer[DeviceImage]
    devName: str
    devCustomName: str
    generation: int
    isSupportProtoBuf: bool
    sendFileMtuSize: int
    dataReceiveTimeOut: int
    functionTypeList: _containers.RepeatedScalarFieldContainer[FunctionType]
    manufacturerSpecificData: str
    mapManual: _containers.RepeatedCompositeFieldContainer[MapManual]
    pagingInformation: _containers.RepeatedCompositeFieldContainer[PagingInformation]
    isAccessory: bool
    ephemerisEffectiveTime: int
    deviceMaxActivityFileNum: int
    connectionMode: int
    androidSupportMinVersion: int
    def __init__(self, deviceImage: _Optional[_Iterable[_Union[DeviceImage, _Mapping]]] = ..., devName: _Optional[str] = ..., devCustomName: _Optional[str] = ..., generation: _Optional[int] = ..., isSupportProtoBuf: _Optional[bool] = ..., sendFileMtuSize: _Optional[int] = ..., dataReceiveTimeOut: _Optional[int] = ..., functionTypeList: _Optional[_Iterable[_Union[FunctionType, str]]] = ..., manufacturerSpecificData: _Optional[str] = ..., mapManual: _Optional[_Iterable[_Union[MapManual, _Mapping]]] = ..., pagingInformation: _Optional[_Iterable[_Union[PagingInformation, _Mapping]]] = ..., isAccessory: _Optional[bool] = ..., ephemerisEffectiveTime: _Optional[int] = ..., deviceMaxActivityFileNum: _Optional[int] = ..., connectionMode: _Optional[int] = ..., androidSupportMinVersion: _Optional[int] = ...) -> None: ...

class MapManual(_message.Message):
    __slots__ = ("manualType", "url")
    class ManualType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[MapManual.ManualType]
        UNBIND: _ClassVar[MapManual.ManualType]
        CONNECT_HELP: _ClassVar[MapManual.ManualType]
    INVALID: MapManual.ManualType
    UNBIND: MapManual.ManualType
    CONNECT_HELP: MapManual.ManualType
    MANUALTYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    manualType: MapManual.ManualType
    url: str
    def __init__(self, manualType: _Optional[_Union[MapManual.ManualType, str]] = ..., url: _Optional[str] = ...) -> None: ...

class DeviceImage(_message.Message):
    __slots__ = ("imageType", "url")
    class ImageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[DeviceImage.ImageType]
        BIG: _ClassVar[DeviceImage.ImageType]
        SMALL: _ClassVar[DeviceImage.ImageType]
        BACKGROUND_IN_PAGE_SETTING: _ClassVar[DeviceImage.ImageType]
        DFU: _ClassVar[DeviceImage.ImageType]
        UNBINDING_ANIMATION: _ClassVar[DeviceImage.ImageType]
    INVALID: DeviceImage.ImageType
    BIG: DeviceImage.ImageType
    SMALL: DeviceImage.ImageType
    BACKGROUND_IN_PAGE_SETTING: DeviceImage.ImageType
    DFU: DeviceImage.ImageType
    UNBINDING_ANIMATION: DeviceImage.ImageType
    IMAGETYPE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    imageType: DeviceImage.ImageType
    url: str
    def __init__(self, imageType: _Optional[_Union[DeviceImage.ImageType, str]] = ..., url: _Optional[str] = ...) -> None: ...

class PagingInformation(_message.Message):
    __slots__ = ("function", "isSupportPaging")
    class Function(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[PagingInformation.Function]
        ACTIVITIES: _ClassVar[PagingInformation.Function]
        ROUTES: _ClassVar[PagingInformation.Function]
        WORKOUTS: _ClassVar[PagingInformation.Function]
    INVALID: PagingInformation.Function
    ACTIVITIES: PagingInformation.Function
    ROUTES: PagingInformation.Function
    WORKOUTS: PagingInformation.Function
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    ISSUPPORTPAGING_FIELD_NUMBER: _ClassVar[int]
    function: PagingInformation.Function
    isSupportPaging: bool
    def __init__(self, function: _Optional[_Union[PagingInformation.Function, str]] = ..., isSupportPaging: _Optional[bool] = ...) -> None: ...

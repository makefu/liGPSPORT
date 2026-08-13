from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class file_download(_message.Message):
    __slots__ = ("file_size", "file_type", "file_id", "file_name")
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    FILE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_size: int
    file_type: int
    file_id: int
    file_name: str
    def __init__(self, file_size: _Optional[int] = ..., file_type: _Optional[int] = ..., file_id: _Optional[int] = ..., file_name: _Optional[str] = ...) -> None: ...

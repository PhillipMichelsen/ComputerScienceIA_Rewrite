from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileServiceTaskRequest(_message.Message):
    __slots__ = ("task_id", "job_id")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    job_id: str
    def __init__(self, task_id: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

class FileServiceAcknowledgement(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

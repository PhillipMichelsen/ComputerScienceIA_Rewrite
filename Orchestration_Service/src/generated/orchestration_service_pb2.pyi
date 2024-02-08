from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateJobRequest(_message.Message):
    __slots__ = ("job_name", "notification_endpoint", "initial_job_data")
    class InitialJobDataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    INITIAL_JOB_DATA_FIELD_NUMBER: _ClassVar[int]
    job_name: str
    notification_endpoint: str
    initial_job_data: _containers.ScalarMap[str, str]
    def __init__(self, job_name: _Optional[str] = ..., notification_endpoint: _Optional[str] = ..., initial_job_data: _Optional[_Mapping[str, str]] = ...) -> None: ...

class AddTaskToJobRequest(_message.Message):
    __slots__ = ("job_id", "task_name")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_NAME_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    task_name: str
    def __init__(self, job_id: _Optional[str] = ..., task_name: _Optional[str] = ...) -> None: ...

class NotifyJobRequest(_message.Message):
    __slots__ = ("task_id", "job_id", "notification")
    class NotificationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    job_id: str
    notification: _containers.ScalarMap[str, str]
    def __init__(self, task_id: _Optional[str] = ..., job_id: _Optional[str] = ..., notification: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TaskCompletedRequest(_message.Message):
    __slots__ = ("task_id", "job_id")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    job_id: str
    def __init__(self, task_id: _Optional[str] = ..., job_id: _Optional[str] = ...) -> None: ...

class TaskErrorRequest(_message.Message):
    __slots__ = ("task_id", "job_id", "error_message")
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    job_id: str
    error_message: str
    def __init__(self, task_id: _Optional[str] = ..., job_id: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class Acknowledgement(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

from typing import ClassVar as _ClassVar, Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor


class RegisterServiceRequest(_message.Message):
    __slots__ = ("service_type", "service_address", "service_port")
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PORT_FIELD_NUMBER: _ClassVar[int]
    service_type: str
    service_address: str
    service_port: str

    def __init__(self, service_type: _Optional[str] = ..., service_address: _Optional[str] = ...,
                 service_port: _Optional[str] = ...) -> None: ...


class RegisterServiceResponse(_message.Message):
    __slots__ = ("service_id",)
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    service_id: str

    def __init__(self, service_id: _Optional[str] = ...) -> None: ...


class DeregisterServiceRequest(_message.Message):
    __slots__ = ("service_id",)
    SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    service_id: str

    def __init__(self, service_id: _Optional[str] = ...) -> None: ...


class DeregisterServiceResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool

    def __init__(self, success: bool = ...) -> None: ...


class GetServiceRequest(_message.Message):
    __slots__ = ("service_type",)
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    service_type: str

    def __init__(self, service_type: _Optional[str] = ...) -> None: ...


class GetServiceResponse(_message.Message):
    __slots__ = ("service_host", "service_port")
    SERVICE_HOST_FIELD_NUMBER: _ClassVar[int]
    SERVICE_PORT_FIELD_NUMBER: _ClassVar[int]
    service_host: str
    service_port: str

    def __init__(self, service_host: _Optional[str] = ..., service_port: _Optional[str] = ...) -> None: ...


class HealthCheckRequest(_message.Message):
    __slots__ = ("serviceName",)
    SERVICENAME_FIELD_NUMBER: _ClassVar[int]
    serviceName: str

    def __init__(self, serviceName: _Optional[str] = ...) -> None: ...


class HealthCheckResponse(_message.Message):
    __slots__ = ("healthy",)
    HEALTHY_FIELD_NUMBER: _ClassVar[int]
    healthy: bool

    def __init__(self, healthy: bool = ...) -> None: ...

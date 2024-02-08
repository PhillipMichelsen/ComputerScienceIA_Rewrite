# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: discovery_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x17\x64iscovery_service.proto\x12\x11\x64iscovery_service\"]\n\x16RegisterServiceRequest\x12\x14\n\x0cservice_type\x18\x01 \x01(\t\x12\x17\n\x0fservice_address\x18\x02 \x01(\t\x12\x14\n\x0cservice_port\x18\x03 \x01(\t\"-\n\x17RegisterServiceResponse\x12\x12\n\nservice_id\x18\x01 \x01(\t\".\n\x18\x44\x65registerServiceRequest\x12\x12\n\nservice_id\x18\x01 \x01(\t\",\n\x19\x44\x65registerServiceResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\")\n\x11GetServiceRequest\x12\x14\n\x0cservice_type\x18\x01 \x01(\t\"@\n\x12GetServiceResponse\x12\x14\n\x0cservice_host\x18\x01 \x01(\t\x12\x14\n\x0cservice_port\x18\x02 \x01(\t\")\n\x12HealthCheckRequest\x12\x13\n\x0bserviceName\x18\x01 \x01(\t\"&\n\x13HealthCheckResponse\x12\x0f\n\x07healthy\x18\x01 \x01(\x08\x32\xec\x01\n\x0cRegistration\x12j\n\x0fRegisterService\x12).discovery_service.RegisterServiceRequest\x1a*.discovery_service.RegisterServiceResponse\"\x00\x12p\n\x11\x44\x65registerService\x12+.discovery_service.DeregisterServiceRequest\x1a,.discovery_service.DeregisterServiceResponse\"\x00\x32h\n\tRetrieval\x12[\n\nGetService\x12$.discovery_service.GetServiceRequest\x1a%.discovery_service.GetServiceResponse\"\x00\x32h\n\x06Health\x12^\n\x0bHealthCheck\x12%.discovery_service.HealthCheckRequest\x1a&.discovery_service.HealthCheckResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'discovery_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_REGISTERSERVICEREQUEST']._serialized_start = 46
    _globals['_REGISTERSERVICEREQUEST']._serialized_end = 139
    _globals['_REGISTERSERVICERESPONSE']._serialized_start = 141
    _globals['_REGISTERSERVICERESPONSE']._serialized_end = 186
    _globals['_DEREGISTERSERVICEREQUEST']._serialized_start = 188
    _globals['_DEREGISTERSERVICEREQUEST']._serialized_end = 234
    _globals['_DEREGISTERSERVICERESPONSE']._serialized_start = 236
    _globals['_DEREGISTERSERVICERESPONSE']._serialized_end = 280
    _globals['_GETSERVICEREQUEST']._serialized_start = 282
    _globals['_GETSERVICEREQUEST']._serialized_end = 323
    _globals['_GETSERVICERESPONSE']._serialized_start = 325
    _globals['_GETSERVICERESPONSE']._serialized_end = 389
    _globals['_HEALTHCHECKREQUEST']._serialized_start = 391
    _globals['_HEALTHCHECKREQUEST']._serialized_end = 432
    _globals['_HEALTHCHECKRESPONSE']._serialized_start = 434
    _globals['_HEALTHCHECKRESPONSE']._serialized_end = 472
    _globals['_REGISTRATION']._serialized_start = 475
    _globals['_REGISTRATION']._serialized_end = 711
    _globals['_RETRIEVAL']._serialized_start = 713
    _globals['_RETRIEVAL']._serialized_end = 817
    _globals['_HEALTH']._serialized_start = 819
    _globals['_HEALTH']._serialized_end = 923
# @@protoc_insertion_point(module_scope)

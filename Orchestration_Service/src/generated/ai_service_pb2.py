# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ai_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x10\x61i_service.proto\x12\nai_service\"7\n\x14\x41IServiceTaskRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0e\n\x06job_id\x18\x02 \x01(\t\"+\n\x18\x41IServiceAcknowledgement\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32m\n\x12LLMAgentSubService\x12W\n\x0bInvokeAgent\x12 .ai_service.AIServiceTaskRequest\x1a$.ai_service.AIServiceAcknowledgement\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ai_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_AISERVICETASKREQUEST']._serialized_start = 32
    _globals['_AISERVICETASKREQUEST']._serialized_end = 87
    _globals['_AISERVICEACKNOWLEDGEMENT']._serialized_start = 89
    _globals['_AISERVICEACKNOWLEDGEMENT']._serialized_end = 132
    _globals['_LLMAGENTSUBSERVICE']._serialized_start = 134
    _globals['_LLMAGENTSUBSERVICE']._serialized_end = 243
# @@protoc_insertion_point(module_scope)

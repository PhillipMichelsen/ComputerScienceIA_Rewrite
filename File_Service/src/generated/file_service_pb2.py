# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x66ile_service.proto\x12\x0c\x66ile_service\"9\n\x16\x46ileServiceTaskRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0e\n\x06job_id\x18\x02 \x01(\t\"-\n\x1a\x46ileServiceAcknowledgement\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xf0\x01\n\x16PresignedURLSubService\x12i\n\x15GetPresignedUploadURL\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x12k\n\x17GetPresignedDownloadURL\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x32\xae\x03\n\x17\x46ileEmbeddingSubService\x12`\n\x0cRegisterFile\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x12`\n\x0cGetFilesInfo\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x12_\n\x0bProcessFile\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x12n\n\x1aRetrieveNearestNParagraphs\x12$.file_service.FileServiceTaskRequest\x1a(.file_service.FileServiceAcknowledgement\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'file_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FILESERVICETASKREQUEST']._serialized_start=36
  _globals['_FILESERVICETASKREQUEST']._serialized_end=93
  _globals['_FILESERVICEACKNOWLEDGEMENT']._serialized_start=95
  _globals['_FILESERVICEACKNOWLEDGEMENT']._serialized_end=140
  _globals['_PRESIGNEDURLSUBSERVICE']._serialized_start=143
  _globals['_PRESIGNEDURLSUBSERVICE']._serialized_end=383
  _globals['_FILEEMBEDDINGSUBSERVICE']._serialized_start=386
  _globals['_FILEEMBEDDINGSUBSERVICE']._serialized_end=816
# @@protoc_insertion_point(module_scope)
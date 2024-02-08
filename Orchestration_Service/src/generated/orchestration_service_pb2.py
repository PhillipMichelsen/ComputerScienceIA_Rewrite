# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: orchestration_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1borchestration_service.proto\x12\x15orchestration_service\"\xd1\x01\n\x10\x43reateJobRequest\x12\x10\n\x08job_name\x18\x01 \x01(\t\x12\x1d\n\x15notification_endpoint\x18\x02 \x01(\t\x12U\n\x10initial_job_data\x18\x03 \x03(\x0b\x32;.orchestration_service.CreateJobRequest.InitialJobDataEntry\x1a\x35\n\x13InitialJobDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"8\n\x13\x41\x64\x64TaskToJobRequest\x12\x0e\n\x06job_id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t\"\xb9\x01\n\x10NotifyJobRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0e\n\x06job_id\x18\x02 \x01(\t\x12O\n\x0cnotification\x18\x03 \x03(\x0b\x32\x39.orchestration_service.NotifyJobRequest.NotificationEntry\x1a\x33\n\x11NotificationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"7\n\x14TaskCompletedRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0e\n\x06job_id\x18\x02 \x01(\t\"J\n\x10TaskErrorRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0e\n\x06job_id\x18\x02 \x01(\t\x12\x15\n\rerror_message\x18\x03 \x01(\t\"\"\n\x0f\x41\x63knowledgement\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xb2\x02\n\nJobService\x12^\n\tCreateJob\x12\'.orchestration_service.CreateJobRequest\x1a&.orchestration_service.Acknowledgement\"\x00\x12\x64\n\x0c\x41\x64\x64TaskToJob\x12*.orchestration_service.AddTaskToJobRequest\x1a&.orchestration_service.Acknowledgement\"\x00\x12^\n\tNotifyJob\x12\'.orchestration_service.NotifyJobRequest\x1a&.orchestration_service.Acknowledgement\"\x00\x32\xd5\x01\n\x0bTaskService\x12\x66\n\rTaskCompleted\x12+.orchestration_service.TaskCompletedRequest\x1a&.orchestration_service.Acknowledgement\"\x00\x12^\n\tTaskError\x12\'.orchestration_service.TaskErrorRequest\x1a&.orchestration_service.Acknowledgement\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'orchestration_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CREATEJOBREQUEST_INITIALJOBDATAENTRY']._options = None
  _globals['_CREATEJOBREQUEST_INITIALJOBDATAENTRY']._serialized_options = b'8\001'
  _globals['_NOTIFYJOBREQUEST_NOTIFICATIONENTRY']._options = None
  _globals['_NOTIFYJOBREQUEST_NOTIFICATIONENTRY']._serialized_options = b'8\001'
  _globals['_CREATEJOBREQUEST']._serialized_start=55
  _globals['_CREATEJOBREQUEST']._serialized_end=264
  _globals['_CREATEJOBREQUEST_INITIALJOBDATAENTRY']._serialized_start=211
  _globals['_CREATEJOBREQUEST_INITIALJOBDATAENTRY']._serialized_end=264
  _globals['_ADDTASKTOJOBREQUEST']._serialized_start=266
  _globals['_ADDTASKTOJOBREQUEST']._serialized_end=322
  _globals['_NOTIFYJOBREQUEST']._serialized_start=325
  _globals['_NOTIFYJOBREQUEST']._serialized_end=510
  _globals['_NOTIFYJOBREQUEST_NOTIFICATIONENTRY']._serialized_start=459
  _globals['_NOTIFYJOBREQUEST_NOTIFICATIONENTRY']._serialized_end=510
  _globals['_TASKCOMPLETEDREQUEST']._serialized_start=512
  _globals['_TASKCOMPLETEDREQUEST']._serialized_end=567
  _globals['_TASKERRORREQUEST']._serialized_start=569
  _globals['_TASKERRORREQUEST']._serialized_end=643
  _globals['_ACKNOWLEDGEMENT']._serialized_start=645
  _globals['_ACKNOWLEDGEMENT']._serialized_end=679
  _globals['_JOBSERVICE']._serialized_start=682
  _globals['_JOBSERVICE']._serialized_end=988
  _globals['_TASKSERVICE']._serialized_start=991
  _globals['_TASKSERVICE']._serialized_end=1204
# @@protoc_insertion_point(module_scope)

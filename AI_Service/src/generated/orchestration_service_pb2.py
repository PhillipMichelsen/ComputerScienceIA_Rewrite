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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1borchestration_service.proto\x12\x15orchestration_service"\xda\x01\n\x10\x43reateJobRequest\x12\x10\n\x08job_name\x18\x01 \x01(\t\x12\x12\n\nservice_id\x18\x02 \x01(\t\x12\x12\n\nrequest_id\x18\x03 \x01(\t\x12U\n\x10initial_job_data\x18\x04 \x03(\x0b\x32;.orchestration_service.CreateJobRequest.InitialJobDataEntry\x1a\x35\n\x13InitialJobDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"8\n\x13\x41\x64\x64TaskToJobRequest\x12\x0e\n\x06job_id\x18\x01 \x01(\t\x12\x11\n\ttask_name\x18\x02 \x01(\t"\xa9\x01\n\x10NotifyJobRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12O\n\x0cnotification\x18\x02 \x03(\x0b\x32\x39.orchestration_service.NotifyJobRequest.NotificationEntry\x1a\x33\n\x11NotificationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\'\n\x14TaskCompletedRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t":\n\x10TaskErrorRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x15\n\rerror_message\x18\x02 \x01(\t"6\n#OrchestrationServiceAcknowledgement\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xf1\x02\n\rJobSubService\x12r\n\tCreateJob\x12\'.orchestration_service.CreateJobRequest\x1a:.orchestration_service.OrchestrationServiceAcknowledgement"\x00\x12x\n\x0c\x41\x64\x64TaskToJob\x12*.orchestration_service.AddTaskToJobRequest\x1a:.orchestration_service.OrchestrationServiceAcknowledgement"\x00\x12r\n\tNotifyJob\x12\'.orchestration_service.NotifyJobRequest\x1a:.orchestration_service.OrchestrationServiceAcknowledgement"\x00\x32\x80\x02\n\x0eTaskSubService\x12z\n\rTaskCompleted\x12+.orchestration_service.TaskCompletedRequest\x1a:.orchestration_service.OrchestrationServiceAcknowledgement"\x00\x12r\n\tTaskError\x12\'.orchestration_service.TaskErrorRequest\x1a:.orchestration_service.OrchestrationServiceAcknowledgement"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "orchestration_service_pb2", _globals
)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_CREATEJOBREQUEST_INITIALJOBDATAENTRY"]._options = None
    _globals["_CREATEJOBREQUEST_INITIALJOBDATAENTRY"]._serialized_options = b"8\001"
    _globals["_NOTIFYJOBREQUEST_NOTIFICATIONENTRY"]._options = None
    _globals["_NOTIFYJOBREQUEST_NOTIFICATIONENTRY"]._serialized_options = b"8\001"
    _globals["_CREATEJOBREQUEST"]._serialized_start = 55
    _globals["_CREATEJOBREQUEST"]._serialized_end = 273
    _globals["_CREATEJOBREQUEST_INITIALJOBDATAENTRY"]._serialized_start = 220
    _globals["_CREATEJOBREQUEST_INITIALJOBDATAENTRY"]._serialized_end = 273
    _globals["_ADDTASKTOJOBREQUEST"]._serialized_start = 275
    _globals["_ADDTASKTOJOBREQUEST"]._serialized_end = 331
    _globals["_NOTIFYJOBREQUEST"]._serialized_start = 334
    _globals["_NOTIFYJOBREQUEST"]._serialized_end = 503
    _globals["_NOTIFYJOBREQUEST_NOTIFICATIONENTRY"]._serialized_start = 452
    _globals["_NOTIFYJOBREQUEST_NOTIFICATIONENTRY"]._serialized_end = 503
    _globals["_TASKCOMPLETEDREQUEST"]._serialized_start = 505
    _globals["_TASKCOMPLETEDREQUEST"]._serialized_end = 544
    _globals["_TASKERRORREQUEST"]._serialized_start = 546
    _globals["_TASKERRORREQUEST"]._serialized_end = 604
    _globals["_ORCHESTRATIONSERVICEACKNOWLEDGEMENT"]._serialized_start = 606
    _globals["_ORCHESTRATIONSERVICEACKNOWLEDGEMENT"]._serialized_end = 660
    _globals["_JOBSUBSERVICE"]._serialized_start = 663
    _globals["_JOBSUBSERVICE"]._serialized_end = 1032
    _globals["_TASKSUBSERVICE"]._serialized_start = 1035
    _globals["_TASKSUBSERVICE"]._serialized_end = 1291
# @@protoc_insertion_point(module_scope)

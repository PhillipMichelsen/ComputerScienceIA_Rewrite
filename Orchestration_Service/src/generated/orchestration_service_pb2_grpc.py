# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.generated.orchestration_service_pb2 as orchestration__service__pb2


class JobSubServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateJob = channel.unary_unary(
            '/orchestration_service.JobSubService/CreateJob',
            request_serializer=orchestration__service__pb2.CreateJobRequest.SerializeToString,
            response_deserializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
        )
        self.AddTaskToJob = channel.unary_unary(
            '/orchestration_service.JobSubService/AddTaskToJob',
            request_serializer=orchestration__service__pb2.AddTaskToJobRequest.SerializeToString,
            response_deserializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
        )
        self.NotifyJob = channel.unary_unary(
            '/orchestration_service.JobSubService/NotifyJob',
            request_serializer=orchestration__service__pb2.NotifyJobRequest.SerializeToString,
            response_deserializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
        )


class JobSubServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddTaskToJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NotifyJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JobSubServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'CreateJob': grpc.unary_unary_rpc_method_handler(
            servicer.CreateJob,
            request_deserializer=orchestration__service__pb2.CreateJobRequest.FromString,
            response_serializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.SerializeToString,
        ),
        'AddTaskToJob': grpc.unary_unary_rpc_method_handler(
            servicer.AddTaskToJob,
            request_deserializer=orchestration__service__pb2.AddTaskToJobRequest.FromString,
            response_serializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.SerializeToString,
        ),
        'NotifyJob': grpc.unary_unary_rpc_method_handler(
            servicer.NotifyJob,
            request_deserializer=orchestration__service__pb2.NotifyJobRequest.FromString,
            response_serializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'orchestration_service.JobSubService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class JobSubService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateJob(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orchestration_service.JobSubService/CreateJob',
                                             orchestration__service__pb2.CreateJobRequest.SerializeToString,
                                             orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddTaskToJob(request,
                     target,
                     options=(),
                     channel_credentials=None,
                     call_credentials=None,
                     insecure=False,
                     compression=None,
                     wait_for_ready=None,
                     timeout=None,
                     metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orchestration_service.JobSubService/AddTaskToJob',
                                             orchestration__service__pb2.AddTaskToJobRequest.SerializeToString,
                                             orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NotifyJob(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orchestration_service.JobSubService/NotifyJob',
                                             orchestration__service__pb2.NotifyJobRequest.SerializeToString,
                                             orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class TaskSubServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TaskCompleted = channel.unary_unary(
            '/orchestration_service.TaskSubService/TaskCompleted',
            request_serializer=orchestration__service__pb2.TaskCompletedRequest.SerializeToString,
            response_deserializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
        )
        self.TaskError = channel.unary_unary(
            '/orchestration_service.TaskSubService/TaskError',
            request_serializer=orchestration__service__pb2.TaskErrorRequest.SerializeToString,
            response_deserializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
        )


class TaskSubServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TaskCompleted(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TaskError(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TaskSubServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'TaskCompleted': grpc.unary_unary_rpc_method_handler(
            servicer.TaskCompleted,
            request_deserializer=orchestration__service__pb2.TaskCompletedRequest.FromString,
            response_serializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.SerializeToString,
        ),
        'TaskError': grpc.unary_unary_rpc_method_handler(
            servicer.TaskError,
            request_deserializer=orchestration__service__pb2.TaskErrorRequest.FromString,
            response_serializer=orchestration__service__pb2.OrchestrationServiceAcknowledgement.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'orchestration_service.TaskSubService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class TaskSubService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TaskCompleted(request,
                      target,
                      options=(),
                      channel_credentials=None,
                      call_credentials=None,
                      insecure=False,
                      compression=None,
                      wait_for_ready=None,
                      timeout=None,
                      metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orchestration_service.TaskSubService/TaskCompleted',
                                             orchestration__service__pb2.TaskCompletedRequest.SerializeToString,
                                             orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TaskError(request,
                  target,
                  options=(),
                  channel_credentials=None,
                  call_credentials=None,
                  insecure=False,
                  compression=None,
                  wait_for_ready=None,
                  timeout=None,
                  metadata=None):
        return grpc.experimental.unary_unary(request, target, '/orchestration_service.TaskSubService/TaskError',
                                             orchestration__service__pb2.TaskErrorRequest.SerializeToString,
                                             orchestration__service__pb2.OrchestrationServiceAcknowledgement.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

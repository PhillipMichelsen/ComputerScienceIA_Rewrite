# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.generated.discovery_service_pb2 as discovery__service__pb2


class RegistrationStub(object):
    """Discovery Service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterService = channel.unary_unary(
            '/discovery_service.Registration/RegisterService',
            request_serializer=discovery__service__pb2.RegisterServiceRequest.SerializeToString,
            response_deserializer=discovery__service__pb2.RegisterServiceResponse.FromString,
        )
        self.DeregisterService = channel.unary_unary(
            '/discovery_service.Registration/DeregisterService',
            request_serializer=discovery__service__pb2.DeregisterServiceRequest.SerializeToString,
            response_deserializer=discovery__service__pb2.DeregisterServiceResponse.FromString,
        )


class RegistrationServicer(object):
    """Discovery Service
    """

    def RegisterService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeregisterService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistrationServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'RegisterService': grpc.unary_unary_rpc_method_handler(
            servicer.RegisterService,
            request_deserializer=discovery__service__pb2.RegisterServiceRequest.FromString,
            response_serializer=discovery__service__pb2.RegisterServiceResponse.SerializeToString,
        ),
        'DeregisterService': grpc.unary_unary_rpc_method_handler(
            servicer.DeregisterService,
            request_deserializer=discovery__service__pb2.DeregisterServiceRequest.FromString,
            response_serializer=discovery__service__pb2.DeregisterServiceResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'discovery_service.Registration', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Registration(object):
    """Discovery Service
    """

    @staticmethod
    def RegisterService(request,
                        target,
                        options=(),
                        channel_credentials=None,
                        call_credentials=None,
                        insecure=False,
                        compression=None,
                        wait_for_ready=None,
                        timeout=None,
                        metadata=None):
        return grpc.experimental.unary_unary(request, target, '/discovery_service.Registration/RegisterService',
                                             discovery__service__pb2.RegisterServiceRequest.SerializeToString,
                                             discovery__service__pb2.RegisterServiceResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeregisterService(request,
                          target,
                          options=(),
                          channel_credentials=None,
                          call_credentials=None,
                          insecure=False,
                          compression=None,
                          wait_for_ready=None,
                          timeout=None,
                          metadata=None):
        return grpc.experimental.unary_unary(request, target, '/discovery_service.Registration/DeregisterService',
                                             discovery__service__pb2.DeregisterServiceRequest.SerializeToString,
                                             discovery__service__pb2.DeregisterServiceResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class RetrievalStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetService = channel.unary_unary(
            '/discovery_service.Retrieval/GetService',
            request_serializer=discovery__service__pb2.GetServiceRequest.SerializeToString,
            response_deserializer=discovery__service__pb2.GetServiceResponse.FromString,
        )


class RetrievalServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RetrievalServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'GetService': grpc.unary_unary_rpc_method_handler(
            servicer.GetService,
            request_deserializer=discovery__service__pb2.GetServiceRequest.FromString,
            response_serializer=discovery__service__pb2.GetServiceResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'discovery_service.Retrieval', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Retrieval(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetService(request,
                   target,
                   options=(),
                   channel_credentials=None,
                   call_credentials=None,
                   insecure=False,
                   compression=None,
                   wait_for_ready=None,
                   timeout=None,
                   metadata=None):
        return grpc.experimental.unary_unary(request, target, '/discovery_service.Retrieval/GetService',
                                             discovery__service__pb2.GetServiceRequest.SerializeToString,
                                             discovery__service__pb2.GetServiceResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class HealthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HealthCheck = channel.unary_unary(
            '/discovery_service.Health/HealthCheck',
            request_serializer=discovery__service__pb2.HealthCheckRequest.SerializeToString,
            response_deserializer=discovery__service__pb2.HealthCheckResponse.FromString,
        )


class HealthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def HealthCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HealthServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'HealthCheck': grpc.unary_unary_rpc_method_handler(
            servicer.HealthCheck,
            request_deserializer=discovery__service__pb2.HealthCheckRequest.FromString,
            response_serializer=discovery__service__pb2.HealthCheckResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'discovery_service.Health', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Health(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def HealthCheck(request,
                    target,
                    options=(),
                    channel_credentials=None,
                    call_credentials=None,
                    insecure=False,
                    compression=None,
                    wait_for_ready=None,
                    timeout=None,
                    metadata=None):
        return grpc.experimental.unary_unary(request, target, '/discovery_service.Health/HealthCheck',
                                             discovery__service__pb2.HealthCheckRequest.SerializeToString,
                                             discovery__service__pb2.HealthCheckResponse.FromString,
                                             options, channel_credentials,
                                             insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
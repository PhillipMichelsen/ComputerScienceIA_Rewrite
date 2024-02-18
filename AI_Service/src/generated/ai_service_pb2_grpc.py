# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.generated.ai_service_pb2 as ai__service__pb2


class LLMAgentSubServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InvokeAgent = channel.unary_unary(
            "/ai_service.LLMAgentSubService/InvokeAgent",
            request_serializer=ai__service__pb2.AIServiceTaskRequest.SerializeToString,
            response_deserializer=ai__service__pb2.AIServiceAcknowledgement.FromString,
        )


class LLMAgentSubServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InvokeAgent(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_LLMAgentSubServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "InvokeAgent": grpc.unary_unary_rpc_method_handler(
            servicer.InvokeAgent,
            request_deserializer=ai__service__pb2.AIServiceTaskRequest.FromString,
            response_serializer=ai__service__pb2.AIServiceAcknowledgement.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "ai_service.LLMAgentSubService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class LLMAgentSubService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InvokeAgent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/ai_service.LLMAgentSubService/InvokeAgent",
            ai__service__pb2.AIServiceTaskRequest.SerializeToString,
            ai__service__pb2.AIServiceAcknowledgement.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

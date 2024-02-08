import grpc

from src.core.retrieval_handler import get_service
from src.generated import discovery_service_pb2_grpc, discovery_service_pb2


class RetrievalService(discovery_service_pb2_grpc.RetrievalServicer):
    def __init__(self, service_registry):
        self.service_registry = service_registry

    def GetService(self, request: discovery_service_pb2.GetServiceRequest, context: grpc.ServicerContext):
        try:
            response = get_service(
                request.service_type,
                self.service_registry,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return discovery_service_pb2.GetServiceResponse()

        return response

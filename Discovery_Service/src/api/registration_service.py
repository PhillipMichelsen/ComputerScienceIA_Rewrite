import grpc

from src.core.registration_handler import register_service, deregister_service
from src.generated import discovery_service_pb2_grpc, discovery_service_pb2


class RegistrationService(discovery_service_pb2_grpc.RegistrationServicer):
    def __init__(self, service_registry):
        self.service_registry = service_registry

    def RegisterService(self, request: discovery_service_pb2.RegisterServiceRequest, context: grpc.ServicerContext):
        try:
            response = register_service(
                request.service_type,
                request.service_address,
                request.service_port,
                self.service_registry,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return discovery_service_pb2.RegisterServiceResponse()

        return response

    def DeregisterService(self, request: discovery_service_pb2.DeregisterServiceRequest, context: grpc.ServicerContext):
        try:
            response = deregister_service(
                request.service_id,
                self.service_registry,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return discovery_service_pb2.RegisterServiceResponse()

        return response

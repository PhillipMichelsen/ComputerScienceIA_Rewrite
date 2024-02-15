import grpc

from src.generated import file_service_pb2, file_service_pb2_grpc


class GrpcServiceManager:
    def __init__(self):
        self.channels = {
            'FileService': grpc.insecure_channel('file-service:55001'),
        }

        self.service_info = {
            'FileService': {
                'stub_classes': {
                    'PresignedURLSubService': file_service_pb2_grpc.PresignedURLSubServiceStub,
                    'FileEmbeddingSubService': file_service_pb2_grpc.FileEmbeddingSubServiceStub,
                },
                'request_class': file_service_pb2.FileServiceTaskRequest,
            },
        }

        self.stubs_cache = {}

    def get_service_components(self, service_name, sub_service_name, method_name) -> tuple:
        if service_name not in self.service_info:
            raise ValueError(f"Service '{service_name}' is not defined.")

        service_config = self.service_info[service_name]

        if sub_service_name not in service_config['stub_classes']:
            raise ValueError(f"Sub service '{sub_service_name}' is not defined in service '{service_name}'.")

        stub_key = f"{service_name}_{sub_service_name}"
        if stub_key not in self.stubs_cache:
            stub_class = service_config['stub_classes'][sub_service_name]
            self.stubs_cache[stub_key] = stub_class(self.channels[service_name])

        stub = self.stubs_cache[stub_key]

        try:
            grpc_method = getattr(stub, method_name)
        except AttributeError:
            raise ValueError(
                f"Method '{method_name}' not found in subservice '{sub_service_name}' of service '{service_name}'.")

        request_class = service_config['request_class']

        return grpc_method, request_class

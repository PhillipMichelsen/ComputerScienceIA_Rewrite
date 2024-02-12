import grpc
from src.generated.file_service_pb2_grpc import PresignedURLSubServiceStub, FileEmbeddingSubServiceStub
from src.generated.file_service_pb2 import FileServiceTaskRequest


class GrpcServiceManager:
    def __init__(self):
        self.services = {
            'FileService': {
                'PresignedURLSubService': {
                    'stub': PresignedURLSubServiceStub,
                    'methods': {
                        'GetPresignedUploadURL': FileServiceTaskRequest,
                        'GetPresignedDownloadURL': FileServiceTaskRequest
                    }
                },
                'FileEmbeddingSubService': {
                    'stub': FileEmbeddingSubServiceStub,
                    'methods': {
                        'RegisterFile': FileServiceTaskRequest,
                        'GetFilesInfo': FileServiceTaskRequest,
                        'ProcessFile': FileServiceTaskRequest,
                        'RetrieveNearestNParagraphs': FileServiceTaskRequest,
                    }
                }
            }
        }

        self.channels = {
            'FileService': grpc.insecure_channel('file-service:50052')
        }

    def get_service_components(self, service_name, sub_service_name, method_name) -> tuple:
        """
        Provides the request class and callable for a given service and method.

        :param service_name: The name of the service.
        :param sub_service_name: The name of the sub-service.
        :param method_name: The name of the method.
        :return: A tuple of (request_class, grpc_method)
        """
        service = self.services.get(service_name, {})
        sub_service = service.get(sub_service_name, {})

        stub_class = sub_service.get('stub')
        request_class = sub_service.get('methods', {}).get(method_name)

        if not stub_class or not request_class:
            raise ValueError(f"Service/Method not found for {service_name}.{sub_service_name}.{method_name}")

        stub = stub_class(self.channels[service_name])
        grpc_method = getattr(stub, method_name, None)

        if not grpc_method:
            raise ValueError(f"Method {method_name} not found in service {service_name}")

        return request_class, grpc_method

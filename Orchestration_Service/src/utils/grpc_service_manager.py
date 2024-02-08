import grpc


class GrpcServiceManager:
    def __init__(self):
        # Define a mapping of services to their stub classes and request classes
        self.services = {
            #'FileService': {
            #    'stub': FileServiceStub,
            #    'methods': {
            #        'ProcessFile': ProcessFileRequest
            #    }
            #},
        }

        self.channels = {service: grpc.insecure_channel(f'{service}:8000')
                         for service in self.services}

    def get_service_components(self, service_name, method_name) -> tuple:
        """
        Provides the request class and callable for a given service and method.

        :param service_name: The name of the service.
        :param method_name: The name of the method.
        :return: A tuple of (request_class, grpc_method)
        """
        service = self.services.get(service_name, {})
        stub_class = service.get('stub')
        request_class = service.get('methods', {}).get(method_name)

        if not stub_class or not request_class:
            raise ValueError(f"Service/Method not found for {service_name}.{method_name}")

        stub = stub_class(self.channels[service_name])
        grpc_method = getattr(stub, method_name, None)

        if not grpc_method:
            raise ValueError(f"Method {method_name} not found in service {service_name}")

        return request_class, grpc_method

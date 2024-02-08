from src.generated.discovery_service_pb2 import GetServiceResponse


def get_service(service_type, service_registry) -> GetServiceResponse:
    service = service_registry.get_service(service_type)

    response = GetServiceResponse(
        service_host=service['service_host'],
        service_port=service['service_port'],
    )

    return response

from src.generated.discovery_service_pb2 import RegisterServiceResponse


def register_service(service_type, service_host, service_port, service_registry) -> RegisterServiceResponse:
    service_id = service_registry.register_service(service_type, service_host, service_port)

    response = RegisterServiceResponse(
        service_id=service_id
    )

    return response


def deregister_service(service_id, service_registry) -> RegisterServiceResponse:
    service_id = service_registry.deregister_service(service_id)

    response = RegisterServiceResponse(
        service_id=service_id
    )

    return response

import logging
from concurrent import futures

import grpc

from src.api.registration_service import RegistrationService
from src.api.retrieval_service import RetrievalService
from src.generated import discovery_service_pb2_grpc
from src.utils.service_registry import ServiceRegistry

service_registry = ServiceRegistry()
logging.basicConfig(level=logging.INFO)


def serve(port=8000):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    discovery_service_pb2_grpc.add_RegistrationServicer_to_server(RegistrationService(service_registry), server)
    discovery_service_pb2_grpc.add_RetrievalServicer_to_server(RetrievalService(service_registry), server)

    # Choose a port to run your server on, for example, 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"----- Server started on port {port} -----")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        logging.info("----- Server stopped -----")


if __name__ == '__main__':
    serve()

from concurrent import futures
import logging
import grpc

from src.generated import file_service_pb2_grpc
from src.api.presigned_url_sub_service import PresignedURLSubService
from src.utils.minio_client import MinioClient
from src.utils.dependency_manager import DependencyManager
from src.utils.orchestration_service_client import OrchestrationServiceClient
from src.utils.redis_client import WorkerRedisClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    file_service_pb2_grpc.add_PresignedURLSubServiceServicer_to_server(
        PresignedURLSubService(dependency_manager_instance),
        server
    )

    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info('----- Server started on port 50051 -----')

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    dependency_manager = DependencyManager()
    dependency_manager.add_dependency('worker_redis_client', WorkerRedisClient(db=1))
    dependency_manager.add_dependency('orchestration_service_client', OrchestrationServiceClient("orchestration_service:50051"))
    dependency_manager.add_dependency('minio_client', MinioClient(endpoint="minio:9000", access_key="minioadmin", secret_key="minioadmin"))

    serve(dependency_manager)

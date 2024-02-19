import logging
from concurrent import futures

import grpc

from src.api.file_embedding_sub_service import FileEmbeddingSubService
from src.api.presigned_url_sub_service import PresignedURLSubService
from src.generated import file_service_pb2_grpc
from src.repositories.file_repository import FileRepository
from src.repositories.redis_client import WorkerRedisClient
from src.repositories.weaviate_client import WeaviateClient
from src.utils.dependency_manager import DependencyManager
from src.utils.grobid_client import GrobidClient
from src.utils.minio_client import MinioClient
from src.utils.orchestration_service_client import OrchestrationServiceClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    file_service_pb2_grpc.add_PresignedURLSubServiceServicer_to_server(
        PresignedURLSubService(dependency_manager_instance), server
    )
    file_service_pb2_grpc.add_FileEmbeddingSubServiceServicer_to_server(
        FileEmbeddingSubService(dependency_manager_instance), server
    )

    server.add_insecure_port("[::]:55001")
    server.start()
    logging.info("----- Server started on port 55001 -----")

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s"
    )

    dependency_manager = DependencyManager()
    dependency_manager.add_dependency("worker_redis_client", WorkerRedisClient(db=1))
    dependency_manager.add_dependency(
        "orchestration_service_client",
        OrchestrationServiceClient("orchestration-service:55000"),
    )
    dependency_manager.add_dependency(
        "minio_client",
        MinioClient(
            endpoint="minio:9000", access_key="minioadmin", secret_key="minioadmin"
        ),
    )
    dependency_manager.add_dependency(
        "file_repository",
        FileRepository("postgresql://postgres:postgres@postgres/computer_science_ia"),
    )
    dependency_manager.add_dependency(
        "weaviate_client", WeaviateClient("weaviate", 8080, 50051)
    )
    dependency_manager.add_dependency(
        "grobid_client", GrobidClient("http://grobid:8070")
    )

    serve(dependency_manager)

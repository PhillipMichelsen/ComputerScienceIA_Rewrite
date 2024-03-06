import json
import logging
from io import BytesIO

from src.repositories.file_repository import FileRepository
from src.repositories.redis_client import WorkerRedisClient
from src.repositories.weaviate_client import WeaviateClient
from src.utils.dependency_manager import DependencyManager
from src.utils.grobid_client import GrobidClient
from src.utils.minio_client import MinioClient
from src.utils.orchestration_service_client import OrchestrationServiceClient


def register_file(task_id: str, job_id: str, dependency_manager: DependencyManager):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    file_repository: FileRepository = dependency_manager.get_dependency(
        "file_repository"
    )
    minio_client: MinioClient = dependency_manager.get_dependency("minio_client")

    object_key, bucket_name = worker_redis_client.get_job_data(
        job_id, ["object_key", "bucket_name"]
    )

    file_repository.add_file(
        file_name=object_key.split(".", 1)[1],
        uuid=object_key.split(".", 1)[0],
        bucket_name=bucket_name,
        paragraph_count=0,
        embedded_paragraph_count=0,
        status="pending",
    )

    orchestration_service_client.add_task_to_job(job_id, "ProcessFile")
    orchestration_service_client.task_completed(task_id)


def get_files_info(task_id: str, job_id: str, dependency_manager: DependencyManager):
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    file_repository: FileRepository = dependency_manager.get_dependency(
        "file_repository"
    )

    files = file_repository.get_all_files()
    files_info = [
        {
            "file_name": file.file_name,
            "uuid": file.uuid,
            "bucket_name": file.bucket_name,
            "paragraph_count": file.paragraph_count,
            "embedded_paragraph_count": file.embedded_paragraph_count,
            "status": file.status,
        }
        for file in files
    ]

    orchestration_service_client.notify_job(
        task_id,
        {
            "type": "RETURN",
            "files_info": json.dumps(files_info),
        },
    )

    orchestration_service_client.task_completed(task_id)


def process_file(task_id: str, job_id: str, dependency_manager: DependencyManager):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    minio_client: MinioClient = dependency_manager.get_dependency("minio_client")
    file_repository: FileRepository = dependency_manager.get_dependency(
        "file_repository"
    )
    grobid_client: GrobidClient = dependency_manager.get_dependency("grobid_client")
    weaviate_client: WeaviateClient = dependency_manager.get_dependency(
        "weaviate_client"
    )

    object_key, bucket_name = worker_redis_client.get_job_data(
        job_id, ["object_key", "bucket_name"]
    )
    file_name = object_key.split(".", 1)[1]

    file_tei = grobid_client.process_file(
        object_key, BytesIO(minio_client.get_object(bucket_name, object_key))
    )
    divisions = grobid_client.tei_to_divisions(file_tei)
    file_repository.set_paragraph_count_by_file_name(file_name, len(divisions))

    for idx, division in enumerate(divisions):
        weaviate_client.add_paragraph(
            text=division, object_key=object_key, bucket_name=bucket_name, position=idx
        )
        file_repository.increment_embedded_paragraph_count_by_file_name(file_name, 1)
        logging.debug(f"Added division {idx} to weaviate.")

    orchestration_service_client.task_completed(task_id)


def retrieve_nearest_n_paragraphs(
    task_id: str, job_id: str, dependency_manager: DependencyManager
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    weaviate_client: WeaviateClient = dependency_manager.get_dependency(
        "weaviate_client"
    )
    file_repository: FileRepository = dependency_manager.get_dependency(
        "file_repository"
    )

    search_concepts, move_towards_concepts, move_away_concepts = (
        worker_redis_client.get_job_data(
            job_id,
            ["search_concepts", "move_towards_concepts", "move_away_concepts"],
        )
    )

    similar_paragraphs = weaviate_client.search_similar_paragraphs(
        query_concepts=search_concepts.split("::"),
        move_towards_concepts=move_towards_concepts.split("::"),
        move_away_concepts=move_away_concepts.split("::"),
    )
    logging.debug(f"Retrieved similar paragraphs: {similar_paragraphs}")
    worker_redis_client.set_job_data_field(
        job_id, "similar_paragraphs", "::".join(similar_paragraphs)
    )
    orchestration_service_client.notify_job(
        task_id,
        {
            "type": "NOTIFICATION",
            "step": "RETRIEVAL",
            "status": "COMPLETED",
        },
    )

    orchestration_service_client.task_completed(task_id)

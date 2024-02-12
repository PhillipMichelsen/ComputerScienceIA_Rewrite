import logging
from uuid import uuid4

from src.utils.dependency_manager import DependencyManager
from src.utils.minio_client import MinioClient
from src.utils.orchestration_service_client import OrchestrationServiceClient
from src.utils.redis_client import WorkerRedisClient


def get_presigned_upload_url(task_id: str, job_id: str, dependency_manager: DependencyManager):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')
    orchestration_service_client: OrchestrationServiceClient = dependency_manager.get_dependency(
        'orchestration_service_client')
    minio_client: MinioClient = dependency_manager.get_dependency('minio_client')

    try:
        file_name = worker_redis_client.get_job_data(job_id, ['file_name'])[0]
    except Exception as e:
        orchestration_service_client.notify_job(
            task_id=task_id,
            notification={
                'type': 'ERROR',
                'message': str(e)
            }
        )
        logging.error(f"Error handling task {task_id}, no file_name found in job data.")
        return

    presigned_upload_url = minio_client.get_presigned_upload_url(
        uuid=str(uuid4()),
        bucket_name='test',
        file_name=file_name
    )

    orchestration_service_client.notify_job(
        task_id=task_id,
        notification={
            'type': 'RETURN',
            'presigned_upload_url': presigned_upload_url,
            'file_name': file_name
        }
    )

    orchestration_service_client.task_completed(task_id=task_id)


def get_presigned_download_url(task_id: str, job_id: str, dependency_manager: DependencyManager):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')
    orchestration_service_client: OrchestrationServiceClient = dependency_manager.get_dependency(
        'orchestration_service_client')
    minio_client: MinioClient = dependency_manager.get_dependency('minio_client')

    raise NotImplementedError("This method has not been implemented yet.")

import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from src.utils.dependency_manager import DependencyManager, get_dependency_manager
from src.utils.orchestration_service_client import OrchestrationServiceClient
from src.utils.pubsub_listener import RedisPubSubListener
from src.utils.redis_client import WorkerRedisClient

router = APIRouter()


@router.get("/get_presigned_upload_url")
def get_presigned_upload_url(
    file_name: str,
    dependency_manager: DependencyManager = Depends(get_dependency_manager),
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    redis_pubsub_listener: RedisPubSubListener = dependency_manager.get_dependency(
        "pubsub_listener"
    )
    service_id = dependency_manager.get_dependency("service_id")

    request_id = str(uuid4())
    logging.info(
        f"New get_presigned_upload_url request, creating GetPresignedUploadURL job, request_id: {request_id}"
    )

    redis_pubsub_listener.add_listener(request_id)

    try:
        orchestration_service_client.create_job(
            job_name="GetPresignedUploadURL",
            service_id=service_id,
            request_id=request_id,
            initial_job_data={"file_name": file_name},
        )

        queue = redis_pubsub_listener.get_queue(request_id)
        while True:
            try:
                message = queue.get(timeout=20)
                if message["type"] == "RETURN":
                    return message
                else:
                    logging.info(
                        f"Received non-final message: {message} for request_id: {request_id}"
                    )
            except Exception as e:
                logging.error(
                    f"Error processing message for request_id {request_id}: {e}"
                )
                raise HTTPException(
                    status_code=408, detail="Request timed out waiting for response."
                )
    finally:
        redis_pubsub_listener.remove_listener(request_id)


@router.post("/minio_notification")
def minio_notification(
    notification: dict,
    dependency_manager: DependencyManager = Depends(get_dependency_manager),
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    redis_pubsub_listener: RedisPubSubListener = dependency_manager.get_dependency(
        "pubsub_listener"
    )
    service_id = dependency_manager.get_dependency("service_id")

    request_id = str(uuid4())
    logging.info(
        f"New minio_notification request, creating FileUploaded job, request_id: {request_id}"
    )

    redis_pubsub_listener.add_listener(request_id)

    try:
        orchestration_service_client.create_job(
            job_name="FileUploaded",
            service_id=service_id,
            request_id=request_id,
            initial_job_data={
                "object_key": notification["Records"][0]["s3"]["object"]["key"],
                "bucket_name": notification["Records"][0]["s3"]["bucket"]["name"],
            },
        )
    finally:
        redis_pubsub_listener.remove_listener(request_id)
        return {"status": "ok"}


@router.get("/get_files_info")
def get_files_info(
    dependency_manager: DependencyManager = Depends(get_dependency_manager),
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    redis_pubsub_listener: RedisPubSubListener = dependency_manager.get_dependency(
        "pubsub_listener"
    )
    service_id = dependency_manager.get_dependency("service_id")

    request_id = str(uuid4())
    logging.info(
        f"New get_files_info request, creating GetFilesInfo job, request_id: {request_id}"
    )

    redis_pubsub_listener.add_listener(request_id)

    try:
        orchestration_service_client.create_job(
            job_name="GetFilesInfo",
            service_id=service_id,
            request_id=request_id,
            initial_job_data={},
        )

        queue = redis_pubsub_listener.get_queue(request_id)
        while True:
            try:
                message = queue.get(timeout=20)
                if message["type"] == "RETURN":
                    return message
                else:
                    logging.info(
                        f"Received non-final message: {message} for request_id: {request_id}"
                    )
            except Exception as e:
                logging.error(
                    f"Error processing message for request_id {request_id}: {e}"
                )
                raise HTTPException(
                    status_code=408, detail="Request timed out waiting for response."
                )
    finally:
        redis_pubsub_listener.remove_listener(request_id)

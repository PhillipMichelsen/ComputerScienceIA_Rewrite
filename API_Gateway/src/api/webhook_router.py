import json

from fastapi import WebSocket, Depends, WebSocketDisconnect, APIRouter
from uuid import uuid4
import logging
from src.utils.dependency_manager import DependencyManager, get_dependency_manager
from src.utils.orchestration_service_client import OrchestrationServiceClient
from src.utils.pubsub_listener import RedisPubSubListener
from src.utils.redis_client import WorkerRedisClient

router = APIRouter()


@router.websocket("/ws/test_endpoint")
async def websocket_endpoint(
    websocket: WebSocket,
    dependency_manager: DependencyManager = Depends(get_dependency_manager),
):
    await websocket.accept()

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

    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            user_input = parsed_data.get("user_input")

            request_id = str(uuid4())

            redis_pubsub_listener.add_listener(request_id)

            try:
                orchestration_service_client.create_job(
                    job_name="RespondToQuery",
                    service_id=service_id,
                    request_id=request_id,
                    initial_job_data={"user_input": user_input},
                )

                queue = redis_pubsub_listener.get_queue(request_id)
                while True:
                    try:
                        message = queue.get(timeout=50)
                        await websocket.send_json(message)
                    except Exception as e:
                        logging.error(
                            f"Error processing message for request_id {request_id}: {e}"
                        )
                        await websocket.close(code=1011)
                        return
            finally:
                redis_pubsub_listener.remove_listener(request_id)

    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")

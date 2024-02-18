import logging
import os
from concurrent import futures

import dotenv
import grpc

from src.api.llm_agent_sub_service import LLMAgentSubService
from src.generated import ai_service_pb2_grpc
from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.orchestration_service_client import OrchestrationServiceClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    ai_service_pb2_grpc.add_LLMAgentSubServiceServicer_to_server(
        LLMAgentSubService(dependency_manager_instance), server
    )

    server.add_insecure_port("[::]:55002")
    server.start()
    logging.info("----- Server started on port 55002 -----")

    server.wait_for_termination()


if __name__ == "__main__":
    dotenv.load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
    )

    dependency_manager = DependencyManager()
    dependency_manager.add_dependency("worker_redis_client", WorkerRedisClient(db=1))
    dependency_manager.add_dependency(
        "orchestration_service_client",
        OrchestrationServiceClient("orchestration-service:55000"),
    )

    serve(dependency_manager)

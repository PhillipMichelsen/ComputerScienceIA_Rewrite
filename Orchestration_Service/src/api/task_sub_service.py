import logging
import threading

import grpc

from src.core.task_sub_service_handler import task_completed, task_error
from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class TaskSubService(orchestration_service_pb2_grpc.TaskSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def TaskCompleted(self, request, context):
        try:
            thread = threading.Thread(
                target=task_completed,
                args=(
                    request.task_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Received a task_completed request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received a task_completed request but had error: {e}")
            return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=False)

        return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=True)

    def TaskError(self, request, context):
        try:
            thread = threading.Thread(
                target=task_error,
                args=(
                    request.task_id,
                    request.error_message,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Received a task_error request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received a task_error request but had error: {e}")
            return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=False)

        return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=True)

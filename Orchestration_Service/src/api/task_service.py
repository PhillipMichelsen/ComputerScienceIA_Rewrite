import grpc
import threading

from src.core.task_service_handler import task_completed, task_error
from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager
import logging


class TaskService(orchestration_service_pb2_grpc.TaskServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def TaskCompleted(self, request, context):
        logging.debug(f"Received a task_completed request: {request}")
        try:
            thread = threading.Thread(
                target=task_completed,
                args=(
                    request.task_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started task_completed successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing task_completed: {e}")
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def TaskError(self, request, context):
        logging.debug(f"Received a task_error request: {request}")
        try:
            thread = threading.Thread(
                target=task_error,
                args=(
                    request.task_id,
                    request.error_message,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started task_error successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing task_error: {e}")
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

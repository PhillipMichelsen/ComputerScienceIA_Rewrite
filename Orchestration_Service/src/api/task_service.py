import grpc
import threading

from src.core.task_service_handler import task_completed, task_error
from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class TaskService(orchestration_service_pb2_grpc.TaskServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def TaskCompleted(self, request, context):
        try:
            thread = threading.Thread(
                target=task_completed,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def TaskError(self, request, context):
        try:
            thread = threading.Thread(
                target=task_error,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

import grpc
import threading

from src.utils.dependency_manager import DependencyManager

from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.core.job_service_handler import create_job, add_task_to_job, notify_job


class JobService(orchestration_service_pb2_grpc.JobServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def CreateJob(self, request, context):
        try:
            thread = threading.Thread(
                target=create_job,
                args=(
                    request.job_name,
                    request.notification_endpoint,
                    request.initial_job_data,
                    self.dependency_manager
                ))
            thread.start()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def AddTaskToJob(self, request, context):
        try:
            thread = threading.Thread(
                target=add_task_to_job,
                args=(
                    request.job_id,
                    request.task_name,
                    self.dependency_manager
                ))
            thread.start()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def NotifyJob(self, request, context):
        try:
            thread = threading.Thread(
                target=notify_job,
                args=(
                    request.task_id,
                    request.job_id,
                    request.notification,
                    self.dependency_manager
                ))
            thread.start()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

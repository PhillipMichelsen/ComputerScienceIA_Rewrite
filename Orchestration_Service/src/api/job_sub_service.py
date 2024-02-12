import logging
import threading

import grpc

from src.core.job_sub_service_handler import create_job, add_task_to_job, notify_job
from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class JobSubService(orchestration_service_pb2_grpc.JobSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def CreateJob(self, request, context):
        try:
            thread = threading.Thread(
                target=create_job,
                args=(
                    request.job_name,
                    request.request_id,
                    request.initial_job_data,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received create_job request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received create_job request but had error: {e}")
            return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=False)

        return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=True)

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
            logging.debug(f"Received add_task_to_job request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received add_task_to_job request but had error: {e}")
            return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=False)

        return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=True)

    def NotifyJob(self, request, context):
        try:
            thread = threading.Thread(
                target=notify_job,
                args=(
                    request.task_id,
                    request.notification,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Received notify_job request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received notify_job request but had error: {e}")
            return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=False)

        return orchestration_service_pb2.OrchestrationServiceAcknowledgement(success=True)

import grpc
import threading
import logging

from src.utils.dependency_manager import DependencyManager

from src.generated import orchestration_service_pb2, orchestration_service_pb2_grpc
from src.core.job_service_handler import create_job, add_task_to_job, notify_job


class JobService(orchestration_service_pb2_grpc.JobServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def CreateJob(self, request, context):
        logging.debug(f"Received a create_job request: {request}")
        try:
            thread = threading.Thread(
                target=create_job,
                args=(
                    request.job_name,
                    request.service_id,
                    request.initial_job_data,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started create_job successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing create_job: {e}")
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def AddTaskToJob(self, request, context):
        logging.debug(f"Received an add_task_to_job request: {request}")
        try:
            thread = threading.Thread(
                target=add_task_to_job,
                args=(
                    request.job_id,
                    request.task_name,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started add_task_to_job successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing add_task_to_job: {e}")
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

    def NotifyJob(self, request, context):
        logging.debug(f"Received a notify_job request: {request}")
        try:
            thread = threading.Thread(
                target=notify_job,
                args=(
                    request.task_id,
                    request.notification,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started notify_job successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing notify_job: {e}")
            return orchestration_service_pb2.Acknowledgement(success=False)

        return orchestration_service_pb2.Acknowledgement(success=True)

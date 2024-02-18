import logging

import grpc

from src.generated.orchestration_service_pb2 import (
    CreateJobRequest,
    AddTaskToJobRequest,
    NotifyJobRequest,
    TaskCompletedRequest,
    TaskErrorRequest,
)
from src.generated.orchestration_service_pb2_grpc import (
    JobSubServiceStub,
    TaskSubServiceStub,
)


class OrchestrationServiceClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.job_stub = JobSubServiceStub(self.channel)
        self.task_stub = TaskSubServiceStub(self.channel)

    def create_job(self, job_name, request_id, initial_job_data):
        request = CreateJobRequest(
            job_name=job_name, request_id=request_id, initial_job_data=initial_job_data
        )
        logging.debug(
            f"Sending create job request, job: {job_name}, request_id: {request_id}"
        )
        return self.job_stub.CreateJob(request)

    def add_task_to_job(self, job_id: str, task_name: str):
        request = AddTaskToJobRequest(job_id=job_id, task_name=task_name)
        logging.debug(
            f"Sending add task to job request, job_id: {job_id}, task_name: {task_name}"
        )
        return self.job_stub.AddTaskToJob(request)

    def notify_job(self, task_id: str, notification: dict):
        request = NotifyJobRequest(task_id=task_id, notification=notification)
        logging.debug(f"Sending notify job request, task_id: {task_id}")
        return self.job_stub.NotifyJob(request)

    def task_completed(self, task_id: str):
        request = TaskCompletedRequest(task_id=task_id)
        logging.debug(f"Sending task completed request, task_id: {task_id}")
        return self.task_stub.TaskCompleted(request)

    def task_error(self, task_id: str, error_message: str):
        request = TaskErrorRequest(task_id=task_id, error_message=error_message)
        logging.debug(
            f"Sending task error request, task_id: {task_id}, error_message: {error_message}"
        )
        return self.task_stub.TaskError(request)

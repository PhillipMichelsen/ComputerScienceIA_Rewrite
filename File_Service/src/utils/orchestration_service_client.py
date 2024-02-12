import grpc
from src.generated.orchestration_service_pb2_grpc import JobSubServiceStub, TaskSubServiceStub
from src.generated.orchestration_service_pb2 import (
    CreateJobRequest,
    AddTaskToJobRequest,
    NotifyJobRequest,
    TaskCompletedRequest,
    TaskErrorRequest
)


class OrchestrationServiceClient:
    def __init__(self, server_address):
        self.channel = grpc.insecure_channel(server_address)
        self.job_stub = JobSubServiceStub(self.channel)
        self.task_stub = TaskSubServiceStub(self.channel)

    def create_job(self, job_name, service_id, initial_job_data):
        request = CreateJobRequest(job_name=job_name, service_id=service_id, initial_job_data=initial_job_data)
        return self.job_stub.CreateJob(request)

    def add_task_to_job(self, job_id, task_name):
        request = AddTaskToJobRequest(job_id=job_id, task_name=task_name)
        return self.job_stub.AddTaskToJob(request)

    def notify_job(self, task_id, notification):
        request = NotifyJobRequest(task_id=task_id, notification=notification)
        return self.job_stub.NotifyJob(request)

    def task_completed(self, task_id):
        request = TaskCompletedRequest(task_id=task_id)
        return self.task_stub.TaskCompleted(request)

    def task_error(self, task_id, error_message):
        request = TaskErrorRequest(task_id=task_id, error_message=error_message)
        return self.task_stub.TaskError(request)

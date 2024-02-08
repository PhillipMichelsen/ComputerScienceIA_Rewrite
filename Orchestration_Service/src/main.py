from concurrent import futures
import yaml

import grpc

from src.api.job_service import JobService
from src.api.task_service import TaskService
from src.generated import orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestration_service_pb2_grpc.add_JobServiceServicer_to_server(JobService(dependency_manager_instance), server)
    orchestration_service_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(dependency_manager_instance), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    dependency_manager = DependencyManager()
    dependency_manager.add_dependency('manager_redis_client', ManagerRedisClient())
    dependency_manager.add_dependency('grpc_service_manager', GrpcServiceManager())
    dependency_manager.add_dependency('jobs_yaml', yaml.safe_load(open('jobs.yaml')))
    dependency_manager.add_dependency('tasks_yaml', yaml.safe_load(open('tasks.yaml')))

    serve(dependency_manager)

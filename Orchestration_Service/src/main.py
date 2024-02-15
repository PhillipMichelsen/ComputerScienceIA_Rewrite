import logging
from concurrent import futures

import grpc
import yaml

from src.api.job_sub_service import JobSubService
from src.api.task_sub_service import TaskSubService
from src.generated import orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestration_service_pb2_grpc.add_JobSubServiceServicer_to_server(
        JobSubService(dependency_manager_instance),
        server
    )
    orchestration_service_pb2_grpc.add_TaskSubServiceServicer_to_server(
        TaskSubService(dependency_manager_instance),
        server
    )

    server.add_insecure_port('[::]:55000')
    server.start()
    logging.info('----- Server started on port 55000 -----')

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    dependency_manager = DependencyManager()
    dependency_manager.add_dependency('manager_redis_client', ManagerRedisClient(db=0))
    dependency_manager.add_dependency('worker_redis_client', WorkerRedisClient(db=1))
    dependency_manager.add_dependency('grpc_service_manager', GrpcServiceManager())
    dependency_manager.add_dependency('jobs_yaml', yaml.safe_load(open('src/jobs.yaml')))
    dependency_manager.add_dependency('tasks_yaml', yaml.safe_load(open('src/tasks.yaml')))

    serve(dependency_manager)

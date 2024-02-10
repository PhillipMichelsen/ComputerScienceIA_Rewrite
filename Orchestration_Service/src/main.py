from concurrent import futures
import yaml
import logging
import grpc

from src.api.job_service import JobService
from src.api.task_service import TaskService
from src.generated import orchestration_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient


def serve(dependency_manager_instance: DependencyManager):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orchestration_service_pb2_grpc.add_JobServiceServicer_to_server(JobService(dependency_manager_instance), server)
    orchestration_service_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(dependency_manager_instance), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info('----- Server started on port 50051 -----')

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

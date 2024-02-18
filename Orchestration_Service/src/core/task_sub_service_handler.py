import logging

from src.core.task_manager import dispatch_task, terminate_job
from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient


def task_completed(task_id: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')
    grpc_service_manager: GrpcServiceManager = dependency_manager.get_dependency('grpc_service_manager')
    tasks_yaml: dict = dependency_manager.get_dependency('tasks_yaml')

    job_id = manager_redis_client.get_task_metadata(task_id, ['job_id'])[0]
    manager_redis_client.set_task_metadata(task_id, {'status': 'Completed'})

    next_task_id = manager_redis_client.dequeue_task_chain(job_id)

    if next_task_id:
        dispatch_task(next_task_id, job_id, dependency_manager)

    else:
        terminate_job(job_id, dependency_manager)


def task_error(task_id: str, error_message: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')

    job_id = manager_redis_client.get_task_metadata(task_id, ['job_id'])[0]
    terminate_job(job_id, dependency_manager)
    logging.error(f"Terminating job of job_id: {job_id} as task of tsk_id: {task_id} had error: {error_message}")

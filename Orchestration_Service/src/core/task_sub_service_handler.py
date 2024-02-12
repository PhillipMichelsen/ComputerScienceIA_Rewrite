import logging

from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient


def task_completed(task_id: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')
    grpc_service_manager: GrpcServiceManager = dependency_manager.get_dependency('grpc_service_manager')
    tasks_yaml: dict = dependency_manager.get_dependency('tasks_yaml')

    job_id = manager_redis_client.get_task_metadata(task_id, ['job_id'])[0]
    next_task_id = manager_redis_client.dequeue_task_chain(job_id)

    if next_task_id:
        next_task_name = manager_redis_client.get_task_metadata(next_task_id, ['task_name'])[0]
        method_signature = tasks_yaml.get(next_task_name, {}).get('signature')
        service_name, sub_service_name, method_name = method_signature.split('.')

        grpc_method, request_class = grpc_service_manager.get_service_components(
            service_name,
            sub_service_name,
            method_name
        )

        request = request_class(
            task_id=next_task_id,
            job_id=job_id
        )

        response = grpc_method(request)

        if response.success:
            pass

        logging.debug(f"Next task dispatched for job_id {job_id}... Task ID: {next_task_id}")

    else:
        task_chain = manager_redis_client.get_job_metadata(job_id, ['task_chain'])[0]
        task_chain = task_chain.split(',')

        for task_id in task_chain:
            manager_redis_client.delete_task_metadata(task_id)

        manager_redis_client.delete_job_metadata(job_id)
        worker_redis_client.delete_job_data(job_id)

        logging.debug(f"Job ID: {job_id} completed successfully... Job terminated gracefully.")


def task_error(task_id: str, error_message: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')

    job_id = manager_redis_client.get_task_metadata(task_id, ['job_id'])[0]
    task_chain = manager_redis_client.get_job_metadata(job_id, ['task_chain'])[0]
    task_chain = task_chain.split(',')

    for task_id in task_chain:
        manager_redis_client.delete_task_metadata(task_id)

    manager_redis_client.delete_job_metadata(job_id)
    worker_redis_client.delete_job_data(job_id)
    logging.error(f'{error_message}, Job ID: {job_id}, Task ID: {task_id}... Job terminated gracefully.')

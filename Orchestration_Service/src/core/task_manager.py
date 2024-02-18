import logging

from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient


def dispatch_task(task_id: str, job_id: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    grpc_service_manager: GrpcServiceManager = dependency_manager.get_dependency('grpc_service_manager')
    tasks_yaml: dict = dependency_manager.get_dependency('tasks_yaml')

    task_name = manager_redis_client.get_task_metadata(task_id, ['task_name'])[0]
    method_signature = tasks_yaml.get(task_name, {}).get('signature')
    service_name, sub_service_name, method_name = method_signature.split('.')

    grpc_method, request_class = grpc_service_manager.get_service_components(
        service_name,
        sub_service_name,
        method_name
    )

    request = request_class(
        task_id=task_id,
        job_id=job_id
    )

    response = grpc_method(request)

    if response.success:
        manager_redis_client.set_task_metadata(task_id, {'status': 'Sent'})

    logging.debug(f"Next task dispatched for job_id {job_id}... Task ID: {task_id}")


def terminate_job(job_id: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')

    manager_redis_client.set_job_metadata(job_id, {'status': 'Completed, Terminating...'})

    task_chain = manager_redis_client.get_job_metadata(job_id, ['task_chain'])[0]
    task_chain = task_chain.split(',')

    for task_id in task_chain:
        manager_redis_client.delete_task_metadata(task_id)

    manager_redis_client.delete_job_metadata(job_id)
    worker_redis_client.delete_job_data(job_id)
    logging.debug(f"Job ID: {job_id} terminated gracefully...")

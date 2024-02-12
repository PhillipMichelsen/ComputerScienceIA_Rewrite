import logging
from uuid import uuid4

from src.utils.dependency_manager import DependencyManager
from src.utils.grpc_service_manager import GrpcServiceManager
from src.utils.redis_client import ManagerRedisClient, WorkerRedisClient
from src.core.task_manager import dispatch_task


def create_job(job_name: str, service_id: str, request_id: str, initial_job_data: dict, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')
    grpc_service_manager: GrpcServiceManager = dependency_manager.get_dependency('grpc_service_manager')
    jobs_yaml: dict = dependency_manager.get_dependency('jobs_yaml')
    tasks_yaml: dict = dependency_manager.get_dependency('tasks_yaml')

    job_id = str(uuid4())
    job_metadata = {
        'job_name': job_name,
        'service_id': service_id,
        'request_id': request_id,
        'task_chain': '',
        'status': 'Created'
    }

    tasks = jobs_yaml.get(job_name, [])

    for task in tasks:
        task_id = str(uuid4())
        task_metadata = {
            'task_name': task,
            'job_id': job_id,
            'method_signature': tasks_yaml.get(task, {}).get('signature'),
            'status': 'Created'
        }
        manager_redis_client.set_task_metadata(task_id, task_metadata)
        manager_redis_client.enqueue_task_chain(job_id, task_id)
        job_metadata['task_chain'] += task_id + ','

    job_metadata['task_chain'] = job_metadata['task_chain'][:-1]

    manager_redis_client.set_job_metadata(job_id, job_metadata)
    worker_redis_client.set_job_data(job_id, initial_job_data)
    logging.debug(f"Created job {job_name} with job_id: {job_id}")

    dispatch_task(manager_redis_client.dequeue_task_chain(job_id), job_id, dependency_manager)


def add_task_to_job(job_id: str, task_name: str, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    tasks_yaml: dict = dependency_manager.get_dependency('tasks_yaml')

    task_id = str(uuid4())
    task_metadata = {
        'task_name': task_name,
        'job_id': job_id,
        'task_signature': tasks_yaml.get(task_name, {}).get('signature'),
        'status': 'Created'
    }
    manager_redis_client.set_task_metadata(task_id, task_metadata)
    manager_redis_client.enqueue_task_chain(job_id, task_id)

    task_chain = manager_redis_client.get_job_metadata(job_id, ['task_chain'])[0]
    manager_redis_client.set_job_metadata(job_id, {'task_chain': task_chain + ',' + task_id})


def notify_job(task_id: str, notification: dict, dependency_manager: DependencyManager):
    manager_redis_client: ManagerRedisClient = dependency_manager.get_dependency('manager_redis_client')
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency('worker_redis_client')

    job_id = manager_redis_client.get_task_metadata(task_id, ['job_id'])[0]
    service_id = manager_redis_client.get_job_metadata(job_id, ['service_id'])[0]
    request_id = manager_redis_client.get_job_metadata(job_id, ['request_id'])[0]

    worker_redis_client.publish_request_notification(service_id, request_id, dict(notification))
    logging.debug(f"Notification published for request_id: {request_id} to service_id: {service_id}...")

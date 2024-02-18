from uuid import uuid4

from src.utils.orchestration_service_client import OrchestrationServiceClient
from src.utils.pubsub_listener import RedisPubSubListener
from src.utils.redis_client import WorkerRedisClient


class DependencyManager:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, name, dependency):
        self.dependencies[name] = dependency

    def get_dependency(self, name):
        return self.dependencies[name]

    def get_dependencies(self):
        return self.dependencies


dependency_manager = DependencyManager()
dependency_manager.add_dependency('service_id', str(uuid4()))
dependency_manager.add_dependency('worker_redis_client', WorkerRedisClient(db=1))

dependency_manager.add_dependency(
    'orchestration_service_client',
    OrchestrationServiceClient("orchestration-service:55000")
)

dependency_manager.add_dependency('pubsub_listener',
                                  RedisPubSubListener(
                                      dependency_manager.get_dependency('worker_redis_client').client,
                                      dependency_manager.get_dependency('service_id')
                                  )
                                  )


def get_dependency_manager():
    return dependency_manager

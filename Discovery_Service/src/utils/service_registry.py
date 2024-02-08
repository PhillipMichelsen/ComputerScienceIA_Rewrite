from threading import Lock
from uuid import uuid4


class ServiceRegistry:
    """
    A simple service registry that stores services by type and id. The registry is thread-safe.
    """

    def __init__(self):
        self.services = {}
        self.lock = Lock()

    def _is_service_conflict(self, service_host: str, service_port: str) -> bool:
        """
        Checks if a service with the same host and port is already registered.

        :param service_host:
        :param service_port:
        :return: True if a service with the same host and port is already registered, False otherwise
        """
        for service_type in self.services:
            for service_id in self.services[service_type]:
                service = self.services[service_type][service_id]
                if service['service_host'] == service_host and service['service_port'] == service_port:
                    return True

        return False

    def register_service(self, service_type: str, service_host: str, service_port: str) -> str:
        """
        Registers a service with the given type, host and port.

        :param service_type:
        :param service_host:
        :param service_port:
        :return: The service id
        """
        with self.lock:
            service_id = str(uuid4())

            if self._is_service_conflict(service_host, service_port):
                raise Exception('Service with the same host and port already registered')

            if service_type not in self.services:
                self.services[service_type] = {}

            self.services[service_type][service_id] = {
                'service_host': service_host,
                'service_port': service_port
            }

            return service_id

    def deregister_service(self, service_id: str) -> str:
        """
        Deregisters the service with the given id. Returns the service id.

        :param service_id:
        :return: The service id
        """
        with self.lock:
            for service_type in self.services:
                if service_id in self.services[service_type]:
                    del self.services[service_type][service_id]
                    return service_id

            raise Exception(f'Service with id {service_id} not found')

    def get_service(self, service_type: str) -> dict:
        """
        Returns a service of the given type.

        :param service_type:
        :return: A service's host and port
        """
        # TODO: Implement load balancing/round robin
        # No lock needed because this is a read-only operation

        if service_type not in self.services:
            raise Exception(f'Service type {service_type} not found')

        for service_id in self.services[service_type]:
            return self.services[service_type][service_id]

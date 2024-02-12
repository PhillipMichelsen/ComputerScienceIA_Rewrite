import json
import logging
import threading
from queue import Queue

import redis


class RedisPubSubListener:
    def __init__(self, redis_client, service_id):
        self.redis_client: redis.Redis = redis_client
        self.listeners = {}
        self.pubsub = self.redis_client.pubsub()

        self.pubsub.subscribe(f"{service_id}:ServiceRequestNotification")
        self.thread = threading.Thread(target=self.listen_to_redis, daemon=True)
        self.thread.start()

    def add_listener(self, request_id):
        if request_id not in self.listeners:
            self.listeners[request_id] = Queue()
            logging.info(f"Listening for: {request_id}")

    def remove_listener(self, request_id):
        if request_id in self.listeners:
            del self.listeners[request_id]
            logging.info(f"Removed listener for: {request_id}")

    def get_queue(self, request_id):
        return self.listeners.get(request_id)

    def listen_to_redis(self):
        for message in self.pubsub.listen():
            logging.info(message)
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data['request_id'] in self.listeners:
                    self.listeners[data['request_id']].put(data)
                    logging.debug(f"Placed message in queue for request_id: {data['request_id']}")

import json
import logging
import threading
from queue import Queue


class RedisPubSubListener:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.listeners = {}
        self.pubsub = self.redis_client.pubsub()
        self.thread = threading.Thread(target=self.listen_to_redis, daemon=True)
        self.thread.start()

    def add_listener(self, request_id):
        request_id_queue = f"{request_id}:RequestNotification"
        if request_id_queue not in self.listeners:
            self.listeners[request_id_queue] = Queue()
            self.pubsub.subscribe(request_id_queue)
            logging.debug(f"Subscribed to channel: {request_id_queue}")

    def remove_listener(self, request_id):
        request_id_queue = f"{request_id}:RequestNotification"
        if request_id_queue in self.listeners:
            del self.listeners[request_id_queue]
            self.pubsub.unsubscribe(f"{request_id_queue}:RequestNotification")
            logging.debug(f"Unsubscribed from channel: {request_id_queue}")

    def get_queue(self, request_id):
        return self.listeners.get(f"{request_id}:RequestNotification")

    def listen_to_redis(self):
        while True:
            message = self.pubsub.get_message()
            if message and message['type'] == 'message':
                channel = message['channel']
                if channel in self.listeners:
                    try:
                        data = json.loads(message['data'])
                        self.listeners[channel].put(data)
                        logging.debug(f"Message received on {channel}: {data}")
                    except json.JSONDecodeError as e:
                        logging.error(f"Error decoding message: {e}")

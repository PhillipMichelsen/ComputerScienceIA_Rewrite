import redis
import json
import logging


class BaseRedisClient:
    def __init__(self, host='redis', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

        try:
            self.client.ping()
            logging.debug(f"Connected to {host}:{port} on db {db}!")
        except redis.exceptions.ConnectionError:
            logging.error(f"Could not connect to {host}:{port} on db {db} :(")
            raise Exception("Redis server not available :(")


class WorkerRedisClient(BaseRedisClient):
    def set_job_data(self, job_id: str, data: dict):
        self.client.hset(f"{job_id}:JobData", mapping=data)

    def set_job_data_field(self, job_id: str, field: str, value: str):
        self.client.hset(f"{job_id}:JobData", field, value)

# Q:
    def get_job_data(self, job_id: str, fields: list = None):
        if fields:
            return self.client.hmget(f"{job_id}:JobData", fields)
        else:
            return self.client.hgetall(job_id)

    def delete_job_data(self, job_id: str):
        self.client.delete(f"{job_id}:JobData")

    def publish_service_notification(self, service_id: str, notification: dict):
        notification_json = json.dumps(notification)
        notification_bytes = notification_json.encode('utf-8')

        self.client.publish(f"{service_id}:ServiceNotification", notification_bytes)

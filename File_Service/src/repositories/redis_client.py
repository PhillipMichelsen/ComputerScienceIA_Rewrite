import json
import logging

import redis


class BaseRedisClient:
    def __init__(self, host='redis', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

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

    def get_job_data(self, job_id: str, fields: list = None):
        if fields:
            return self.client.hmget(f"{job_id}:JobData", fields)
        else:
            return self.client.hgetall(job_id)

    def delete_job_data(self, job_id: str):
        self.client.delete(f"{job_id}:JobData")

    def publish_request_notification(self, service_id: str, request_id: str, notification: dict):
        notification['request_id'] = request_id
        notification_json = json.dumps(notification)
        notification_bytes = notification_json.encode('utf-8')

        self.client.publish(f"{service_id}:ServiceRequestNotification", notification_bytes)

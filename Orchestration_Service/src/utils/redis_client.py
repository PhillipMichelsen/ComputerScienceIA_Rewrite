import redis


class BaseRedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)


class ManagerRedisClient(BaseRedisClient):
    def set_job_metadata(self, job_id: str, metadata: dict):
        self.client.hset(f"{job_id}:JobMetadata", mapping=metadata)

    def set_job_metadata_field(self, job_id: str, field: str, value: str):
        self.client.hset(f"{job_id}:JobMetadata", field, value)

    def get_job_metadata(self, job_id: str, fields: list = None):
        if fields:
            return self.client.hmget(f"{job_id}:JobMetadata", fields)
        else:
            return self.client.hgetall(job_id)

    def delete_job_metadata(self, job_id: str):
        self.client.delete(f"{job_id}:JobMetadata")

    def set_task_metadata(self, task_id: str, metadata: dict):
        self.client.hset(f"{task_id}:TaskMetadata", mapping=metadata)

    def set_task_metadata_field(self, task_id: str, field: str, value: str):
        self.client.hset(f"{task_id}:TaskMetadata", field, value)

    def get_task_metadata(self, task_id: str, fields: list = None):
        if fields:
            return self.client.hmget(f"{task_id}:TaskMetadata", fields)
        else:
            return self.client.hgetall(task_id)

    def delete_task_metadata(self, task_id: str):
        self.client.delete(f"{task_id}:TaskMetadata")

    def enqueue_task_chain(self, job_id: str, task_id: str):
        self.client.lpush(f"{job_id}:TaskChain", task_id)

    def dequeue_task_chain(self, job_id: str):
        return self.client.rpop(f"{job_id}:TaskChain")


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

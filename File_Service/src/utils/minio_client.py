import minio
from minio.notificationconfig import NotificationConfig, QueueConfig


class MinioClient:
    def __init__(self, endpoint, access_key, secret_key):
        self.minio = minio.Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False,
        )

        if not self.minio.bucket_exists("test"):
            self.minio.make_bucket("test")

        self.minio.set_bucket_notification(
            "test",
            NotificationConfig(
                queue_config_list=[
                    QueueConfig(
                        queue="arn:minio:sqs::_:webhook",
                        events=["s3:ObjectCreated:*"]
                    )
                ]
            )
        )

    def get_presigned_upload_url(self, uuid: str, bucket_name: str, file_name: str) -> str:
        presigned_url = self.minio.get_presigned_url(
            method="PUT",
            bucket_name=bucket_name,
            object_name=f"{uuid}.{file_name}",
        )

        return presigned_url

    def get_presigned_download_url(self, object_name: str, bucket_name: str) -> str:
        presigned_url = self.minio.get_presigned_url(
            method="GET",
            bucket_name=bucket_name,
            object_name=object_name
        )

        return presigned_url

    def get_object(self, bucket_name: str, object_name: str):
        file_obj = self.minio.get_object(
            bucket_name=bucket_name, object_name=object_name
        )

        return file_obj.read()

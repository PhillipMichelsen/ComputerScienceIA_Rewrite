import logging
import threading

import grpc

from src.core.presigned_url_sub_service_handler import get_presigned_upload_url, get_presigned_download_url
from src.generated import file_service_pb2, file_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class PresignedURLSubService(file_service_pb2_grpc.PresignedURLSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def GetPresignedUploadURL(self, request, context):
        try:
            thread = threading.Thread(
                target=get_presigned_upload_url,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received get_presigned_upload_url request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received get_presigned_upload_url request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

    def GetPresignedDownloadURL(self, request, context):
        try:
            thread = threading.Thread(
                target=get_presigned_download_url,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Received get_presigned_download_url request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received get_presigned_download_url request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

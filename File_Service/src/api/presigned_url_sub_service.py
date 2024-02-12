import grpc
import threading
import logging

from src.utils.dependency_manager import DependencyManager

from src.generated import file_service_pb2, file_service_pb2_grpc
from src.core.presigned_url_sub_service_handler import get_presigned_upload_url, get_presigned_download_url


class PresignedURLSubService(file_service_pb2_grpc.PresignedURLSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def GetPresignedUploadURL(self, request, context):
        logging.debug(f"Received a get_presigned_url request: {request}")
        try:
            thread = threading.Thread(
                target=get_presigned_upload_url,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started get_presigned_url successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing get_presigned_url: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

    def GetPresignedDownloadURL(self, request, context):
        logging.debug(f"Received a get_presigned_url request: {request}")
        try:
            thread = threading.Thread(
                target=get_presigned_download_url,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.debug(f"Started get_presigned_url successfully on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Error processing get_presigned_url: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)
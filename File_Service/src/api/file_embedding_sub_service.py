import logging
import threading

import grpc

from src.core.file_embedding_sub_service_handler import register_file, get_files_info, process_file, \
    retrieve_nearest_n_paragraphs
from src.generated import file_service_pb2, file_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class FileEmbeddingSubService(file_service_pb2_grpc.FileEmbeddingSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def RegisterFile(self, request, context):
        try:
            thread = threading.Thread(
                target=register_file,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received register_file request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received register_file request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

    def GetFilesInfo(self, request, context):
        try:
            thread = threading.Thread(
                target=get_files_info,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received get_files_info request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received get_files_info request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

    def ProcessFile(self, request, context):
        try:
            thread = threading.Thread(
                target=process_file,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received process_file request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received process_file request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

    def RetrieveNearestNParagraphs(self, request, context):
        try:
            thread = threading.Thread(
                target=retrieve_nearest_n_paragraphs,
                args=(
                    request.task_id,
                    request.job_id,
                    self.dependency_manager
                ))
            thread.start()
            logging.info(f"Received retrieve_nearest_n_paragraphs request and successfully started on thread {thread}")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received retrieve_nearest_n_paragraphs request but had error: {e}")
            return file_service_pb2.FileServiceAcknowledgement(success=False)

        return file_service_pb2.FileServiceAcknowledgement(success=True)

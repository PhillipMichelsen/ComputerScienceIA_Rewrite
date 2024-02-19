import logging
import threading

import grpc

from src.core.llm_agent_sub_service_handler import invoke_agent
from src.generated import ai_service_pb2, ai_service_pb2_grpc
from src.utils.dependency_manager import DependencyManager


class LLMAgentSubService(ai_service_pb2_grpc.LLMAgentSubServiceServicer):
    def __init__(self, dependency_manager: DependencyManager):
        self.dependency_manager: DependencyManager = dependency_manager

    def InvokeInterpreterAgent(self, request, context):
        try:
            thread = threading.Thread(
                target=invoke_agent,
                args=(request.task_id, request.job_id, "InterpreterAgent", self.dependency_manager),
            )
            thread.start()
            logging.info(
                f"Received InvokeInterpreterAgent request and successfully started on thread {thread}"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received InvokeInterpreterAgent request but had error: {e}")
            return ai_service_pb2.AIServiceAcknowledgement(success=False)

        return ai_service_pb2.AIServiceAcknowledgement(success=True)

    def InvokeRetrievalAgent(self, request, context):
        try:
            thread = threading.Thread(
                target=invoke_agent,
                args=(request.task_id, request.job_id, "RetrievalAgent", self.dependency_manager),
            )
            thread.start()
            logging.info(
                f"Received InvokeRetrievalAgent request and successfully started on thread {thread}"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received InvokeRetrievalAgent request but had error: {e}")
            return ai_service_pb2.AIServiceAcknowledgement(success=False)

        return ai_service_pb2.AIServiceAcknowledgement(success=True)

    def InvokeSummarizationAgent(self, request, context):
        try:
            thread = threading.Thread(
                target=invoke_agent,
                args=(request.task_id, request.job_id, "SummarizationAgent", self.dependency_manager),
            )
            thread.start()
            logging.info(
                f"Received InvokeSummarizationAgent request and successfully started on thread {thread}"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received InvokeSummarizationAgent request but had error: {e}")
            return ai_service_pb2.AIServiceAcknowledgement(success=False)

        return ai_service_pb2.AIServiceAcknowledgement(success=True)

    def InvokeResponseAgent(self, request, context):
        try:
            thread = threading.Thread(
                target=invoke_agent,
                args=(request.task_id, request.job_id, "ResponseAgent", self.dependency_manager),
            )
            thread.start()
            logging.info(
                f"Received InvokeResponseAgent request and successfully started on thread {thread}"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            logging.error(f"Received InvokeResponseAgent request but had error: {e}")
            return ai_service_pb2.AIServiceAcknowledgement(success=False)

        return ai_service_pb2.AIServiceAcknowledgement(success=True)

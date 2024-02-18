from src.core.agents import (
    interpreter_agent,
    response_agent,
    retrieval_agent,
    summarization_agent,
)
from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.orchestration_service_client import OrchestrationServiceClient


def invoke_agent(task_id: str, job_id: str, dependency_manager: DependencyManager):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )

    agent_type = worker_redis_client.get_job_data(job_id, ["agent_type"])[0]

    if agent_type == "InterpreterAgent":
        print("INVOKING INTERPRETER AGENT")
        interpreter_agent.invoke_interpreter_agent(task_id, job_id, dependency_manager)
    elif agent_type == "ResponseAgent":
        print("INVOKING RESPONSE AGENT")
        response_agent.invoke_response_agent(task_id, job_id, dependency_manager)
    elif agent_type == "RetrievalAgent":
        print("INVOKING RETRIEVAL AGENT")
        retrieval_agent.invoke_retrieval_agent(task_id, job_id, dependency_manager)
    elif agent_type == "SummarizationAgent":
        print("INVOKING SUMMARIZATION AGENT")
        summarization_agent.invoke_summarization_agent(
            task_id, job_id, dependency_manager
        )
    else:
        print("INVALID AGENT TYPE")
        orchestration_service_client.task_error(task_id, "Invalid agent type")

import json
import logging

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.llm_client import LLMClient
from src.utils.orchestration_service_client import OrchestrationServiceClient


def invoke_interpreter_agent(
    task_id: str, job_id: str, dependency_manager: DependencyManager
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )
    llm_client: LLMClient = dependency_manager.get_dependency("llm_client")

    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFICATION", "step": "INTERPRET", "status": "IN_PROGRESS"}
    )

    user_input = worker_redis_client.get_job_data(job_id, ["user_input"])[0]

    prompt = 'Evaluate a user\'s request to determine if it\'s answerable. If answerable, identify the user\'s goal and specify retrieval goals (concepts to be retrieved from a semantic search) to achieve the user\'s goal. Respond in JSON format with fields for is_answerable, user_goal, and retrieval_goal.\n\'is_answerable\': A boolean value (true or false) indicating if the user\'s request can be answered. Typically, will be true, unless in rare case that user has provided unintelligible input or an input which has no clear answer.\n\'user_goal\': A string representing what the user aims to achieve with their request. Should be a single string, can be multiple sentences. An interpretation of what the user is expecting out of their message.\n\'retrieval_goals\': A list of strings that distills the user goal into queries for information retrieval.\nAll fields must be present exactly as given and lists of strings. The JSON response must contain plain JSON with no language specifiers.\n\nINPUT:{"user_input": "Can you tell me about the impact of climate change on polar bears?"}\nJSON:{"is_answerable": true, "user_goal": "Learn about the effects of climate change on polar bears", "retrieval_goals": ["Climate change effect on polar bears", "Climate change in arctic"]}\n\nINPUT:{"user_input": "How does the use of harmony in Baroque music differ from its use in the Classical period"}\nJSON:{"is_answerable": true, "user_goal": "Understand differences in harmony use between Baroque and Classical periods", "retrieval_goals": ["Harmony differences between Baroque and Classical periods", "Harmony in Baroque period", "Harmony in Classical period"]}\n\nINPUT:{"user_input": "I like fish"}\nJSON:{"is_answerable": false, "user_goal": "", "retrieval_goals": []}'

    response = llm_client.create_completion_json(
        model="gemini-pro",
        prompt=prompt,
        input_message=json.dumps({"user_input": user_input}),
        return_fields=(
            ("is_answerable", bool),
            ("user_goal", str),
            ("retrieval_goals", list),
        ),
    )
    logging.info(f"Interpreter response: {response}")

    if response["is_answerable"]:
        worker_redis_client.set_job_data_field(
            job_id, "user_goal", response["user_goal"]
        )
        worker_redis_client.set_job_data_field(
            job_id, "retrieval_goals", "::".join(response["retrieval_goals"])
        )

        orchestration_service_client.add_task_to_job(job_id, "InvokeRetrievalAgent")
    else:
        orchestration_service_client.task_error(task_id, "Query not answerable")
        raise Exception("Query not answerable")

    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFICATION", "step": "INTERPRET", "status": "COMPLETED", "detail": f"Interpreted goal: {response['user_goal']}"}
    )
    orchestration_service_client.task_completed(task_id)

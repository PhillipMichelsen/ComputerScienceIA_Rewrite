import json

import openai

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
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

    user_input = worker_redis_client.get_job_data(job_id, ["user_input"])[0]

    prompt = (
        "You're an interpreting agent in a 'retrieval and generation' system designed to provide context-specific responses to user queries. "
        "Your role is to evaluate incoming messages for answerability and interpret user intentions. "
        "Respond in JSON (and nothing else aside from the JSON object) with is_answerable, user_goal, and retrieval_goals: "
        "is_answerable: Boolean indicating if the query is answerable. If False, set other fields to blank strings. Remember that the query is with relation to information stored, so it is most likely answerable. This is more of a check to see if the query is not a misinput."
        "user_goal: This is the goal the system should aim to complete. Provide in sentences, multiple sentences are fine if the request is multifaceted. Should never be a list, always a single string."
        "retrieval_goals: Statements or phrases guiding the retrieval agent, semantic search is used so broad phrases on the general topic are best. Outline all information deemed necessary for fulfilling the user_goal. Give as a list of goals in order of 'importance'. Should be a list of strings."
    )

    llm_response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": str(prompt)},
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )

    response = llm_response.choices[0].message.content
    response = json.loads(response)
    print(response, flush=True)
    print(
        (llm_response.usage.prompt_tokens * 0.0000005)
        + (llm_response.usage.completion_tokens * 0.0000015),
        flush=True,
    )

    if response["is_answerable"]:
        worker_redis_client.set_job_data_field(
            job_id, "user_goal", response["user_goal"]
        )
        worker_redis_client.set_job_data_field(
            job_id, "retrieval_goals", "::".join(response["retrieval_goals"])
        )
        worker_redis_client.set_job_data_field(job_id, "agent_type", "RetrievalAgent")

        orchestration_service_client.add_task_to_job(job_id, "InvokeAgent")
    else:
        orchestration_service_client.task_error(task_id, "Query not answerable")
        raise Exception("Query not answerable")

    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFY", "message": "Interpreted user input."}
    )
    orchestration_service_client.task_completed(task_id)

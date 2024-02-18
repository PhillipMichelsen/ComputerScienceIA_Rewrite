import json

import openai

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.orchestration_service_client import OrchestrationServiceClient


def invoke_retrieval_agent(
    task_id: str, job_id: str, dependency_manager: DependencyManager
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )

    user_goal, retrieval_goals = worker_redis_client.get_job_data(
        job_id, ["user_goal", "retrieval_goals"]
    )

    query = {
        "user_goal": user_goal,
        "retrieval_goal": str(retrieval_goals.split("::")),
    }

    prompt = (
        "You're a retrieval agent within a 'retrieval and generation' system, aimed at sourcing information to answer user queries with contextually relevant data. "
        "Your task is guided by a specific 'retrieval_goal' alongside a 'user_goal' for broader contextual understanding. "
        "Generate targeted 'search_concepts'. "
        "Also, determine 'move_towards_concepts' to highlight and 'move_away_concepts' to avoid, ensuring the search's relevance and precision. "
        "These will be given to a semantic search engine to retrieve the most relevant information, so keywords and phrases are best if they are not too specific."
        "Respond in JSON with 'search_concepts', 'move_towards_concepts', and 'move_away_concepts': "
        "search_concepts: These should be keywords and terms which guide the search to the general topic and area of the user query. This should be broad yet focused, and should be a list of strings."
        "move_towards_concepts: These should again be keywords and terms, but these refine the search to a more specific area of the general topic. This should be a list of strings."
        "move_away_concepts: This should be a list of keywords and terms which should be avoided in the search. These are to move the search away from irrelevant areas that may be related too but not impactful to the retrieval goal. This should be a list of strings."
        "You are expected to fill out each of these fields with a list of strings. Focus more on the 'search_concepts' and 'move_towards_concepts' as they are the most important, but ensure that all fields are filled out."
        "As you are responding in this strict JSON format, ensure that the keys are exactly as specified here. All fields must be present and lists of strings."
    )

    llm_response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": str(prompt),
            },
            {
                "role": "user",
                "content": json.dumps(query),
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

    worker_redis_client.set_job_data_field(
        job_id, "search_concepts", "::".join(response["search_concepts"])
    )
    worker_redis_client.set_job_data_field(
        job_id, "move_towards_concepts", "::".join(response["move_towards_concepts"])
    )
    worker_redis_client.set_job_data_field(
        job_id, "move_away_concepts", "::".join(response["move_away_concepts"])
    )
    worker_redis_client.set_job_data_field(job_id, "agent_type", "SummarizationAgent")

    orchestration_service_client.add_task_to_job(job_id, "RetrieveNearestNParagraphs")
    orchestration_service_client.add_task_to_job(job_id, "InvokeAgent")

    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFY", "message": "Retrieval request formed."}
    )
    orchestration_service_client.task_completed(task_id)

import json
import logging

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.llm_client import LLMClient
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
    llm_client: LLMClient = dependency_manager.get_dependency("llm_client")

    orchestration_service_client.notify_job(
        task_id,
        {
            "type": "NOTIFICATION",
            "step": "RETRIEVAL",
            "status": "IN_PROGRESS",
            "detail": "Retrieval agent invoked.",
        },
    )

    user_goal, retrieval_goals = worker_redis_client.get_job_data(
        job_id, ["user_goal", "retrieval_goals"]
    )

    prompt = 'Evaluate and a user_goal and retrieval_goal input message into a semantic search. Respond in JSON with \'search_concepts\', \'move_towards_concepts\', and \'move_away_concepts\' fields.\n\'search_concepts\': An array of strings, the general topic and area of the user query.\n\'move_towards_concepts\': An array of strings, refining the search to a more specific area of the general topic.\n\'move_away_concepts\': An array of strings, to avoid irrelevant areas that may be related too but not impactful to the retrieval goal.\nAll fields must be present exactly as given and lists of strings. The JSON response must contain plain JSON with no language specifiers.\n\nINPUT:{"user_goal": "Explain Maslow\'s theory", "retrieval_goal": "Maslow\'s theory"}\nJSON:{"search_concepts": ["Maslow\'s hierarchy of needs", "human motivation", "psychology"], "move_towards_concepts": ["Abraham Maslow", "self-actualization", "deficiency needs"], "move_away_concepts": ["Carl Rogers", "humanistic psychology", "behaviorism"]} \n\nINPUT:{"user_goal": "Provide reasons renewable energy is better than non-renewable energy", "retrieval_goal": "Renewable energy"}\nJSON:{"search_concepts": ["Renewable energy", "Non-renewable energy", "Energy sources"], "move_towards_concepts": ["Environmental benefits", "Economic benefits", "Sustainability"], "move_away_concepts": ["Nuclear energy", "Fossil fuels", "Depletion of natural resources"]}'

    response = llm_client.create_completion_json(
        model="gemini-pro",
        prompt=prompt,
        input_message=json.dumps(
            {"user_input": user_goal, "retrieval_goal": retrieval_goals}
        ),
        return_fields=(
            ("search_concepts", list),
            ("move_towards_concepts", list),
            ("move_away_concepts", list),
        ),
    )
    logging.info(f"Retrieval response: {response}")

    worker_redis_client.set_job_data_field(
        job_id, "search_concepts", "::".join(response["search_concepts"])
    )
    worker_redis_client.set_job_data_field(
        job_id, "move_towards_concepts", "::".join(response["move_towards_concepts"])
    )
    worker_redis_client.set_job_data_field(
        job_id, "move_away_concepts", "::".join(response["move_away_concepts"])
    )

    orchestration_service_client.add_task_to_job(job_id, "RetrieveNearestNParagraphs")
    orchestration_service_client.add_task_to_job(job_id, "InvokeSummarizationAgent")

    orchestration_service_client.notify_job(
        task_id,
        {
            "type": "NOTIFICATION",
            "step": "RETRIEVAL",
            "status": "IN_PROGRESS",
            "detail": f"Search concepts: {response['search_concepts']}",
        },
    )
    orchestration_service_client.task_completed(task_id)

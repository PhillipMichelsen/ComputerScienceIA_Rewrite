import json

import openai

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.orchestration_service_client import OrchestrationServiceClient


def invoke_summarization_agent(
    task_id: str, job_id: str, dependency_manager: DependencyManager
):
    worker_redis_client: WorkerRedisClient = dependency_manager.get_dependency(
        "worker_redis_client"
    )
    orchestration_service_client: OrchestrationServiceClient = (
        dependency_manager.get_dependency("orchestration_service_client")
    )

    similar_paragraphs, user_goal, user_input = worker_redis_client.get_job_data(
        job_id, ["similar_paragraphs", "user_goal", "user_input"]
    )

    prompt = (
        "You're a summarization agent in a 'retrieval and generation' system designed to provide context-specific responses to user queries. "
        "Your role is to take in a list of 'similar_paragraphs' which have been retrieved from a semantic search engine, and to pick out information pieces that are relevant."
        "You are also provided with a 'user_goal' (alonside the original user input) which is the goal the system should aim to complete. Use this to guide your summary."
        "Respond in JSON (and nothing else aside from the JSON object) with a 'summary' field:"
        "summary: A list of information pieces from the 'similar_paragraphs' that is relevant to the 'user_goal'. This should be a list of strings (required field, if no useful summary can be generated, leave as an empty list)."
        "You are encouraged to quote the information as to not lose the original context, but ensure that the summary is concise and to the point. In essence, you are removing the unnecessary information and keeping the relevant information."
        "Although you are 'summarizing' you are really more 'extracting' the relevant information from the paragraphs. INCLUDE AS MANY AS POSSIBLE. Even if not directly relevant, it is better to have too much information than too little."
        "There will exist examples or details related to aspects of the user goal, make sure to include them. Basically, take the paragraphs and remove the useless information, leaving only the relevant information. Most of it will be useful!"
    )

    llm_response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": str(prompt)},
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "similar_paragraphs": similar_paragraphs,
                        "user_goal": user_goal,
                        "user_input": user_input,
                    }
                ),
            },
        ],
    )

    response = llm_response.choices[0].message.content
    response = json.loads(response)
    print(
        {
            "similar_paragraphs": similar_paragraphs,
            "user_goal": user_goal,
            "user_input": user_input,
        }
    )
    print(response, flush=True)
    print(
        (llm_response.usage.prompt_tokens * 0.0000005)
        + (llm_response.usage.completion_tokens * 0.0000015),
        flush=True,
    )

    if response["summary"]:
        current_summary = worker_redis_client.get_job_data(job_id, ["summary"])[0]

        if current_summary:
            current_summary += "::" + "::".join(response["summary"])
            worker_redis_client.set_job_data_field(job_id, "summary", current_summary)
        else:
            worker_redis_client.set_job_data_field(
                job_id, "summary", "::".join(response["summary"])
            )
    else:
        orchestration_service_client.task_error(task_id, "No summary generated")
        raise Exception("No summary generated")

    # JUST FOR NOW. TODO: Need to check if there exists another retrieval goal and if so, add another task to the job
    worker_redis_client.set_job_data_field(job_id, "agent_type", "ResponseAgent")

    orchestration_service_client.add_task_to_job(job_id, "InvokeAgent")
    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFY", "message": "Summary generated!"}
    )
    orchestration_service_client.task_completed(task_id)

import json
import logging

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.llm_client import LLMClient
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
    llm_client: LLMClient = dependency_manager.get_dependency("llm_client")

    orchestration_service_client.notify_job(task_id, {"type": "NOTIFICATION", "step": "SUMMARIZATION", "status": "IN_PROGRESS"})

    similar_paragraphs, retrieval_goals, user_goal = worker_redis_client.get_job_data(
        job_id, ["similar_paragraphs", "retrieval_goals", "user_goal"]
    )

    prompt = 'Evaluate a list of \'similar_paragraphs\' retrieved from a semantic search alongside a \'user_goal and \'retrieval_goal\' to extract and condense relevant information to fulfill the user\'s goal. Respond in JSON format with a \'summary\' field:\n\'summary\': A LIST OF STRINGS, each an essential piece of information from \'similar_paragraphs\' that, at minimum, are loosely related to the \'user_goal\'. This should include direct quotes or paraphrased content as necessary to maintain context and accuracy. The summary should be as verbose as possible to retain as much important information as possible.\nAll fields must be present exactly as given and lists of strings. The JSON response must contain plain JSON with no language specifiers. Ensure that you JSON is accurate and without error.\n\nINPUT:{"similar_paragraphs": ["Climate change has led to significant ice melting in the Arctic, reducing the natural habitat of polar bears. These changes force polar bears to travel greater distances for food, leading to a decrease in body condition and survival rates.", "Polar bears are known to be excellent swimmers, but increased open water areas require more energy for swimming, which is not always available in their diet.", "Global warming is often discussed in the context of its impact on tropical regions, with less focus on polar areas. However, the Arctic is one of the most affected regions, experiencing warming at twice the rate of the rest of the world."], "retrieval_goal": "Effects of climate change on polar bears", "user_goal": "Learn about the effects of climate change on polar bears"}\nJSON:{"summary": ["The Arctic\'s significant ice melt, driven by climate change, is reducing polar bears\' natural habitats, compelling them to traverse longer distances in search of food. This increased effort not only leads to a decline in their physical condition but also negatively impacts their overall survival rates, underscoring the dire consequences of environmental changes on these apex predators.", "Despite being adept swimmers, polar bears face increased challenges as melting ice results in larger open water areas. This situation demands higher energy expenditure for swimming—a demand that often exceeds the energy they can derive from their diet, illustrating a critical survival challenge induced by changing climate conditions.", "While global warming\'s impact is frequently highlighted in tropical contexts, the Arctic\'s situation is particularly acute, with the region experiencing double the warming rate compared to the global average. This accelerated change makes the Arctic a critical area of concern for climate scientists and conservationists, emphasizing the urgent need for focused attention on the implications of such rapid environmental transformations."]}\n\nINPUT:{"similar_paragraphs": ["Baroque music is characterized by its complex use of harmony, with composers often employing counterpoint to create rich, textured soundscapes. This period saw the development of chordal experimentation and ornamental melodies.", "In contrast, the Classical period favored clarity and simplicity in harmony. Composers like Mozart and Haydn sought to achieve balance and form, using harmonious progressions that supported clear, lyrical melodies.", "The use of harmony in jazz music, while not directly related to the Baroque or Classical periods, shows a different approach to chordal structure and improvisation."], "retrieval_goal": "Difference in harmony between Baroque and Classical periods", "user_goal": "Understand differences in harmony use between Baroque and Classical periods"}\nJSON:{"summary": ["Baroque music\'s hallmark is its intricate harmony, achieved through the extensive use of counterpoint. This era was notable for its adventurous chordal experimentation and the embellishment of melodies, creating a distinctively rich and textured musical fabric that stands in contrast to later periods.", "The Classical period marked a departure towards a more refined harmonic approach, emphasizing clarity, simplicity, and structural balance. Iconic composers of this era, such as Mozart and Haydn, mastered the art of crafting harmonious progressions that underpinned clear, expressive melodies, setting a new standard for musical composition that valued coherence and elegance.", "Though not a direct comparison, the harmonic techniques in jazz characterized by innovative chordal structures and the freedom of improvisation—offer a glimpse into the evolving nature of harmony beyond the classical tradition. This demonstrates the diverse application and transformation of harmonic concepts across different musical genres."]}'

    response = llm_client.create_completion_json(
        model="gemini-pro",
        prompt=prompt,
        input_message=json.dumps(
            {
                "similar_paragraphs": similar_paragraphs,
                "retrieval_goal": retrieval_goals,
                "user_goal": user_goal,
            }
        ),
        return_fields=(("summary", list),),
    )
    logging.info(f"Summarization response: {response}")

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

    orchestration_service_client.add_task_to_job(job_id, "InvokeResponseAgent")
    orchestration_service_client.notify_job(
        task_id,
        {
            "type": "NOTIFICATION",
            "step": "SUMMARIZATION",
            "status": "COMPLETED",
            "detail": f"Summary generated for retrieval goal: {retrieval_goals}",
        },
    )
    orchestration_service_client.task_completed(task_id)

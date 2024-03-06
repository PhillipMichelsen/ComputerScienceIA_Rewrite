import json

from src.repositories.redis_client import WorkerRedisClient
from src.utils.dependency_manager import DependencyManager
from src.utils.llm_client import LLMClient
from src.utils.orchestration_service_client import OrchestrationServiceClient


def invoke_response_agent(
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
        task_id, {"type": "NOTIFICATION", "step": "RESPONSE", "status": "IN_PROGRESS"}
    )

    summary, user_goal, user_query = worker_redis_client.get_job_data(
        job_id, ["summary", "user_goal", "user_input"]
    )

    prompt = 'Generate a comprehensive response to the user\'s query by interpreting a \'summary\' of key information extracted from relevant paragraphs. The response is guided by the \'user_goal\'. Your response should be provided in a JSON format with a \'response\' field:\n\'response\': A detailed answer to the user query, directly addressing the \'user_input\', guided by the user_goal. Use the information in the \'summary\' to construct your response, ensuring it is relevant, accurate, and self-contained. If the \'summary\' does not contain information sufficient to answer the user query, respond with a polite message indicating the absence of relevant information. Your response should be verbose, covering as much information from the \'summary\' as possible to minimize follow-up questions. Structure your response in paragraphs for readability. This response should be a single string. Do use nice looking formatting within the string for the response, using \'\\n\' to line break.\nAll fields must be present exactly as given and lists of strings. The JSON response must contain plain JSON with no language specifiers.\n\nINPUT:{"summary": ["Arctic ice melting due to climate change reduces polar bear habitats, impacting their food access and survival.", "Increased distances and open water require polar bears to expend more energy swimming, affecting their dietary needs and overall health."], "user_input": "What are the effects of climate change on polar bears?", "user_goal": "Learn about the effects of climate change on polar bears"}\nJSON:{"response": "The effects of climate change on polar bears are profound and multifaceted. The melting Arctic ice diminishes the natural habitat of polar bears, significantly impacting their access to food and, consequently, their survival rates. Furthermore, as polar bears are compelled to cover greater distances due to the increased open water, their energy expenditure for swimming rises, adversely affecting their dietary needs and overall health. These changes underscore the urgent need for climate action to protect polar bears and their habitat."}\n\nINPUT:{"summary": ["Artificial Intelligence (AI) in medicine is revolutionizing patient care through predictive analytics, enabling early detection of diseases such as cancer.", "AI-driven algorithms are instrumental in analyzing vast datasets, significantly improving the accuracy of diagnoses and the personalization of treatment plans.", "Robot-assisted surgery, guided by AI, enhances precision during operations, minimizing recovery times and improving surgical outcomes.", "Despite its benefits, the integration of AI in medicine raises ethical concerns, including patient data privacy and the potential for algorithmic bias.", "The ongoing development of AI technologies promises to further transform healthcare, making it more efficient, effective, and personalized."], "user_input": "What is the impact of AI on modern medicine?", "user_goal": "Explain the impact of artificial intelligence on modern medicine."}\nJSON:{"response": "The advent of Artificial Intelligence (AI) in the realm of modern medicine marks a pivotal transformation, ushering in an era of enhanced patient care, diagnostic precision, and treatment efficacy. At the forefront, AI\'s application in predictive analytics plays a critical role in the early detection of life-threatening diseases, such as cancer, by meticulously analyzing patterns within vast healthcare datasets. This capability not only accelerates the diagnostic process but also elevates the accuracy level, thereby significantly influencing treatment outcomes positively.\\n\\nMoreover, AI-driven algorithms stand as a cornerstone in the realm of personalized medicine. By sifting through extensive datasets, these algorithms facilitate the customization of treatment plans tailored specifically to individual patient profiles, thereby optimizing therapeutic effectiveness. Additionally, the introduction of robot-assisted surgery, underpinned by AI, epitomizes the technological strides in surgical precision. These robotic systems enhance the surgeon\'s ability to perform complex procedures with heightened accuracy, resulting in reduced recovery times and markedly improved post-operative results.\\n\\nHowever, the integration of AI into healthcare is not devoid of challenges. Ethical concerns, particularly regarding patient data privacy and the risk of algorithmic bias, pose significant hurdles. These issues necessitate stringent regulatory frameworks and ethical guidelines to ensure that AI\'s deployment in medicine prioritizes patient welfare and equity.\\n\\nLooking forward, the trajectory of AI in medicine is poised for further groundbreaking advancements. The continuous refinement of AI technologies promises to bolster healthcare delivery, making it more efficient, effective, and patient-centric. The potential for AI to redefine medical paradigms is immense, setting the stage for a future where technology and healthcare converge to facilitate unprecedented levels of care and treatment personalization."}\n\nINPUT:{"summary": [], "user_input": "What is the impact of urban development on local wildlife and fauna?", "user_goal": "Explore the impact of urban development on local wildlife and plant species."}\nJSON:{\n  "response": "I\'m sorry, but we were unable to find detailed information on the impact of urban development on local wildlife and plant species based on the current resources. Urbanization\'s effects on biodiversity is a complex topic, often involving changes to habitats, disruptions in local ecosystems, and challenges for wildlife conservation."}'

    response = llm_client.create_completion_json(
        model="gemini-pro",
        prompt=prompt,
        input_message=json.dumps(
            {
                "summary": summary,
                "user_input": user_query,
                "user_goal": user_goal,
            }
        ),
        return_fields=(("response", str),),
    )

    orchestration_service_client.notify_job(
        task_id, {"type": "NOTIFICATION", "step": "RESPONSE", "status": "COMPLETED"}
    )
    orchestration_service_client.notify_job(
        task_id, {"type": "RETURN", "response": response["response"]}
    )
    orchestration_service_client.task_completed(task_id)

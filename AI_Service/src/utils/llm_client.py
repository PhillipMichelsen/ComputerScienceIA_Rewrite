import json
from abc import ABC, abstractmethod

import google.generativeai as genai
import openai


class LLMClient(ABC):
    @abstractmethod
    def create_completion_json(
        self, model: str, prompt: str, input_message: str, return_fields: list
    ) -> dict:
        pass


class OpenAILLMClient(LLMClient):
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def create_completion_json(
        self, model: str, prompt: str, input_message: str, return_fields: tuple
    ) -> dict:
        llm_response = openai.ChatCompletion.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": input_message,
                },
            ],
        )
        response = llm_response.choices[0].message.content
        response = json.loads(response)

        result = {}
        for field, expected_type in return_fields:
            if field in response:
                if isinstance(response[field], expected_type):
                    result[field] = response[field]
                else:
                    raise ValueError(
                        f"Field {field} in the response is not of type {expected_type}"
                    )
            else:
                raise ValueError(f"Field {field} not found in the response")

        return result


class GoogleAILLMClient(LLMClient):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)

    def create_completion_json(
        self, model: str, prompt: str, input_message: str, return_fields: tuple
    ) -> dict:
        model = genai.GenerativeModel(model)

        response = model.generate_content(
            f"{prompt} \n\n###\nINPUT:\n{input_message}\n\nOUTPUT:\n"
        )
        response = json.loads(response.text)
        print(response)
        result = {}
        for field, expected_type in return_fields:
            if field in response:
                if isinstance(response[field], expected_type):
                    result[field] = response[field]
                else:
                    raise ValueError(
                        f"Field {field} in the response is not of type {expected_type}"
                    )
            else:
                raise ValueError(f"Field {field} not found in the response")

        return result

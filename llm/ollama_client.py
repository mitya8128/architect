import ollama
from llm.base import LLM


class OllamaClient(LLM):

    def __init__(self, model="deepseek-r1:latest"):
        self.model = model

    def generate(self, system_prompt, user_prompt):

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response["message"]["content"]
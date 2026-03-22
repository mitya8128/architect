import requests
from llm.base import LLM


class OllamaClient(LLM):

    def __init__(self, model="llama3"):
        self.model = model

    def generate(self, system_prompt, user_prompt):

        prompt = f"{system_prompt}\n\n{user_prompt}"

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
        )

        return response.json()["response"]
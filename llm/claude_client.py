import anthropic
from llm.base import LLM


class ClaudeClient(LLM):

    def __init__(self, model="claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic()
        self.model = model

    def generate(self, system_prompt, user_prompt):

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"{system_prompt}\n\n{user_prompt}"
                }
            ],
        )

        return response.content[0].text
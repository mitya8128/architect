from llm.openai_client import OpenAIClient
from llm.ollama_client import OllamaClient


def get_llm(provider: str):

    if provider == "openai":
        return OpenAIClient()

    if provider == "ollama":
        return OllamaClient()

    raise ValueError("Unknown provider")
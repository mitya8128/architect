from llm.openai_client import OpenAIClient
from llm.ollama_client import OllamaClient
from llm.claude_client import ClaudeClient


def get_llm(provider: str, model: str):

    if provider == "openai":
        return OpenAIClient()

    if provider == "ollama":
        return OllamaClient()
    
    if provider == "claude":
        return ClaudeClient()

    raise ValueError("Unknown provider")
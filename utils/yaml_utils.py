import re
import yaml


def extract_yaml(text: str) -> str:
    """
    Extract the most likely YAML block from an LLM response.
    Handles:
    - <think> blocks
    - ```yaml fences
    - explanations before/after YAML
    """

    # remove think tags
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # case 1 — markdown yaml block
    fenced = re.findall(r"```yaml(.*?)```", text, flags=re.DOTALL)

    if fenced:
        return fenced[0].strip()

    # case 2 — any fenced block
    fenced_any = re.findall(r"```(.*?)```", text, flags=re.DOTALL)

    if fenced_any:
        return fenced_any[0].strip()

    # case 3 — fallback: find start of architecture
    idx = text.find("system:")

    if idx != -1:
        return text[idx:].strip()

    return text.strip()


def normalize_yaml(text: str) -> str:
    """
    Parse and re-dump YAML to clean indentation.
    """

    data = yaml.safe_load(text)

    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True
    )
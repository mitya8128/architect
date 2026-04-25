def build_code_prompt(architecture_yaml: str) -> str:

    return f"""
Generate Python code from the following architecture.

STRICT RULES:
- Each module = one function
- Function name must match module name
- Avoid cycles if possible
- Use type annotations
- Follow pipeline order via function calls
- No extra explanations
- Output ONLY Python code

Architecture:
{architecture_yaml}
"""
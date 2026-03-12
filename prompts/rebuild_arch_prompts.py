def build_repair_prompt(original_prompt, errors):

    error_text = "\n".join(errors)

    return f"""
The architecture you generated contains verification errors.

Errors:
{error_text}

Please regenerate a corrected architecture YAML.

Original request:
{original_prompt}
"""
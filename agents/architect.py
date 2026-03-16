def generate_architecture(requirements):

    prompt = f"""
    Design system architecture in YAML DSL.

    Requirements:
    {requirements}

    Output only YAML.
    """

    return llm.generate(prompt)
def critique_architecture(architecture):

    prompt = f"""
    Analyze the architecture and find design issues.

    Architecture:
    {architecture}

    Return YAML list of issues.
    """

    return llm.generate(prompt)
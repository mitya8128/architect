def improve_architecture(architecture, issues):

    prompt = f"""
    Improve the architecture.

    Current architecture:
    {architecture}

    Issues:
    {issues}

    Output improved YAML architecture.
    """

    return llm.generate(prompt)
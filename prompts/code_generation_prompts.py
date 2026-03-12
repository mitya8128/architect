PYTHON_PROMPT = '''
You are a code generator.

You must implement the modules defined in the architecture.

Rules:

1. Every module must be implemented as a Python function.
2. The function name must match the module name.
3. The input argument type must match the module input type.
4. The return type must match the module output type.
5. Use Python type annotations.

Architecture:

{{architecture_yaml}}

Generate ONLY Python code.

'''
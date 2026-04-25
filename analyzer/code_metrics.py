import ast


DANGEROUS = ["eval", "exec", "os.system"]


def detect_large_functions(tree):

    errors = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            if len(node.body) > 20:
                errors.append(f"{node.name} too large")

    return errors


def detect_high_coupling(graph):

    errors = []

    for f, calls in graph.items():
        if len(calls) > 5:
            errors.append(f"{f} has high coupling")

    return errors


def detect_dangerous_calls(calls):

    return [
        f"dangerous call: {callee}"
        for _, callee in calls
        if callee in DANGEROUS
    ]


def compute_score(errors, warnings):

    return (
        -10 * len(errors)
        -2 * len(warnings)
    )

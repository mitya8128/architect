import ast


def detect_side_effects(tree):

    effects = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            name = getattr(node.func, "id", None)

            if name in ["print", "open", "requests", "os"]:
                effects.append(name)

    return effects
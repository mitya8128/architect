def match_modules(arch, code_functions):

    missing = []
    extra = []

    for m in arch.modules:
        if m not in code_functions:
            missing.append(m)

    for f in code_functions:
        if f not in arch.modules:
            extra.append(f)

    return missing, extra


def match_types(arch, code_types):

    arch_types = set(arch.types)

    missing = arch_types - code_types
    extra = code_types - arch_types

    return missing, extra


def check_pipeline_vs_graph(arch, graph):

    errors = []
    warnings = []

    for pipeline in arch.pipelines.values():

        for i in range(len(pipeline.modules) - 1):

            f = pipeline.modules[i]
            g = pipeline.modules[i+1]

            callees = graph.get(f, [])

            if g not in callees:

                if f not in graph:
                    warnings.append(f"{f} not implemented in code")
                else:
                    errors.append(f"Pipeline inconsistent: {f} -> {g}")

    return errors, warnings


def check_composition(graph, functions):

    errors = []

    for f, callees in graph.items():

        f_out = functions[f]["output"]

        for g in callees:

            if g not in functions:
                continue

            g_in = functions[g]["input"]

            if f_out and g_in and f_out != g_in:
                errors.append(
                    f"type mismatch: {f} ({f_out}) -> {g} ({g_in})"
                )

    return errors


def check_cycles(graph):

    visited = set()
    stack = set()

    def dfs(node):

        if node in stack:
            return True

        if node in visited:
            return False

        visited.add(node)
        stack.add(node)

        for neighbor in graph[node]:
            if neighbor in graph and dfs(neighbor):
                return True

        stack.remove(node)
        return False

    for node in graph:
        if dfs(node):
            return ["Cycle detected"]

    return []


def check_unused_functions(graph):

    called = set()

    for callees in graph.values():
        called.update(callees)

    unused = set(graph.keys()) - called

    # исключаем entry points (например, main)
    unused = [f for f in unused if f != "main"]

    return [f"Unused function: {f}" for f in unused]


def check_missing_functions(graph):

    errors = []

    all_funcs = set(graph.keys())

    for caller, callees in graph.items():
        for callee in callees:
            if callee not in all_funcs:
                errors.append(f"{caller} calls unknown function {callee}")

    return errors
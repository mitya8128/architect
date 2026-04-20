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

    for pipeline in arch.pipelines.values():

        for i in range(len(pipeline.modules) - 1):

            f = pipeline.modules[i]
            g = pipeline.modules[i+1]

            if g not in graph.get(f, []):
                errors.append(f"Pipeline broken: {f} -> {g}")

    return errors


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

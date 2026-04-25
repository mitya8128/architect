import ast
from .parser import extract_functions, extract_types, extract_calls, build_call_graph
from .side_effects import detect_side_effects
from .matching import check_composition, check_cycles, check_pipeline_vs_graph, check_unused_functions, \
check_missing_functions
from .code_metrics import detect_high_coupling, detect_large_functions, detect_dangerous_calls, \
compute_score


def analyze_code(code: str, arch=None):

    tree = ast.parse(code)

    # extraction
    functions = extract_functions(code)
    calls = extract_calls(code)
    graph = build_call_graph(functions, calls)
    types = extract_types(tree)
    side_effects = detect_side_effects(tree)

    # checks
    errors = []
    warnings = []

    errors += check_missing_functions(graph)
    errors += check_cycles(graph)
    errors += check_unused_functions(graph)
    errors += check_composition(graph, functions)

    warnings += detect_high_coupling(graph)
    warnings += detect_large_functions(tree)
    warnings += detect_dangerous_calls(calls)

    # arch matching
    if arch is not None:
        arch_errors, arch_warnings = check_pipeline_vs_graph(
            arch, graph
        )
        errors += arch_errors
        warnings += arch_warnings

    # metrics
    metrics = {
        "num_functions": len(functions),
        "num_edges": sum(len(v) for v in graph.values()),
        # "num_types": len(types),
        "num_side_effects": len(side_effects),
        "num_errors": len(errors),
        "num_warnings": len(warnings),
    }

    score = compute_score(errors, warnings)

    return {
        "functions": functions,
        "graph": graph,
        # "types": list(types),
        "side_effects": side_effects,
        "metrics": metrics,
        "errors": errors,
        "warnings": warnings,
        "score": score,
    }
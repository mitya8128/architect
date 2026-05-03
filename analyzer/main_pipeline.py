import ast
from .parser import extract_functions, extract_types, extract_calls, build_call_graph, is_valid_python
from .side_effects import detect_side_effects
from .matching import check_composition, check_cycles, check_pipeline_vs_graph, check_unused_functions, \
check_missing_functions
from .code_metrics import detect_high_coupling, detect_large_functions, detect_dangerous_calls, \
compute_score


def init_error_structure():
    return {
        "syntax": [],
        "semantic": [],
        "architecture": []
    }


def analyze_code(code: str, arch=None):

    error_map = init_error_structure()
    warnings = []

    # =====================
    # SYNTAX LEVEL
    # =====================
    valid, syntax_error = is_valid_python(code)

    if not valid:
        error_map["syntax"].append(f"Syntax error: {syntax_error}")

        return build_result(
            functions={},
            graph={},
            types=[],
            side_effects=[],
            error_map=error_map,
            warnings=warnings
        )

    # =====================
    # AST
    # =====================
    tree = ast.parse(code)

    functions = extract_functions(code)
    calls = extract_calls(code)
    graph = build_call_graph(functions, calls)
    types = extract_types(tree) or set()
    side_effects = detect_side_effects(tree)

    # =====================
    # SEMANTIC LEVEL
    # =====================
    error_map["semantic"] += check_missing_functions(graph)
    error_map["semantic"] += check_cycles(graph)
    error_map["semantic"] += check_unused_functions(graph)
    error_map["semantic"] += check_composition(graph, functions)

    warnings += detect_high_coupling(graph)
    warnings += detect_large_functions(tree)
    warnings += detect_dangerous_calls(calls)

    # =====================
    # ARCH LEVEL
    # =====================
    if arch is not None:
        arch_errors, arch_warnings = check_pipeline_vs_graph(
            arch, graph
        )

        error_map["architecture"] += arch_errors
        warnings += arch_warnings

    # =====================
    # METRICS
    # =====================
    flat_errors = sum(error_map.values(), [])

    metrics = {
        "num_functions": len(functions),
        "num_edges": sum(len(v) for v in graph.values()),
        "num_types": len(types),
        "num_side_effects": len(side_effects),
        "num_errors": len(flat_errors),
        "num_warnings": len(warnings),
    }

    score = compute_score(flat_errors, warnings)

    return {
        "functions": functions,
        "graph": graph,
        "types": list(types),
        "side_effects": side_effects,
        "metrics": metrics,
        "errors": error_map,
        "warnings": warnings,
        "score": score,
    }


def build_result(functions, graph, types, side_effects, error_map, warnings):

    flat_errors = sum(error_map.values(), [])

    metrics = {
        "num_functions": len(functions),
        "num_edges": sum(len(v) for v in graph.values()) if graph else 0,
        "num_types": len(types),
        "num_side_effects": len(side_effects),
        "num_errors": len(flat_errors),
        "num_warnings": len(warnings),
    }

    score = compute_score(flat_errors, warnings)

    return {
        "functions": functions,
        "graph": graph,
        "types": list(types),
        "side_effects": side_effects,
        "metrics": metrics,
        "errors": error_map,
        "warnings": warnings,
        "score": score,
    }
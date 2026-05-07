import os
from .matching import check_cycles, check_unused_functions, check_missing_functions
from .parser import extract_functions, extract_calls


def collect_python_files(root_path):
    py_files = []

    for root, _, files in os.walk(root_path):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(root, f))

    return py_files


def parse_repository(files):

    all_functions = {}
    all_calls = {}

    for file_path in files:

        try:
            with open(file_path) as f:
                code = f.read()
        except Exception:
            continue

        functions = extract_functions(code)
        calls = extract_calls(code)

        # namespace functions by file
        for name, meta in functions.items():
            key = f"{file_path}::{name}"
            all_functions[key] = meta

        # store calls per file
        all_calls[file_path] = calls

    return all_functions, all_calls


def build_global_call_graph(all_functions, all_calls):

    graph = {f: [] for f in all_functions.keys()}

    # reverse index: function name → full keys
    name_index = {}

    for full_name in all_functions:
        fname = full_name.split("::")[-1]
        name_index.setdefault(fname, []).append(full_name)

    # build edges
    for file_path, calls in all_calls.items():

        caller_file_index = {}

        for full_name in all_functions:
            if full_name.startswith(file_path + "::"):
                short = full_name.split("::")[-1]
                caller_file_index[short] = full_name

        # calls is LIST now
        for caller, callee in calls:

            caller_key = caller_file_index.get(caller)

            if caller_key is None:
                continue

            targets = name_index.get(callee, [])

            for target in targets:
                graph[caller_key].append(target)

    return graph


def analyze_repository(root_path):

    files = collect_python_files(root_path)

    all_functions, all_calls = parse_repository(files)

    graph = build_global_call_graph(all_functions, all_calls)

    errors = []
    warnings = []

    # reuse your existing checks
    errors += check_missing_functions(graph)
    errors += check_cycles(graph)
    errors += check_unused_functions(graph)

    metrics = {
        "num_files": len(files),
        "num_functions": len(all_functions),
        "num_edges": sum(len(v) for v in graph.values()),
        "num_errors": len(errors),
        "num_warnings": len(warnings),
    }

    return {
        "graph": graph,
        "functions": all_functions,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }
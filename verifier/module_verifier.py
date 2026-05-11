def verify_module(node, semantic_summary):

    errors = []
    imports = semantic_summary["imports"]
    allowed = set(node.depends_on)

    for imported in imports:
        root = imported.split(".")[0]
        if root not in allowed and root != node.name:
            errors.append(
                f"Forbidden dependency: {root}"
            )

    exported_functions = set(semantic_summary["functions"])

    for required_export in node.exports:
        if required_export not in exported_functions:
            errors.append(
                f"Missing export: {required_export}"
            )
            
    return errors
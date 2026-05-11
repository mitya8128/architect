from architecture.model import SemanticNode,RepositorySemanticModel


def compile_semantic_model(arch: dict) -> RepositorySemanticModel:

    system_name = arch["system"]["name"]
    nodes = {}
    modules = arch.get("modules", {})

    for module_name, module_data in modules.items():

        node = SemanticNode(
            name=module_name,
            role=module_data.get("role", "service"),
            description=module_data.get("description", ""),
            exports=module_data.get("exports", []),
            depends_on=module_data.get("depends_on", []),
            constraints=module_data.get("constraints", []),
        )

        nodes[module_name] = node

    return RepositorySemanticModel(
        system_name=system_name,
        nodes=nodes,
        global_constraints=arch.get(
            "global_constraints",
            []
        )
    )
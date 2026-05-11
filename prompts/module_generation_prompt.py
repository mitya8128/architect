def build_module_generation_prompt(current_node, generation_state):

    already_generated = list( generation_state.generated_modules.keys())

    return f'''
You are generating ONE Python module.

Generate ONLY valid Python code.

CURRENT MODULE:
{current_node.name}

ROLE:
{current_node.role}

DESCRIPTION:
{current_node.description}

EXPORTS:
{current_node.exports}

ALLOWED DEPENDENCIES:
{current_node.depends_on}

CONSTRAINTS:
{current_node.constraints}

ALREADY GENERATED MODULES:
{already_generated}

Rules:

1. Generate ONLY this module.
2. Do not generate unrelated code.
3. Use clean Python.
4. Respect dependency constraints.
5. Do not import unknown modules.
6. Export required functions.
7. Keep implementation minimal.
8. Prefer deterministic logic.

Output ONLY valid Python code.
'''
# def build_code_repair_prompt(code: str, errors: list, warnings: list) -> str:
#     return f"""
# You generated the following Python code:

# {code}

# The analyzer found issues:

# ERRORS:
# {chr(10).join(errors)}

# WARNINGS:
# {chr(10).join(warnings)}

# Fix the code while preserving functionality.

# Return ONLY valid Python code.
# """


def build_code_repair_prompt(code, error_map, warnings):

    syntax = error_map.get("syntax", [])
    semantic = error_map.get("semantic", [])
    architecture = error_map.get("architecture", [])

    return f"""
Fix the code with priority:

1. Syntax errors (CRITICAL)
{syntax}

2. Semantic errors
{semantic}

3. Architecture mismatches
{architecture}

Warnings:
{warnings}

Code:
{code}

Return ONLY valid Python code.
"""
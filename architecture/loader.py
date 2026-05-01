import yaml
from .model import Architecture, Module, Pipeline


def load_architecture(path: str) -> Architecture:

    with open(path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("YAML must define a dictionary at top level")

    # ---- TYPES ----
    raw_types = data.get("types", [])

    if isinstance(raw_types, list):
        types = set(raw_types)
    elif isinstance(raw_types, dict):
        types = set(raw_types.keys())
    else:
        types = set()

    # ---- MODULES ----
    raw_modules = data.get("modules", {})

    modules = {}
    for name, m in raw_modules.items():
        try:
            modules[name] = Module(
                name=name,
                input=m.get("input"),
                output=m.get("output"),
                description=m.get("description", "")
            )
        except Exception:
            continue  # skip broken modules

    # ---- PIPELINES (SAFE) ----
    raw_pipelines = data.get("pipelines", {})

    pipelines = {}
    if isinstance(raw_pipelines, dict):
        for name, mods in raw_pipelines.items():
            if isinstance(mods, list):
                pipelines[name] = Pipeline(name=name, modules=mods)

    # ---- SYSTEM NAME ----
    system_name = data.get("system", {}).get("name", "UnnamedSystem")

    return Architecture(
        name=system_name,
        types=types,
        modules=modules,
        pipelines=pipelines
    )
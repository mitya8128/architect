import yaml
from .model import Architecture, Module, Pipeline


def load_architecture(path: str) -> Architecture:

    with open(path) as f:
        data = yaml.safe_load(f)

    # support for list И dict
    raw_types = data["types"]

    if isinstance(raw_types, list):
        types = set(raw_types)
    elif isinstance(raw_types, dict):
        types = set(raw_types.keys())
    else:
        raise ValueError("Invalid types format")

    modules = {
        name: Module(
            name=name,
            input=m["input"],
            output=m["output"],
            description=m.get("description", "")
        )
        for name, m in data["modules"].items()
    }

    pipelines = {
        name: Pipeline(name=name, modules=mods)
        for name, mods in data["pipelines"].items()
    }

    return Architecture(
        name=data["system"]["name"],
        types=types,
        modules=modules,
        pipelines=pipelines
    )
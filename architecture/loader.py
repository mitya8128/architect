import yaml
from .model import Architecture, Module, Pipeline


def load_architecture(path: str) -> Architecture:

    with open(path) as f:
        data = yaml.safe_load(f)

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
        types=data["types"],
        modules=modules,
        pipelines=pipelines
    )
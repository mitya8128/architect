from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Module:
    name: str
    input: str
    output: str
    description: str = ""


@dataclass
class Pipeline:
    name: str
    modules: List[str]


@dataclass
class Architecture:
    name: str
    types: List[str]
    modules: Dict[str, Module]
    pipelines: Dict[str, Pipeline]
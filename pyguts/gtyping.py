import ast

from dataclasses import dataclass
from typing import (
    List,
    Literal,
)


@dataclass
class ModuleASTs:
    """
    Represents a module and its Abstract Syntax Trees (ASTs).
    """

    module_name: str
    asts: List[ast.Module]


MessageTypesFullName = Literal[
    "convention",
    "error",
    "fatal",
    "info",
    "refactor",
    "statement",
    "warning",
    "unacomplished",
]

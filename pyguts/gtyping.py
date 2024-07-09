import ast

from dataclasses import dataclass
from typing import (
    List,
    Literal,
    Tuple,
    TypedDict,
    Union,
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


class ExtraMessageOptions(TypedDict, total=False):
    """All allowed keys in the extra options for message definitions."""

    scope: str
    maxversion: tuple[int, int]
    minversion: tuple[int, int]
    shared: bool
    default_enabled: bool


MessageDefinitionTuple = Union[
    Tuple[str, str, str],
    Tuple[str, str, str, ExtraMessageOptions],
]

import ast

from dataclasses import dataclass

from typing import (
    List,
    Literal,
    Optional,
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
    file_path: str  # Relative path to the module
    absolute_path: str  # Absolute path to the module
    file_name: str  # File name of the module
    asts: Optional[List[ast.Module]]  # List of ASTs or None

    def __init__(
        self,
        module_name: str,
        file_path: str,
        absolute_path: str,
        file_name: str,
        asts: Optional[List[ast.Module]] = None,
    ) -> None:
        self.module_name = module_name
        self.file_path = file_path
        self.absolute_path = absolute_path
        self.file_name = file_name
        self.asts = asts


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


@dataclass
class MessageLocationTuple:
    """Tuple with information about the location of a to-be-displayed message."""

    abspath: str
    path: str
    obj: str
    module: str | None = None
    line: int | None = None
    column: int | None = None
    end_line: int | None = None
    end_column: int | None = None

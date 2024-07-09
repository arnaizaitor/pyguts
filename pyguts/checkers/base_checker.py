from astroid import nodes
from abc import ABC, abstractmethod

from pyguts.gtyping import (
    MessageDefinitionTuple,
    ModuleASTs,
)


class BaseChecker:
    """Base class for checkers."""

    name = "base-checker"
    msgs = {}

    def __init__(self, module_asts: ModuleASTs) -> None:
        self.filename = filename
        self.messages = dict[str, MessageDefinitionTuple] = {}

    def add_message(
        self,
        msg_id: str,
        node: nodes.Node | None = None,
        args: tuple[str, ...] = (),
        confidence: int = 0,
    ) -> None:
        self.messages.append((msg_id, node, args, confidence))

    @abstractmethod
    def run(self) -> list[tuple[str, nodes.Node | None, tuple[str, ...], int]]:
        """Run the checker and return the messages."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.filename})"

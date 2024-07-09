from astroid import nodes
from abc import ABC, abstractmethod

from pyguts.gtyping import (
    MessageDefinitionTuple,
    ModuleASTs,
)

from typing import (
    Any,
    List,
)


class BaseChecker(ABC):
    """Abstract Base class for checkers."""

    name = "base-checker"
    msgs = {}

    def __init__(self) -> None:
        pass

    # TODO: Check how its done in old_guts
    def add_message(
        self,
        msg_id: str,
        node: nodes.NodeNG | None = None,
        args: tuple[str, ...] = (),
        confidence: int = 0,
    ) -> None:
        self.messages.append((msg_id, node, args, confidence))

    @abstractmethod
    def check(self) -> None:
        """Run the checker and return the messages."""
        raise NotImplementedError

    @abstractmethod
    def register(self) -> None:
        """Register the checker."""
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.filename})"

    def __gt__(self, other: Any) -> bool:
        """Permits sorting checkers for stable doc and tests.

        The main checker is always the first one, then builtin checkers in alphabetical
        order, then extension checkers in alphabetical order.
        """
        if not isinstance(other, BaseChecker):
            return False
        if self.name == MAIN_CHECKER_NAME:
            return False
        if other.name == MAIN_CHECKER_NAME:
            return True
        self_is_builtin = type(self).__module__.startswith("pyguts.checkers")
        if self_is_builtin ^ type(other).__module__.startswith("pyguts.checkers"):
            return not self_is_builtin
        return self.name > other.name

    def __eq__(self, other: object) -> bool:
        """Permit to assert Checkers are equal."""
        if not isinstance(other, BaseChecker):
            return False
        return f"{self.name}{self.msgs}" == f"{other.name}{other.msgs}"

    def __hash__(self) -> int:
        """Make Checker hashable."""
        return hash(f"{self.name}{self.msgs}")

    def __repr__(self) -> str:
        status = "Checker" if self.enabled else "Disabled checker"
        msgs = "', '".join(self.msgs.keys())
        return f"{status} '{self.name}' (responsible for '{msgs}')"

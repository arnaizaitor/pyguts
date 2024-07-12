from astroid import nodes
from abc import ABC, abstractmethod

from pyguts.constants import MAIN_CHECKER_NAME
from pyguts.message.message import Message
from pyguts.message.message_store import MessageStore
from pyguts.message.message_id_store import MessageIdStore
from pyguts.gtyping import (
    MessageDefinitionTuple,
    MessageLocationTuple,
    ModuleASTs,
)
from pyguts.utils.file_state_handler import FileStateHandler
from pyguts.interfaces import (
    Confidence,
    HIGH,
    UNDEFINED,
)

from typing import (
    Any,
    List,
)


class BaseChecker(ABC):
    """Abstract Base class for checkers."""

    name = "base-checker"
    msgs = {}
    enabled = True
    __message_store: MessageStore = None
    __message_id_store: MessageIdStore = None

    def __init__(self) -> None:
        """Checker instances should have the guts as argument."""

        self.__message_store: MessageStore = MessageStore()
        self.__message_id_store: MessageIdStore = MessageIdStore()
        self.__file_state_handler: FileStateHandler = FileStateHandler()

        if self.name is not None:
            self.name = self.name.lower()

    # TODO: Check how its done in old_guts
    def add_message(
        self,
        msg_id: str,
        node: nodes.NodeNG | None = None,
        args: tuple[str, ...] = (),
        confidence: Confidence = UNDEFINED,
    ) -> None:

        file_state_handler: FileStateHandler = self.__file_state_handler
        line = col_offset = end_lineno = end_col_offset = None

        if node:
            if node.position:
                if not line:
                    line = node.position.lineno
                if not col_offset:
                    col_offset = node.position.col_offset
                if not end_lineno:
                    end_lineno = node.position.end_lineno
                if not end_col_offset:
                    end_col_offset = node.position.end_col_offset
            else:
                if not line:
                    line = node.fromlineno
                if not col_offset:
                    col_offset = node.col_offset
                if not end_lineno:
                    end_lineno = node.end_lineno
                if not end_col_offset:
                    end_col_offset = node.end_col_offset

        location: MessageLocationTuple = (
            file_state_handler.absolute_path,
            file_state_handler.file_path,
            file_state_handler.module_name,
            str(node),
            line,
            col_offset,
            end_lineno,
            end_col_offset,
        )

        message: Message = Message(
            msg_id,
            self.__message_id_store.get_symbol(msg_id),
            location,
            self.msgs[msg_id][0].format(*args),  # Message text with arguments resolved
            confidence,
        )

        self.__message_store.add_message(message)

    @abstractmethod
    def check(self) -> None:
        """Run the checker and return the messages."""
        raise NotImplementedError

    @property
    def is_enabled(self) -> bool:
        return self.enabled

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

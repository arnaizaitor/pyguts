import os
import ast
import astroid

from typing import Iterable, List
from collections import defaultdict

from pyguts.checkers import BaseChecker
from pyguts.constants import PY_EXTS, PYGUTS_HOME
from pyguts.utils.ast_walker import ASTWalker
from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger  # noqa: E402
from pyguts.message.message_id_store import MessageIdStore  # noqa: E402


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyGuts(
    ASTWalker,
):
    """Checks Python modules for Unacomplished Tool Specifications (GUTS)"""

    def __init__(self, base_dir: str) -> None:
        super().__init__(base_dir=base_dir)  # Initialize ASTWalker attributes
        self.base_dir = base_dir
        self._message_id_store: MessageIdStore = MessageIdStore()
        self._checkers: defaultdict[str, list[checkers.BaseChecker]] = defaultdict(list)

    def guts(self, recursive: bool = True) -> None:
        """
        Checks all Python files (.py) in the specified directory and its subdirectories
        for Unaccomplished Tool Specifications (GUTS).

        Args:
            directory (str): The root directory to start checking from.
            recursive (bool, optional): Whether to check recursively in subdirectories. Default is True.
        """

        module_asts: Iterable[ModuleASTs] = self._get_asts(self.base_dir, recursive)
        logger.debug(f"Found {len(module_asts)} modules to check")

        self.register_checkers()

        checkers = self.get_checkers()
        logger.debug(f"Registered checkers: {checkers}")

        for module_ast in module_asts:
            logger.debug(f"Checking module: {module_ast}")
            # TODO set current module info as attributes of some class
            self.walk(module_ast.asts[0])

    def register_checkers(self) -> None:
        """Registers all checkers in pyguts.checkers module"""

        for filename in os.listdir(os.path.join(PYGUTS_HOME, "pyguts", "checkers")):
            base, extension = os.path.splitext(filename)
            if extension in PY_EXTS and not (
                base.startswith("__") and base.endswith("__")
            ):
                try:
                    logger.debug(f"Loading checker from file: {filename}")
                    module = astroid.modutils.load_module_from_file(
                        os.path.join(PYGUTS_HOME, "pyguts", "checkers", filename)
                    )
                except ValueError:
                    # empty module name (usually Emacs auto-save files)
                    logger.warning(f"Failed to load checker from file: {filename}")
                    continue
                except ImportError as exc:
                    logger.error(f"Failed to load checker module: {filename}: {exc}")
                else:
                    if hasattr(module, "register"):
                        module.register(self)
                    else:
                        logger.error(
                            f"Checker module {module.__name__} does not have a register function"
                        )

    def register_checker(self, checker: BaseChecker) -> None:
        """Registers a checker in the PyGuts instance.

        Args:
            checker (BaseChecker): The checker to register.
        """

        logger.debug(f"Registering checker: '{checker.name}'...")
        self._checkers[checker.name].append(checker)

        # Register message ids and symbols
        if hasattr(checker, "msgs"):
            for msg_id, msg in checker.msgs.items():
                self._message_id_store.add_msgid_and_symbol(msg_id, msg[1])

        vcids: set[str] = set()
        lcids: set[str] = set()
        visits = self.visit_events
        leaves = self.leave_events

        # Register visit methods
        for member in dir(checker):
            cid = member[6:]
            if cid == "default":
                continue
            if member.startswith("visit_"):
                visit = getattr(checker, member)
                if callable(visit):
                    logger.debug(f"Registering visit method: {member} for checker: {checker.name}")
                    visits[cid].append(visit)
                    vcids.add(cid)
            if member.startswith("leave_"):
                leave = getattr(checker, member)
                if callable(leave):
                    logger.debug(f"Registering leave method: {member} for checker: {checker.name}")
                    leaves[cid].append(leave)
                    lcids.add(cid)


    def get_checkers(self) -> List[BaseChecker]:
        """Return all available checkers as an ordered list.

        Returns:
            List[BaseChecker]: An ordered list of all registered checkers.
        """

        return sorted(c for _checkers in self._checkers.values() for c in _checkers)

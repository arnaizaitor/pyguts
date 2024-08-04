import os
import ast
import astroid

from typing import Iterable, List
from collections import defaultdict

from pyguts.checkers import BaseChecker, NodeChecker, FileChecker, FileFinder
from pyguts.constants import PY_EXTS, PYGUTS_HOME
from pyguts.utils.ast_walker import ASTWalker
from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger
from pyguts.message.message_store import MessageStore
from pyguts.message.message_id_store import MessageIdStore
from pyguts.utils.file_state_handler import FileStateHandler
from pyguts.reporters.base_reporter import BaseReporter

from pprint import pprint, pformat


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyGuts(
    ASTWalker,
):
    """Checks Python modules for Unacomplished Tool Specifications (GUTS)"""

    def __init__(self, base_dir: str, reporter: BaseReporter) -> None:
        super().__init__(base_dir=base_dir)  # Initialize ASTWalker attributes
        self.base_dir = base_dir
        self.reporter = reporter

        self._message_store: MessageStore = MessageStore()
        self._message_id_store: MessageIdStore = MessageIdStore()
        self._file_state_handler: FileStateHandler = FileStateHandler()

        self._node_checkers: defaultdict[str, list[checkers.NodeChecker]] = defaultdict(
            list
        )
        self._file_checkers: defaultdict[str, list[checkers.FileChecker]] = defaultdict(
            list
        )
        self._file_finders: defaultdict[str, list[checkers.FileFinder]] = defaultdict(
            list
        )

    def guts(self, recursive: bool = True) -> None:
        """
        Checks all Python files (.py) in the specified directory and its subdirectories
        for Unaccomplished Tool Specifications (GUTS).

        Args:
            directory (str): The root directory to start checking from.
            recursive (bool, optional): Whether to check recursively in subdirectories. Default is True.
        """

        # Initialize FileStateHandler
        file_state_handler: FileStateHandler = self._file_state_handler

        # Get all ASTs of the modules in the specified directory and all the files separately
        module_asts: Iterable[ModuleASTs] = self._get_asts(recursive)
        all_files = self._discover_all_files(recursive)

        logger.debug(f"Found {len(module_asts)} modules to check.")
        logger.debug(f"Found {len(all_files)} files to check.")

        # Register all checkers
        self.register_checkers()

        # Get all registered NodeCheckers, FileCheckers and FileFinders
        node_checkers = self.get_node_checkers()
        logger.debug(f"Registered NodeCheckers: {node_checkers}")

        file_checkers = self.get_file_checkers()
        logger.debug(f"Registered FileCheckers: {file_checkers}")

        file_finders = self.get_file_finders()
        logger.debug(f"Registered FileFinders: {file_finders}")

        # Walk the ASTs of each module using the registered NodeCheckers
        for module_ast in module_asts:
            logger.debug(f"Checking module: {module_ast.module_name}")
            file_state_handler.set_current_file(module_ast)
            logger.critical(
                f"Current module info: {file_state_handler.get_current_file()}"
            )
            self.walk(module_ast.asts[0])

        # Call check method for each FileChecker over the list of all files
        for file_checker in file_checkers:
            for file_info in all_files:
                self._file_state_handler.set_current_file_from_tuple(file_info)
                file_checker.check(file_info)

        # Call check method for each FileFinder over the list of all files
        for file_finder in file_finders:
            logger.info(f"Checking files with checker: {file_finder.name}")
            file_finder.check(all_files)

        logger.info(
            f"Messages stored:\n\n {pformat(self._message_store.get_messages_sorted_by_location())}"
        )

        # Generate report
        self.reporter.report()

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

        logger.debug(f"Registering node checker: '{checker.name}'...")
        if isinstance(checker, NodeChecker):
            self._node_checkers[checker.name].append(checker)
        elif isinstance(checker, FileChecker):
            self._file_checkers[checker.name].append(checker)
        elif isinstance(checker, FileFinder):
            self._file_finders[checker.name].append(checker)
        else:
            logger.error(
                f"Checker {checker.name} is neither a NodeChecker nor a FileChecker nor a FileFinder"
            )

        # Register message ids and symbols
        if hasattr(checker, "msgs"):
            for msg_id, msg in checker.msgs.items():
                self._message_id_store.add_msgid_and_symbol(msg_id, msg[1])

        vcids: set[str] = set()
        lcids: set[str] = set()
        visits = self.visit_events
        leaves = self.leave_events

        # Only register visit and leave methods for NodeCheckers
        if checker.is_enabled and isinstance(checker, NodeChecker):
            # Register visit methods
            for member in dir(checker):
                cid = member[6:]
                if cid == "default":
                    continue
                if member.startswith("visit_"):
                    visit = getattr(checker, member)
                    if callable(visit):
                        logger.debug(
                            f"Registering visit method: {member} for checker: {checker.name}"
                        )
                        visits[cid].append(visit)
                        vcids.add(cid)
                if member.startswith("leave_"):
                    leave = getattr(checker, member)
                    if callable(leave):
                        logger.debug(
                            f"Registering leave method: {member} for checker: {checker.name}"
                        )
                        leaves[cid].append(leave)
                        lcids.add(cid)

    def get_node_checkers(self) -> List[NodeChecker]:
        """Return all available checkers as an ordered list.

        Returns:
            List[NodeChecker]: An ordered list of all registered NodeCheckers.
        """

        return sorted(
            c for _checkers in self._node_checkers.values() for c in _checkers
        )

    def get_file_checkers(self) -> List[FileChecker]:
        """Return all available checkers as an ordered list.

        Returns:
            List[FileChecker]: An ordered list of all registered FileCheckers.
        """

        return sorted(
            c for _checkers in self._file_checkers.values() for c in _checkers
        )

    def get_file_finders(self) -> List[FileFinder]:
        """Return all available FileFinder checkers as an ordered list.

        Returns:
            List[FileFinder]: An ordered list of all registered FileFinders.
        """

        return sorted(c for _checkers in self._file_finders.values() for c in _checkers)

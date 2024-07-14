from __future__ import annotations

from pyguts.checkers import FileFinder
from pyguts.interfaces import HIGH

from pyguts.logger.logger import logger

from typing import Tuple


class RequirementsFinderChecker(FileFinder):
    """Checker for requirements.txt file existance."""

    name = "requirements-finder-checker"
    msgs = {
        "G0008": (
            "No requirements.txt file found in the project.",
            "no-requirements-found",
        ),
    }

    def check(self, files_info: List[Tuple[str, str, str, str]]) -> None:
        # Empty the current file state
        self._file_state_handler.set_current_file_from_tuple(("", "", "", ""))

        requirements_exists = False
        for module_name, rel_path, abs_path, file_name in files_info:
            if file_name.lower() == "requirements.txt":
                return

        self.add_message(msg_symbol="no-requirements-found", confidence=HIGH)


def register(guts: PyGuts) -> None:
    guts.register_checker(RequirementsFinderChecker())

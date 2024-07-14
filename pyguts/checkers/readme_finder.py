from __future__ import annotations

from pyguts.checkers import FileFinder
from pyguts.interfaces import HIGH

from pyguts.logger.logger import logger

from typing import Tuple


class ReadmeFinderChecker(FileFinder):
    """Checker for Readme file existance."""

    name = "readme-finder-checker"
    msgs = {
        "G0006": (
            "No README file found in the project root.",
            "no-readme-found",
        ),
        "G0007": (
            "README file is empty.",
            "readme-found-empty",
        ),
    }

    def check(self, files_info: List[Tuple[str, str, str, str]]) -> None:
        logger.debug("Readme file finder is running...")
        self._file_state_handler.set_current_file_from_tuple(("", "", "", ""))
        for module_name, rel_path, abs_path, file_name in files_info:
            if file_name.lower() == "readme.md":
                # check if readme file is empty
                with open(abs_path, "r") as readme_file:
                    if not readme_file.read():
                        self.add_message(
                            msg_symbol="readme-found-empty",
                            filename=file_name,
                            confidence=HIGH,
                        )
                    else:
                        continue
        self.add_message(
            msg_symbol="no-readme-found", filename=file_name, confidence=HIGH
        )


def register(guts: PyGuts) -> None:
    guts.register_checker(ReadmeFinderChecker())

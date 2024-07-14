from __future__ import annotations

from pyguts.checkers import FileChecker
from pyguts.interfaces import HIGH

from pyguts.logger.logger import logger

from typing import Tuple

import re

class ReadmeFileChecker(FileChecker):
    """Checker for Readme file content."""

    name = "readme-checker"
    msgs = {
        "G0007": (
            "README file found at {} is empty.",
            "readme-found-empty",
        ),
    }

    def check(self, file_info: Tuple[str, str, str, str]) -> None:

        module_name, rel_path, abs_path, file_name = file_info
        if file_name.lower() == "readme.md":
            # check if readme file is empty
            with open(abs_path, "r") as readme_file:
                if not readme_file.read():
                    self.add_message(
                        msg_symbol="readme-found-empty",
                        filename=file_name,
                        confidence=HIGH,
                        args=(rel_path,),
                    )


def register(guts: PyGuts) -> None:
    guts.register_checker(ReadmeFileChecker())

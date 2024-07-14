from __future__ import annotations

from pyguts.checkers import FileChecker
from pyguts.interfaces import HIGH

from pyguts.logger.logger import logger

from typing import Tuple

import re

class RequirementsFileChecker(FileChecker):
    """Checker for Python requirements file content."""

    name = "requirements-checker"
    msgs = {
        "G0009": (
            "Requirements file found at {} is empty.",
            "requirements-found-empty",
        ),
        "G0010": (
            "Requirements file found at {} has an invalid structure.",
            "requirements-structure-invalid",
        ),
    }

    def check(self, file_info: Tuple[str, str, str, str]) -> None:

        module_name, rel_path, abs_path, file_name = file_info
        if file_name.lower() == "requirements.txt":
            # check if requirements file is empty
            with open(abs_path, "r") as requirements_file:
                if not requirements_file.read():
                    self.add_message(
                        msg_symbol="requirements-found-empty",
                        filename=file_name,
                        confidence=HIGH,
                        args=(rel_path,),
                    )
                # check requirements file correct structure
                else:
                    if not self.check_requirements_structure(abs_path):
                        self.add_message(
                            msg_symbol="requirements-structure-invalid",
                            filename=file_name,
                            confidence=HIGH,
                            args=(rel_path,),
                        )

    def check_requirements_structure(self, filename: str) -> bool:
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue  # Skip blank lines and comments

                    # Validate the structure using regular expression with optional spaces
                    pattern = r'^[a-zA-Z0-9_-]+\s*==\s*\d+\.\d+\.\d+$'
                    if not re.match(pattern, line):
                        raise ValueError(f"Invalid line: '{line}'")

            return True  # All lines are valid
        except FileNotFoundError:
            logger.error(f"Error: File '{filename}' not found.")
            return False
        except ValueError as e:
            logger.error(f"Error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False


def register(guts: PyGuts) -> None:
    guts.register_checker(RequirementsFileChecker())

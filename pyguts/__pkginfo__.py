# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""
This module exists for compatibility reasons.
TODO: Update via tbump, do not modify.
"""

from __future__ import annotations

__version__ = "0.1.0"


def get_numversion_from_version(v: str) -> tuple[int, int, int]:
    """
    Kept for compatibility reason.
    """
    version = v.replace("pyguts-", "")
    result_version = []
    for number in version.split(".")[0:3]:
        try:
            result_version.append(int(number))
        except ValueError:
            current_number = ""
            for char in number:
                if char.isdigit():
                    current_number += char
                else:
                    break
            try:
                result_version.append(int(current_number))
            except ValueError:
                result_version.append(0)
    while len(result_version) != 3:
        result_version.append(0)

    return tuple(result_version)  # type: ignore[return-value] # mypy can't infer the length


numversion = get_numversion_from_version(__version__)

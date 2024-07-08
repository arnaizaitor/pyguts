# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""Pyguts [options] modules_or_packages.

Check that module(s) satisfy a coding standard (and more !).

pyguts --help

Display this help message and exit.

pyguts --help-msg <msg-id>[,<msg-id>]

Display help messages about given message identifiers and exit.
"""
import sys

from pyguts.guts.run import Run

__all__ = [
    "Run",
]

if __name__ == "__main__":
    Run(sys.argv[1:])

# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

__all__ = ["__version__", "version", "modify_sys_path", "run_pyguts"]

import os
import sys
from collections.abc import Sequence

from pyguts.__pkginfo__ import __version__
from pyguts.logger.logger import logger  # noqa: E402


def run_pyguts(argv: Sequence[str] | None = None) -> None:
    """Run pyguts.

    argv can be a sequence of strings normally supplied as arguments on the command line
    """
    from pyguts.guts import Run as PygutsRun

    try:
        PygutsRun(argv or sys.argv[1:])
    except KeyboardInterrupt:
        logger.warning("pyguts interrupted by user")
        sys.exit(1)

def set_guts_path() -> None:
    """Set the path to the guts package in sys.path."""
    # Add the path to the guts root path in sys.path
    sys.path.insert(
        0,
        os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)
        ),
    )
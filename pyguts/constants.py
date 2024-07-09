import os
import sys
import astroid

from pyguts.__pkginfo__ import __version__
from pyguts.gtyping import MessageTypesFullName

full_version = f"""pyguts {__version__}
astroid {astroid.__version__}
Python {sys.version}"""

MAIN_CHECKER_NAME = "base-checker"

PY_EXTS = (".py", ".pyc", ".pyo", ".pyw", ".so", ".dll")

# TODO Redefine message types  # pylint: disable=fixme
MSG_TYPES: dict[str, MessageTypesFullName] = {
    "I": "info",
    "C": "convention",
    "R": "refactor",
    "W": "warning",
    "E": "error",
    "F": "fatal",
    "G": "unacomplished",
}
MSG_TYPES_LONG: dict[str, str] = {v: k for k, v in MSG_TYPES.items()}

def _get_pyguts_home() -> str:
    """Return the pyguts home."""
    return os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)
    )

PYGUTS_HOME = _get_pyguts_home()

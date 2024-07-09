# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""Utilities methods and classes for checkers.
TODO: Revisit this
Base id of standard checkers (used in msg and report ids):
01: base
02: classes
03: format
04: import
05: misc
06: variables
07: exceptions
08: similar
09: design_analysis
10: newstyle
11: typecheck
12: logging
13: string_format
14: string_constant
15: stdlib
16: python3 (This one was deleted but needs to be reserved for consistency with old messages)
17: refactoring
.
.
.
24: non-ascii-names
25: unicode
26: unsupported_version
27: private-import
28-50: not yet used: reserved for future internal checkers.
This file is not updated. Use
   script/get_unused_message_id_category.py
to get the next free checker id.

51-99: perhaps used: reserved for external checkers

The raw_metrics checker has no number associated since it doesn't emit any
messages nor reports. XXX not true, emit a 07 report !
"""

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pyguts.guts import PyGuts

from pyguts.logger.logger import logger  # noqa: E402

from pyguts.checkers.base_checker import BaseChecker

__all__ = ["BaseChecker"]
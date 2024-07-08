# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""Checks for magic values instead of literals."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pyguts.checkers import BaseChecker
from pyguts.interfaces import HIGH

if TYPE_CHECKING:
    from pyguts.guts import PyGuts

from pyguts.logger.logger import logger  # noqa: E402


class TemplateChecker(BaseChecker):
    """Checks for constants in comparisons."""

    name = "template-Checker"
    msgs = {
        "I9999": (
            "Message.",
            "message-symbol",
            "Description" "msg_options",
            {
                "default_enabled": False,
            },
        )
    }

    options = ()

    valid_magic_vals = (0, -1, 1, "", "__main__")

    def visit_assign(self, node: nodes.Assign) -> None:
        logger.debug("Visiting some node")
        self.add_message(
            "message-symbol",
            node=node,
            confidence=HIGH,
        )


def register(guts: PyGuts) -> None:
    guts.register_checker(TemplateChecker(guts))

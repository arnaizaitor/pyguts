# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""Checks for creation of virtual units."""

from __future__ import annotations

from typing import TYPE_CHECKING

from astroid import nodes

from pyguts.checkers import BaseChecker
# from pyguts.interfaces import HIGH

if TYPE_CHECKING:
    from pyguts.guts import PyGuts

from pyguts.logger.logger import logger  # noqa: E402


class VirtualUnitsChecker(BaseChecker):
    """Checker for detecting virtual unit creation."""

    name = "virtual-units-checker"

    msgs = {
        "G0004": (
            "Attempting to create virtual unit with 'subst' command",
            "virtual-unit-creation-subst",
            "Attempting to create a virtual unit using 'subst' command",
        ),
        "G0005": (
            "Attempting to create virtual unit with 'mount' command",
            "virtual-unit-creation-mount",
            "Attempting to create a virtual unit using 'mount' command",
        ),
    }

    options = ()

    def visit_call(self, node: nodes.Call) -> None:
        if isinstance(node.func, nodes.Attribute):
            if isinstance(node.func.expr, nodes.Name) and node.func.expr.name in [
                "subprocess",
                "os",
            ]:
                if isinstance(node.func.attrname, str) and node.func.attrname in [
                    "run",
                    "system",
                    "Popen",
                    "check_output",
                    "call",
                    "check_call",
                    "get_status_output",
                    "getoutput",
                    "getstatusoutput",
                ]:
                    for arg in node.args:
                        if isinstance(arg, nodes.List):
                            command = [
                                elt.value
                                for elt in arg.elts
                                if isinstance(elt, nodes.Const)
                            ]
                            logger.critical(f"Command: {command}")
                            if command and command[0].startswith("subst"):
                                self.add_message(
                                    "virtual-unit-creation-subst",
                                    node=node,
                                    confidence=HIGH,
                                )
                                logger.debug(
                                    "Attempting to create virtual unit with 'subst' command"
                                )
                            if (
                                command
                                and command[0] == "mount"
                                and "-t" in command
                                and "tmpfs" in command
                            ):
                                self.add_message(
                                    "virtual-unit-creation-mount",
                                    node=node,
                                    confidence=HIGH,
                                )
                                logger.debug(
                                    "Attempting to create virtual unit with 'mount' command"
                                )
                        elif isinstance(arg, nodes.Const):
                            if arg.value.startswith("subst"):
                                self.add_message(
                                    "virtual-unit-creation-subst",
                                    node=node,
                                    confidence=HIGH,
                                )
                                logger.debug(
                                    "Attempting to create virtual unit with 'subst' command"
                                )
                            if arg.value == "mount":
                                self.add_message(
                                    "virtual-unit-creation-mount",
                                    node=node,
                                    confidence=HIGH,
                                )

    def register(self, guts: PyGuts) -> None:
        guts.register_checker(VirtualUnitsChecker())

    def check(self) -> None:
        logger.debug("Checking for virtual unit creation...")

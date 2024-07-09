# For details: https://github.com/arnaizaitor/pyguts/blob/main/LICENSE
# Copyright (c) https://github.com/arnaizaitor/pyguts/blob/main/CONTRIBUTORS.txt

"""Checks for absolute paths assigned to variables."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from astroid import nodes

from pyguts.checkers import BaseChecker

# from pyguts.interfaces import HIGH

if TYPE_CHECKING:
    from pyguts.guts import PyGuts

from pyguts.logger.logger import logger  # noqa: E402


class AbsolutePathChecker(BaseChecker):
    """Checker for absolute paths in assignments."""

    name = "absolute-path-checker"
    msgs = {
        "G0001": (
            "Absolute path '%s' assigned to a variable, consider using a relative path or receive the path as script argument.",
            "absolute-path-assigned",
            "Using absolute paths in assignments can lead to issues with portability and flexibility of the code.",
        ),
        "G0002": (
            "Absolute path '%s' used as an argument, consider using a relative path or receive the path as script argument.",
            "absolute-path-used",
            "Using absolute paths as function arguments can lead to issues with portability and flexibility of the code.",
        ),
        "G0003": (
            "Concatenation results in absolute path '%s'. Consider using a relative path or a configuration method.",
            "absolute-path-from-binop",
            "Concatenating strings to form absolute paths can lead to issues with portability and flexibility of the code.",
        ),
    }

    def visit_assign(self, node: nodes.Assign) -> None:
        # Check all the assigned values in the node
        for assigned_value in (
            node.value.elts
            if isinstance(node.value, (nodes.Tuple, nodes.List))
            else [node.value]
        ):
            if (
                isinstance(assigned_value, nodes.Const)
                and isinstance(assigned_value.value, str)
                and os.path.isabs(assigned_value.value)
            ):
                logger.debug(f"Detected absolute path: {assigned_value.value}")
                self.add_message(
                    "absolute-path-assigned",
                    node=node,
                    args=(assigned_value.value,),
                    confidence=HIGH,
                )

    def visit_call(self, node: nodes.Call) -> None:
        # Check all arguments in function/method calls
        for argument in node.args:
            if (
                isinstance(argument, nodes.Const)
                and isinstance(argument.value, str)
                and os.path.isabs(argument.value)
            ):
                logger.debug(
                    f"Detected absolute path in function argument: {argument.value}"
                )
                self.add_message(
                    "absolute-path-used",
                    node=node,
                    args=(argument.value,),
                    confidence=HIGH,
                )

    def visit_binop(self, node: nodes.BinOp) -> None:
        # Check if the operation is an addition, commonly used for string concatenation
        logger.debug(
            f"Detected binary operation: {node.op.__class__.__name__} at line {node.lineno} of {node.root().name}"
        )
        if node.op == "+":
            logger.debug(f"Detected string concatenation: {node.left} + {node.right}")
            if self._is_string_concatenation(node.left, node.right):
                constructed_path = self._evaluate_concatenation(node.left, node.right)
                if os.path.isabs(constructed_path):
                    self.add_message(
                        "absolute-path-from-binop",
                        node=node,
                        args=(constructed_path,),
                        confidence=HIGH,
                    )

    def _is_string_concatenation(self, left, right):
        # Check if both sides of the operation are strings
        return (
            isinstance(left, nodes.Const)
            and isinstance(left.value, str)
            and isinstance(right, nodes.Const)
            and isinstance(right.value, str)
        )

    def _evaluate_concatenation(self, left, right):
        # Evaluate the concatenation of two string nodes
        return left.value + right.value

    def check(self) -> None:
        logger.debug("Checking for absolute paths existance...")


def register(guts: PyGuts) -> None:
    guts.register_checker(AbsolutePathChecker())

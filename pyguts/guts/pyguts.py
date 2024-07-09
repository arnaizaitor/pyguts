import os
import ast

from typing import Iterable, List

from pyguts.utils.ast_walker import ASTWalker
from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger  # noqa: E402


# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyGuts(ASTWalker):
    """Checks Python modules for Unacomplished Tool Specifications (GUTS)"""

    def __init__(self, base_dir: str) -> None:
        self.base_dir = base_dir

    def guts(self, recursive: bool = True) -> None:
        """
        Checks all Python files (.py) in the specified directory and its subdirectories
        for Unaccomplished Tool Specifications (GUTS).

        Args:
            directory (str): The root directory to start checking from.
            recursive (bool, optional): Whether to check recursively in subdirectories. Default is True.
        """

        module_asts: Iterable[ModuleASTs] = self._get_asts(self.base_dir, recursive)

        # TODO: Remove, only for demonstration purposes
        for module_ast in module_asts:
            print(f"************* Module {module_ast.module_name}")
            for ast_tree in module_ast.asts:
                self._print_classes_functions_methods(ast_tree)

    # TODO: Remove, only for demonstration purposes
    def _print_classes_functions_methods(self, tree: ast.Module) -> None:
        """
        Prints classes, functions, and methods found in the given AST (Abstract Syntax Tree).

        Args:
            tree (ast.Module): The Abstract Syntax Tree of a Python module.
        """

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                print(f"  Class: {node.name}")
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        print(f"    Function: {item.name}")
                    elif isinstance(item, ast.AsyncFunctionDef):
                        print(f"    Async Function: {item.name}")
                    elif isinstance(item, ast.MethodDef):
                        print(f"    Method: {item.name}")
            elif isinstance(node, ast.FunctionDef):
                print(f"  Function: {node.name}")
            elif isinstance(node, ast.AsyncFunctionDef):
                print(f"  Async Function: {node.name}")

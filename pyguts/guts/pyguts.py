import os
import ast

from typing import (
    Iterable,
    List
)

from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger  # noqa: E402

# pylint: disable=too-many-instance-attributes,too-many-public-methods
class PyGuts():
    """Checks Python modules for Unacomplished Tool Specifications (GUTS)
    """

    def __init__(self) -> None:
        self.base_directory = None

    def _discover_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Recursively finds all Python files (.py) in the specified directory and its subdirectories.

        Args:
            directory (str): The root directory to start searching from.
            recursive (bool, optional): Whether to search recursively in subdirectories. Default is True.

        Returns:
            List[str]: A list of absolute paths to the Python files found.
        """
        self.base_directory = directory

        python_files = []
        for root, _, files in os.walk(directory, topdown=True):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
            if not recursive:
                break  # Stop walking subdirectories if recursive=False
        return python_files

    def _get_ast(self, filename: str) -> ModuleASTs:
        """
        Parses the given Python module/file and returns its Abstract Syntax Tree (AST) representation.

        Args:
            filename (str): The path to the Python module/file.

        Returns:
            ModuleASTs: An instance of ModuleASTs containing the module name and its ASTs.
        """
        with open(filename, 'r') as file:
            source_code = file.read()
        ast_tree = ast.parse(source_code, filename=filename)

        # Get the relative path of the file from the root directory
        relative_path = os.path.relpath(filename, start=self.base_directory)  # Adjust the root directory as needed

        # Convert relative path to module name (examples.test)
        module_name = os.path.splitext(relative_path)[0].replace(os.path.sep, '.')  # Replace directory separators with dots
        if module_name.startswith('.'):
            module_name = module_name[1:]  # Remove leading dot if present

        return ModuleASTs(module_name=module_name, asts=[ast_tree])

    def _get_asts(self, directory: str, recursive: bool = True) -> List[ModuleASTs]:
        """
        Parses all Python files (.py) found in the specified directory and its subdirectories,
        and returns a list of ModuleASTs instances where each instance contains a module path and its ASTs.

        Args:
            directory (str): The root directory to start parsing from.
            recursive (bool, optional): Whether to parse recursively in subdirectories. Default is True.

        Returns:
            List[ModuleASTs]: A list of ModuleASTs instances representing each Python module and its ASTs.
        """

        python_files = self._discover_files(directory, recursive)
        module_asts = []

        for file in python_files:
            try:
                module_asts.append(self._get_ast(file))
            except Exception as e:
                print(f"Error parsing {file}: {e}")
        return module_asts

    def check(self, directory: str, recursive: bool = True) -> None:
        """
        Checks all Python files (.py) in the specified directory and its subdirectories
        for Unaccomplished Tool Specifications (GUTS).

        Args:
            directory (str): The root directory to start checking from.
            recursive (bool, optional): Whether to check recursively in subdirectories. Default is True.
        """

        module_asts: Iterable[ModuleASTs] = self._get_asts(directory, recursive)

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
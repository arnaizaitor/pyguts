import os
import ast

from typing import List

from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger  # noqa: E402


class ASTWalker:
    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir

    def _discover_files(self, recursive: bool = True) -> List[str]:
        """
        Recursively finds all Python files (.py) in the specified base directory and its subdirectories.

        Args:
            recursive (bool, optional): Whether to search recursively in subdirectories. Default is True.

        Returns:
            List[str]: A list of absolute paths to the Python files found.
        """

        python_files = []
        for root, _, files in os.walk(self.base_dir, topdown=True):
            for file in files:
                if file.endswith(".py"):
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
        with open(filename, "r") as file:
            source_code = file.read()
        ast_tree = ast.parse(source_code, filename=filename)

        # Get the relative path of the file from the root directory
        relative_path = os.path.relpath(
            filename, start=self.base_dir
        )  # Adjust the root directory as needed

        # Convert relative path to module name (examples.test)
        module_name = os.path.splitext(relative_path)[0].replace(
            os.path.sep, "."
        )  # Replace directory separators with dots
        if module_name.startswith("."):
            module_name = module_name[1:]  # Remove leading dot if present

        return ModuleASTs(module_name=module_name, asts=[ast_tree])

    def _get_asts(self, directory: str, recursive: bool = True) -> List[ModuleASTs]:
        """
        Parses all Python files (.py) found in the base directory and its subdirectories,
        and returns a list of ModuleASTs instances where each instance contains a module path and its ASTs.

        Args:
            directory (str): The root directory to start parsing from.
            recursive (bool, optional): Whether to parse recursively in subdirectories. Default is True.

        Returns:
            List[ModuleASTs]: A list of ModuleASTs instances representing each Python module and its ASTs.
        """

        python_files = self._discover_files(recursive)
        module_asts = []

        for file in python_files:
            try:
                module_asts.append(self._get_ast(file))
            except Exception as e:
                print(f"Error parsing {file}: {e}")
        return module_asts

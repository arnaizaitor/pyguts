import os
import astroid
from astroid import nodes
from collections import defaultdict

from typing import (
    List,
    Callable,
    Union,
)

from pyguts.gtyping import ModuleASTs
from pyguts.logger.logger import logger  # noqa: E402

# Callable parameter type NodeNG not completely correct.
# Due to contravariance of Callable parameter types,
# it should be a Union of all NodeNG subclasses.
# However, since the methods are only retrieved with
# getattr(checker, member) and thus are inferred as Any,
# NodeNG will work too.
AstCallback = Callable[[nodes.NodeNG], None]


class ASTWalker:
    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir
        self.visit_events: defaultdict[str, list[AstCallback]] = defaultdict(list)
        self.leave_events: defaultdict[str, list[AstCallback]] = defaultdict(list)

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

        try:
            ast_tree = astroid.parse(source_code)
        except astroid.exceptions.AstroidSyntaxError as e:
            # Handle parsing errors gracefully
            print(f"Error parsing {filename}: {e}")
            ast_tree = None

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

        return ModuleASTs(
            module_name=module_name,
            file_path=relative_path,
            absolute_path=os.path.abspath(filename),
            file_name=os.path.basename(filename),
            asts=[ast_tree] if ast_tree else [],
        )

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

    def walk(self, ast_node: nodes.NodeNG) -> None:
        """Call visit events of astroid checkers for the given node, recurse on
        its children, then leave events.
        """
        cid = ast_node.__class__.__name__.lower()

        # Detect if the node is a new name for a deprecated alias.
        # In this case, favour the methods for the deprecated
        # alias if any,  in order to maintain backwards
        # compatibility.
        visit_events: Sequence[AstCallback] = self.visit_events.get(cid, ())
        leave_events: Sequence[AstCallback] = self.leave_events.get(cid, ())

        logger.debug(f"Running walk on node: {ast_node.__class__.__name__.lower()}, node: {ast_node}")
        logger.debug(f"Visit events: {visit_events}, length: {len(visit_events)}")

        # pylint: disable = too-many-try-statements
        try:
            # if ast_node.is_statement:
            #     self.nbstatements += 1
            # generate events for this node on each checker
            for callback in visit_events:
                logger.debug(f"Running visit event: {callback.__name__}")
                callback(ast_node)
            # recurse on children
            for child in ast_node.get_children():
                self.walk(child)
            for callback in leave_events:
                callback(ast_node)
        except Exception:
            logger.error("Error walking the AST", exc_info=True)
            raise


from pyguts.utils.utils import singleton
from pyguts.logger.logger import logger
from pyguts.gtyping import ModuleASTs

from typing import Tuple

@singleton
class FileStateHandler:
    """Singleton class to store and manage currently analyzed files."""

    def __init__(self) -> None:
        """Initialize the file state handler."""
        self.module_name: str = ""
        self.file_path: str = ""
        self.absolute_path: str = ""
        self.file_name: str = ""

    @classmethod
    def set_current_file(cls, module_ast: ModuleASTs) -> None:
        """Set the currently analyzed file."""
        cls().module_name = module_ast.module_name
        cls().file_path = module_ast.file_path
        cls().absolute_path = module_ast.absolute_path
        cls().file_name = module_ast.file_name

    @classmethod
    def get_current_file(cls) -> Tuple[str, str, str, str]:
        """Return the information about the current analyzed file."""
        return (cls().file_name, cls().file_path, cls().absolute_path, cls().module_name)
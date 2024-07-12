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
    def set_current_file(self, module_ast: ModuleASTs) -> None:
        """Set the currently analyzed file."""
        self.module_name = module_ast.module_name
        self.file_path = module_ast.file_path
        self.absolute_path = module_ast.absolute_path
        self.file_name = module_ast.file_name

    @classmethod
    def get_current_file(self) -> Tuple[str, str, str, str]:
        """Return the information about the current analyzed file."""
        return (
            self.file_name,
            self.file_path,
            self.absolute_path,
            self.module_name,
        )

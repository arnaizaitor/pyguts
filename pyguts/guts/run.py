import os
import sys
import argparse

from collections.abc import Sequence
from pyguts.guts.pyguts import PyGuts
from pyguts.constants import full_version

from pyguts.logger.logger import logger  # noqa: E402

class Run:
    """Helper class to use as main for pyguts with 'run(*sys.argv[1:])'."""

    GutsClass = PyGuts

    def __init__(
        self,
        args: Sequence[str]
    ) -> None:
        # Initialize argument parser
        parser = argparse.ArgumentParser(description="Run pyguts with optional directory and recursive options")

        # Add optional arguments
        parser.add_argument('-d', '--dir', metavar='DIRECTORY', default='.',
                            help='Directory path to check (default: current directory)')
        parser.add_argument('-r', '--recursive', action='store_true',
                            help='Enable recursive directory search')
        parser.add_argument('-v', '--version', action='store_true',
                            help='Show pyguts version and exit')

        # Parse arguments
        parsed_args = parser.parse_args(args)

        # Show version and exit if --version or -v is passed
        if parsed_args.version:
            print(full_version)
            sys.exit(0)

        # Initialize PyGuts instance
        self.guts = guts = self.GutsClass()

        # Set directory path and recursive option
        self.directory_to_check = parsed_args.dir
        self.recursive = parsed_args.recursive

        # Run the guts with the specified directory and recursive options
        if os.path.isdir(self.directory_to_check) and os.path.exists(self.directory_to_check):
            guts.check(self.directory_to_check, recursive=self.recursive)
        else:
            logger.error(f"Directory '{self.directory_to_check}' does not exist or is not valid.")
            sys.exit(1)

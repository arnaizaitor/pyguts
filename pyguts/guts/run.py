import os
import sys
import argparse

from collections.abc import Sequence
from pyguts.guts.pyguts import PyGuts
from pyguts.reporters.json_reporter import JsonReporter
from pyguts.reporters.simple_text_reporter import SimpleTextReporter
from pyguts.constants import full_version

from pyguts.logger.logger import logger


class Run:
    """Helper class to use as main for pyguts with 'run(*sys.argv[1:])'."""

    GutsClass = PyGuts
    ReporterClass = None

    def __init__(self, args: Sequence[str]) -> None:
        # Initialize argument parser
        parser = argparse.ArgumentParser(
            description="Run pyguts with optional directory and recursive options"
        )

        # Add optional arguments
        parser.add_argument(
            "-d",
            "--dir",
            metavar="DIRECTORY",
            required=True,
            help="Directory path to check (default: current directory)",
        )
        parser.add_argument(
            "-r",
            "--recursive",
            action="store_true",
            help="Enable recursive directory search",
        )
        parser.add_argument(
            "-v", "--version", action="store_true", help="Show pyguts version and exit"
        )
        parser.add_argument(
            '-o', 
            '--output',
            metavar='OUTPUT_DIR',
            required=True, 
            help='Directory to store the generated report.'
        )
        parser.add_argument(
            '-f', '--format', required=True, choices=['json', 'txt'], help='Format of the report to generate (json or txt).'
        )

        # Parse arguments
        parsed_args = parser.parse_args(args)

        # Show version and exit if --version or -v is passed
        if parsed_args.version:
            print(full_version)
            sys.exit(0)

        # Set directory path and recursive option
        self.directory_to_check = parsed_args.dir
        self.recursive = parsed_args.recursive
        self.output_dir = parsed_args.output
        self.format = parsed_args.format

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        ReporterClass = SimpleTextReporter if self.format == 'txt' else JsonReporter

        # Run the guts with the specified directory and recursive options
        if os.path.isdir(self.directory_to_check) and os.path.exists(
            self.directory_to_check
        ):
            # Initialize PyGuts instance
            self.guts = guts = self.GutsClass(self.directory_to_check, reporter=ReporterClass(self.output_dir))
            # Initialize FileStateHandler instance
            logger.debug(f"Initializing FileStateHandler...")

            # Run PyGuts
            guts.guts(recursive=self.recursive)
        else:
            logger.error(
                f"Directory '{self.directory_to_check}' does not exist or is not valid."
            )
            sys.exit(1)

"""
Main module for my_python_tool
"""

import os
import sys

# Add the base directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import argparse  # noqa: E402
from src.logger import configure_logger  # noqa: E402


def main():
    """
    Main function to run the tool
    """
    parser = argparse.ArgumentParser(description="Run my Python tool.")
    parser.add_argument(
        "--log_file", type=str, help="Path to the log file", default=None
    )
    args = parser.parse_args()

    # Configure logger
    logger = configure_logger(args.log_file)
    logger.info("Starting the tool...")

    # Add your tool code here

    logger.info("Finishing the tool execution...")
    config_path = "/etc/config/settings.conf"  # This should trigger R9999


if __name__ == "__main__":
    main()

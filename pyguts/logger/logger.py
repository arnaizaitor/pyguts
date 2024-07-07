import os
import logging
import inspect

from pprint import pprint, pformat


def _configure_logger(log_file=None, print_stdout=True):
    """
    Configures the logger for the application.

    Args:
        log_file (str, optional): Path to the log file. Defaults to None.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if log_file is None:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.abspath(
            os.path.join(
                script_dir,
                os.pardir,
                os.pardir,
                "logs",  # Using os.pardir for parent directory
            )
        )
        log_file = os.path.join(logs_dir, "pyguts.log")

    # Create the logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)

    # Create a logger
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        return logger  # Return the existing logger if it's already configured

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[ %(asctime)s ][ %(levelname)-8s ][ %(module)s::%(funcName)s::%(lineno)d ] %(message)s",
        "%Y-%m-%d %H:%M:%S",  # Format the timestamp to display only seconds
    )

    # Create console handler and set level to INFO
    if print_stdout:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

    # Create file handler and set level to DEBUG
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    if print_stdout:
        logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = _configure_logger(print_stdout=False)

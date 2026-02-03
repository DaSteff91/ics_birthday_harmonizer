"""
Configuration module for the Birthday Harmonizer.
Contains global constants, strategic defaults, and logging setup.
"""

import logging

# Strategic Constants
SENTINEL_YEAR = 1604  # Leap year for unknown birthdays
DEFAULT_ALARM_HOURS = 9  # 9:00 AM

# Logging Configuration
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    """
    Initializes the global logging configuration.

    Sets the log level and format for the entire application based on
    predefined constants. This should be called once at the start
    of the script execution.
    """
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

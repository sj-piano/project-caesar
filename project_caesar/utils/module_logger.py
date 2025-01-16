# Goal: A custom logger per module.


# Imports
import os
import logging


# Components
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, validate_call


# Local imports
from .. import config
from ..utils.misc import stop


# Future:
#import importlib.util
#colorlog_imported = importlib.util.find_spec("colorlog") is not None


# Non-standard-library imports
colorlog_imported = False
try:
  import colorlog  # type: ignore
  colorlog_imported = True
except Exception as e:
  colorlog_imported = False


# Future: Import from constants.py


class LogLevelStringEnum(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


LOG_LEVEL_STRINGS = [level.value for level in LogLevelStringEnum]


# Dynamically generate a mapper dict from the enum and the logging module.
# Example entry: 'info': logging.INFO
MAP_LOG_LEVEL_STRING_TO_LEVEL = {
    level.value: getattr(logging, level.name)
    for level in LogLevelStringEnum
}


class LoggerConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    logger_name: str = Field(..., description="The name of the logger (usually the path to the module file).")
    log_level: LogLevelStringEnum = Field(
        config.log_level,
        description="Log level for the logger.",
    )
    debug: bool = Field(False, description="Force debug log level.")
    log_timestamp: Optional[bool] = Field(
        False, description="Include timestamps in log messages."
    )
    log_file: Optional[str] = Field(
        None, description="Path to the log file if file logging is specified."
    )

    @staticmethod
    def from_defaults(logger_name: str) -> "LoggerConfig":
        """Initialize LoggerConfig using default settings."""
        return LoggerConfig(logger_name=logger_name)


@validate_call
def create_logger(logger_name: str):
    """Create and configure a logger with default settings."""
    # We typically pass in the module file path as the logger name.
    # We try to remove the first part of the path to make the logger name more readable.
    # Example: The logger name
    # '/home/admin/project-caesar/scripts/generate_secret_key.py'
    # becomes
    # 'scripts/generate_secret_key.py'
    try:
        logger_name = logger_name.split(config.repo_dir_name + "/", 1)[1]
    except ValueError:
        pass

    logger = logging.getLogger(logger_name)

    # Add a handler if there isn't one already.
    # - this NullHandler is only needed to prevent propagation. if we've set propagate to false, maybe this isn't needed ?
    #if not logger.handlers:
        #logger.addHandler(logging.NullHandler())

    # Get default config and configure the logger
    default_config = LoggerConfig.from_defaults(logger_name)
    configure_logger(logger, default_config)

    # Return logger and shortcuts
    log = logger.info
    deb = logger.debug
    return logger, log, deb


def configure_logger(logger: logging.Logger, logger_config: LoggerConfig):
    """Configure a logger using a LoggerConfig."""
    # Determine the log level
    level_str = logger_config.log_level
    if logger_config.debug:
        level_str = 'debug'

    level = MAP_LOG_LEVEL_STRING_TO_LEVEL[level_str]
    logger.setLevel(level)
    logger.propagate = False

    # Store the log level as a string.
    logger.log_level = level_str

    # Log format
    log_format = f"[{logger_config.logger_name}: %(lineno)s (%(funcName)s)] %(message)s"
    if logger_config.log_timestamp:
        log_format = "%(asctime)s " + log_format
    log_format = f"%(levelname)-8s {log_format}"
    log_formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

    # Add colored formatter if available
    log_formatter2 = None
    if colorlog_imported:
        log_format_color = log_format.replace('%(levelname)-8s ', '%(log_color)s%(levelname)-8s %(baseline_log_color)s')
        log_format_color = log_format_color.replace('%(message)', '%(message_log_color)s%(message)')
        log_formatter2 = colorlog.ColoredFormatter(
            log_format_color,
            datefmt='%Y-%m-%d %H:%M:%S',
            reset=True,
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={
                'baseline': {'DEBUG': 'white', 'INFO': 'white', 'WARNING': 'white', 'ERROR': 'white', 'CRITICAL': 'white'},
                'message': {'DEBUG': 'blue', 'INFO': 'white', 'WARNING': 'white', 'ERROR': 'white', 'CRITICAL': 'white'},
            },
        )

    # Configure console handler
    if not colorlog_imported:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
    else:
        console_handler2 = colorlog.StreamHandler()
        console_handler2.setLevel(level)
        console_handler2.setFormatter(log_formatter2)
        logger.addHandler(console_handler2)

    # Configure file handler if a log file is specified
    if logger_config.log_file:
        os.makedirs(os.path.dirname(logger_config.log_file), exist_ok=True)
        file_handler = logging.FileHandler(logger_config.log_file, mode="a", delay=True)
        file_handler.setLevel(level)
        file_handler.setFormatter(log_formatter if not colorlog_imported else log_formatter2)
        logger.addHandler(file_handler)

    # Add convenience method to update log level
    def setLevelStr(level_str: str):
        logger.setLevel(MAP_LOG_LEVEL_STRING_TO_LEVEL[level_str])

    logger.setLevelStr = setLevelStr

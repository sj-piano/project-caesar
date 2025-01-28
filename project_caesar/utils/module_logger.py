# Goal: A custom logger per module.


# Imports
import argparse
import os
import logging


# Components
from typing import Callable, Optional, Self, Tuple
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, field_validator, validate_call


# Local imports
from .. import config
from .. import constants
from ..utils.misc import stop


# Dynamically import colorlog if available
import importlib
colorlog_spec = importlib.util.find_spec("colorlog")
colorlog = None
colorlog_imported = False
if colorlog_spec:
    colorlog = importlib.import_module("colorlog")
    colorlog_imported = True




class LoggerConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    logger_name: Optional[str] = Field(None, description="The name of the logger (usually the path to the module file).")
    log_level: constants.LogLevelStringEnum = Field(
        config.log_level,
        description="Log level for the logger.",
    )
    debug: bool = Field(False, description="Force debug log level.")
    log_timestamp: Optional[bool] = Field(
        False, description="Include timestamps in log messages."
    )
    log_to_file: Optional[bool] = Field(
        False, description="Whether to save log output to a file."
    )
    log_file: Optional[Path] = Field(None, description="Path to the log file.")

    @field_validator("log_file")
    @classmethod
    def validate_log_file(cls, v: Optional[Path]) -> Optional[Path]:
        if v:
            if v.is_dir():
                raise ValueError(f"Log file path '{v}' is a directory, expected a file.")
            if not v.parent.exists():
                raise ValueError(f"Log file directory '{v.parent}' does not exist.")
        return v

    @staticmethod
    def from_defaults() -> Self:
        """Initialize LoggerConfig using default settings."""
        return LoggerConfig()




class ArgsModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    args: argparse.Namespace

    @field_validator("args")
    @classmethod
    def validate_args(cls, v):
        if not isinstance(v, argparse.Namespace):
            raise ValueError(f"Expected 'argparse.Namespace', got '{type(v).__name__}'")
        return v




def configure_logger_from_args(logger, args):
    """Configure a logger using an argparse namespace."""
    validated_args = ArgsModel(args=args)
    args2 = validated_args.args
    field_names = LoggerConfig.model_fields.keys()
    fields = {k: args2.__dict__.get(k) for k in field_names}
    logger_config = LoggerConfig(**fields)
    configure_logger(logger, logger_config)


@validate_call
def create_logger(
    logger_name: str,
) -> Tuple[logging.Logger, Callable[..., None], Callable[..., None]]:
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
    default_config = LoggerConfig.from_defaults()
    configure_logger(logger, default_config)

    # Return logger and shortcuts
    log = logger.info
    deb = logger.debug
    return logger, log, deb


def configure_logger(logger: logging.Logger, logger_config: LoggerConfig):
    """Configure a logger using a LoggerConfig."""

    # Determine the logger name.
    if logger_config.logger_name:
        logger.name = logger_config.logger_name

    # Determine the log level
    level_str = logger_config.log_level
    if logger_config.debug:
        level_str = 'debug'

    level = constants.MAP_LOG_LEVEL_STRING_TO_LEVEL[level_str]
    logger.setLevel(level)
    logger.propagate = False

    # Store the log level as a string.
    logger.log_level = level_str

    # Log format
    log_format = f"[{logger.name}: %(lineno)s (%(funcName)s)] %(message)s"
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
                'baseline': {
                    'DEBUG': 'white',
                    'INFO': 'white',
                    'WARNING': 'white',
                    'ERROR': 'white',
                    'CRITICAL': 'white'
                },
                'message': {
                    'DEBUG': 'blue',
                    'INFO': 'white',
                    'WARNING': 'white',
                    'ERROR': 'white',
                    'CRITICAL': 'white',
                },
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
    if logger_config.log_to_file and logger_config.log_file:
        parent_dir = os.path.dirname(logger_config.log_file)
        # If the log file is in the current directory, parent_dir will be empty string.
        # Ensure it exists if not empty.
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        file_handler = logging.FileHandler(logger_config.log_file, mode="a", delay=True)
        file_handler.setLevel(level)
        file_handler.setFormatter(log_formatter if not colorlog_imported else log_formatter2)
        logger.addHandler(file_handler)

    # Add convenience method to update log level
    def setLevelStr(level_str: str):
        logger.setLevel(constants.MAP_LOG_LEVEL_STRING_TO_LEVEL[level_str])

    logger.setLevelStr = setLevelStr


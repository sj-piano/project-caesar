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
from project_caesar.configuration import config
from project_caesar import constants
from project_caesar.utils.misc import stop


# Dynamically import colorlog if available
import importlib
colorlog_spec = importlib.util.find_spec("colorlog")
colorlog = None
colorlog_imported = False
if colorlog_spec:
    colorlog = importlib.import_module("colorlog")
    colorlog_imported = True



# Constants
MAP_LEVEL_NAME_TO_LEVEL = logging.getLevelNamesMapping()
# {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}
MAP_LEVEL_NAME_TO_LEVEL = {k.lower(): v for k, v in MAP_LEVEL_NAME_TO_LEVEL.items()}
MAP_LEVEL_TO_LEVEL_NAME = {v: k for k, v in MAP_LEVEL_NAME_TO_LEVEL.items()}




class LoggerConfig(BaseModel):


    model_config = ConfigDict(validate_assignment=True)

    logger_name: Optional[str] = Field(None, description="The name of the logger (usually the path to the module file).")
    log_level: constants.LogLevelNameLiteral = Field(
        config.log_level,
        description="Log level name (lowercase) for the logger.",
    )
    debug: bool = Field(config.debug, description="Force debug log level.")
    log_timestamp: Optional[bool] = Field(
        config.log_timestamp,
        description="Include timestamps in log messages.",
    )
    log_to_file: Optional[bool] = Field(
        config.log_to_file,
        description="Whether to save log output to a file.",
    )
    log_file: Optional[Path] = Field(config.log_file, description="Path to the log file.")


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




def configure_all_package_loggers_from_args(args):
    logger_config = get_config_from_args(args)
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if not hasattr(logger, 'log_level'):
            continue
        if logger.log_level == 'notset':
            continue
        start = logger.name.split('.')[0]
        if start not in constants.TOP_LEVEL_DIR_NAMES:
            continue
        configure_logger(logger, logger_config)
        msg = f"Logger configured: {logger.name} - level={logger.log_level}"
        #print(msg)


def configure_logger_from_args(logger, args):
    logger_config = get_config_from_args(args)
    configure_logger(logger, logger_config)


def get_config_from_args(args):
    """Get a LoggerConfig object from an argparse namespace."""
    validated_args = ArgsModel(args=args)
    args2 = validated_args.args
    field_names = LoggerConfig.model_fields.keys()
    fields = {k: args2.__dict__.get(k) for k in field_names}
    return LoggerConfig(**fields)


class CustomLogger(logging.Logger):

    @property
    def log_level(self):
        log_level_name = MAP_LEVEL_TO_LEVEL_NAME[self.level]
        return log_level_name

    @log_level.setter
    def log_level(self, log_level_name):
        """Allows setting the log level using a string (e.g., logger.log_level = 'debug')."""
        level = MAP_LEVEL_NAME_TO_LEVEL[log_level_name]
        self.setLevel(level)


# Set the custom logger class to be used by logging.getLogger()
logging.setLoggerClass(CustomLogger)


@validate_call
def create_logger(
    logger_name: str,
) -> Tuple[CustomLogger, Callable[..., None], Callable[..., None]]:
    """Create and configure a logger with default settings."""
    # We pass in the module file path as the logger name.
    # We avoid using the __name__ variable because it is not always the module file path (it can be '__main__').
    # Nonetheless we want to mimic the normal logger name hierarchy.
    # We process the file path to get a more readable logger name.
    # Example: The logger name
    # '/home/admin/project-caesar/scripts/generate_secret_key.py'
    # becomes
    # 'scripts.generate_secret_key'
    if logger_name[-3:] == '.py':
        logger_name = logger_name[:-3]
    start = constants.REPO_DIR_NAME + '/'
    if start in logger_name:
        logger_name = logger_name.split(start, 1)[1]
    logger_name = logger_name.replace('/', '.')

    logger = logging.getLogger(logger_name)

    # Add a default NullHandler.
    # This prevents the logger from propagating messages to the root logger.
    # - Also, it prevents the "No handlers could be found for logger" warning.
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    # Get default config and configure the logger
    default_config = LoggerConfig.from_defaults()
    configure_logger(logger, default_config)

    # Return logger and shortcuts
    log = logger.info
    deb = logger.debug
    return logger, log, deb


def configure_logger(logger: CustomLogger, logger_config: LoggerConfig):
    """Configure a logger using a LoggerConfig."""

    # Determine the logger name.
    if logger_config.logger_name:
        logger.name = logger_config.logger_name

    # Determine the log level
    log_level_name = logger_config.log_level
    if logger_config.debug:
        log_level_name = 'debug'

    level_value = MAP_LEVEL_NAME_TO_LEVEL[log_level_name]

    # Set the level.
    logger.log_level = log_level_name
    logger.propagate = False

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
        console_handler.setLevel(level_value)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)
    else:
        console_handler2 = colorlog.StreamHandler()
        console_handler2.setLevel(level_value)
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
        file_handler.setLevel(level_value)
        file_handler.setFormatter(log_formatter if not colorlog_imported else log_formatter2)
        logger.addHandler(file_handler)


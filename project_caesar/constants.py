# Imports
import logging


# Components
from enum import Enum


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


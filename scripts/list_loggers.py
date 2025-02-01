# Imports
import logging


# Local imports
from project_caesar.utils import arguments, module_logger


# Logger
logger, log, deb = module_logger.create_logger(__file__)


def list_active_loggers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

    s = 'Active Loggers:'
    for logger in loggers:
        s += f"\n- {logger.name}: {logging.getLevelName(logger.level)}"

    print(s)

list_active_loggers()
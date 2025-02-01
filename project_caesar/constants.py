# Imports


# Components
from typing import get_args, Literal


# Types
LogLevelNameLiteral = Literal['debug', 'info', 'warning', 'error', 'critical']


# Constants
REPO_DIR_NAME = 'project-caesar'
TOP_LEVEL_PACKAGE_DIR_NAME = 'project_caesar'
SCRIPT_DIR_NAME = 'scripts'


# Derived
LOG_LEVEL_NAMES = list(get_args(LogLevelNameLiteral))
TOP_LEVEL_DIR_NAMES = [TOP_LEVEL_PACKAGE_DIR_NAME, SCRIPT_DIR_NAME]


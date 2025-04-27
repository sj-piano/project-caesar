# Components
from pydantic import BaseModel, ConfigDict
from typing import Final, Any


# Local imports
from . import constants


# Defaults
# - Future: Retrieve from .env file ?
DEFAULT_LOG_LEVEL = 'info'
DEFAULT_DEBUG = False
DEFAULT_LOG_TIMESTAMP = False
DEFAULT_LOG_TO_FILE = False
DEFAULT_LOG_FILE = 'log.txt'


class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True, frozen=True)

    log_level: constants.LogLevelNameLiteral
    debug: bool
    log_timestamp: bool
    log_to_file: bool
    log_file: str

    @classmethod
    def from_args(cls, args: Any) -> 'Config':
        """
        Create a new Config instance from command line arguments.
        
        Args:
            args: An object containing configuration arguments (typically from argparse)
            
        Returns:
            A new Config instance with the loaded arguments
        """
        return cls(
            log_level=args.log_level,
            debug=args.debug,
            log_timestamp=args.log_timestamp,
            log_to_file=args.log_to_file,
            log_file=args.log_file,
        )


# Create and validate the config
# This can now be imported e.g.:
# from project_caesar.configuration import config
config: Final[Config] = Config(
    log_level=DEFAULT_LOG_LEVEL,
    debug=DEFAULT_DEBUG,
    log_timestamp=DEFAULT_LOG_TIMESTAMP,
    log_to_file=DEFAULT_LOG_TO_FILE,
    log_file=DEFAULT_LOG_FILE,
) 
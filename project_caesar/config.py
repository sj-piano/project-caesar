# Components
from pydantic import BaseModel, ConfigDict


# Local imports
from . import constants


# Defaults
# - Future: Store in .env file ?
log_level ='error'
debug = False
log_timestamp = False
log_to_file = False
log_file = 'log.txt'


class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    log_level: constants.LogLevelNameLiteral
    debug: bool
    log_file: str


# Validate the config values
config_dict = {
    'log_level': log_level,
    'debug': debug,
    'log_file': log_file,
}
config_validated = Config(**config_dict)


# You can now import the validated config. E.g.
# from ..config import config


def load_args(a):
    """
    Load arguments into the config.
    """
    log_level = a.log_level
    debug = a.debug
    log_file = a.log_file


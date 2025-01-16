# Components
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Literal


# Local imports
from . import constants


# Controls
log_level ='error'


# Settings
repo_dir_name = 'project-caesar'


class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    log_level: constants.LogLevelStringEnum
    repo_dir_name: str

    @field_validator('repo_dir_name')
    def validate_repo_dir_name(cls, value):
        if not value.strip():
            raise ValueError("repo_dir_name cannot be empty or only whitespace.")
        return value


config_dict = {
    "log_level": log_level,
    "repo_dir_name": repo_dir_name,
}


# Validate the config values
config = Config(**config_dict)


# You can now import the validated config. E.g.
# from ..config import config


# Imports
import argparse


# Local imports
from project_caesar.code import secret_key
from project_caesar.utils import arguments, module_logger


# Arguments
parser = argparse.ArgumentParser(
    description="Generate a secret key.",
    parents=[arguments.get_common_parser()]
)
a = parser.parse_args()


# Process arguments
logger_aspect_names = 'log_level log_file'.split()  # Future: Move to config.
logger_aspects = {k: a.__dict__.get(k) for k in logger_aspect_names}


# Logger
logger, log, deb = module_logger.create_logger(__file__)
logger_config = module_logger.LoggerConfig(**logger_aspects)
module_logger.configure_logger(logger, logger_config)


# Run
if __name__ == "__main__":
    sk = secret_key.generate_secret_key()
    log(f"Generated secret key: {sk}")
    print(sk.value)


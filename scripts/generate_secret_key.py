# Imports
import argparse


# Local imports
from project_caesar.configuration import Config
from project_caesar.code import secret_key
from project_caesar.utils import arguments, module_logger


# Arguments
parser = argparse.ArgumentParser(
    description="Generate a secret key.",
    parents=[arguments.get_common_parser()]
)
a = parser.parse_args()


# Config
config = Config.from_args(a)


# Logger
logger, log, deb = module_logger.create_logger(
    __file__,
    config=config,
    configure_all=True,
)


# Run
if __name__ == "__main__":
    sk = secret_key.generate_secret_key()
    deb(f"Args: {a}")
    log(f"Generated secret key: {sk}")
    print(sk.value)


# Local imports
from project_caesar.code import secret_key
from project_caesar.utils import module_logger


# Logger
logger, log, deb = module_logger.create_logger(__file__)


if __name__ == "__main__":
    sk = secret_key.generate_secret_key()
    log(f"Generated secret key: {sk}")
    print(sk.value)


# Local imports
from ..utils import module_logger


# Logger
logger, log, deb = module_logger.create_logger(__file__)


def hello_world():
    log('hello world')
    return 'hello world'


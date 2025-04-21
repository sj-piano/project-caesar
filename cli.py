# Local imports
from project_caesar.code import address, block
from project_caesar.utils import module_logger


# Local components
from project_caesar.code.genesis import get_genesis_block
from project_caesar.code.node import Node
from project_caesar.utils.misc import stop


# Logger
logger, log, deb = module_logger.create_logger(__file__)
logger.log_level = 'debug'


# Run
print(logger.log_level)
log('hello')
stop()


block_0 = get_genesis_block()
print(block_0.text)
print(block_0.hex_values)
print(block_0.hex)
print(block_0.hash)


#node = Node()

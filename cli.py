# Local imports
from project_caesar.code import address, block


# Local components
from project_caesar.code.genesis import get_genesis_block
from project_caesar.code.node import Node


block_0 = get_genesis_block()
print(block_0.text)
print(block_0.hex_values)
print(block_0.hex)
print(block_0.hash)


#node = Node()




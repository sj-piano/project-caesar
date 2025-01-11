# Local imports
from ..utils import hash, misc
from . import transaction


# Local components
from .block import Block
from .genesis import get_genesis_block
from .transaction import Transaction




class Node:


    def __init__(self):
        self.chain = []
        self.process_genesis_block()


    def process_genesis_block(self):
        block_0 = get_genesis_block()
        # Future: Store block in db.
        self.chain.append(block_0)
        # Future: Add coinbase tx to db.


    def process_block(self):
        pass




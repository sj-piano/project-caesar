# Components
from typing import Any, Dict, List, Optional
from pydantic import Field


# Local imports
from ..utils import hash, misc


# Local components
from .models.hex_string import HexString
from .models.json_serializable import JsonSerializable
from .transaction import Transaction
from ..utils.misc import iso_timestamp_to_int
from ..utils.hex_utils import compact_size, int_to_hex




class Block(JsonSerializable):
    """
    Represents a block in a blockchain, containing transactions and a header.

    Attributes:
        version (Optional[int]): The version of the block.
        previous_block (dict): The previous block in the blockchain.
            Contains 'block_height' and 'block_hash'.
        timestamp (Optional[str]): The timestamp of the block.
        mining_difficulty_threshold (Optional[int]): The mining difficulty threshold.
        nonce (Optional[int]): The nonce value for the block.
        transaction_count (Optional[int]): The total number of transactions in the block.
        transactions (Optional[List[Transaction]]): The transactions in the block.
    """

    version: Optional[int] = Field(default=None, description="The version of the block.")
    previous_block: dict = Field(
        default_factory=lambda: {
            'block_height': None,
            'block_hash': None,
        },
        description="The previous block in the blockchain.",
    )
    timestamp: Optional[str] = Field(default=None, description="The timestamp of the block.")
    mining_difficulty_threshold: Optional[int] = Field(default=None, description="The mining difficulty threshold.")
    nonce: Optional[int] = Field(default=None, description="The nonce value for the block.")
    transaction_count: Optional[int] = Field(default=None, description="The total number of transactions in the block.")
    transactions: Optional[List[Transaction]] = Field(default=None, description="The transactions in the block.")

    class Config:
        json_encoders = {
            # Future custom serialization logic if required.
        }


    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Block":
        instance = super().from_json(json_data)
        return instance


    @property
    def merkle_root(self) -> HexString:
        """
        Computes the Merkle root of the block's transactions.

        Returns:
            str: The Merkle root of the block's transactions.
        """
        merkle_root = None
        n = len(self.transactions)
        if n == 0:
            raise ValueError('No transactions to compute the Merkle root.')
        if n == 1:
            tx = self.transactions[0]
            merkle_root = tx.hash
            return merkle_root
        else:
            raise NotImplementedError('Merkle root computation for more than one transaction is not implemented.')
        return merkle_root


    @property
    def hex_values(self) -> Dict[str, HexString]:
        version_hex = int_to_hex(self.version)
        previous_block = self.previous_block
        block_height_hex = int_to_hex(previous_block['block_height'])
        block_hash = previous_block['block_hash']
        timestamp_int = iso_timestamp_to_int(self.timestamp)
        timestamp_hex = int_to_hex(timestamp_int)
        mining_difficulty_threshold_hex = int_to_hex(self.mining_difficulty_threshold)
        nonce_hex = int_to_hex(self.nonce)
        merkle_root_hex = self.merkle_root
        transaction_count_hex = int_to_hex(self.transaction_count)
        transactions_hex_values = [t.hex_values for t in self.transactions]
        return {
            'version_length': compact_size(version_hex),
            'version': version_hex,
            'previous_block': {
                'block_height_length': compact_size(block_height_hex),
                'block_height': block_height_hex,
                'block_hash': block_hash,
            },
            'merkle_root': merkle_root_hex,
            'timestamp_length': compact_size(timestamp_hex),
            'timestamp': timestamp_hex,
            'mining_difficulty_threshold_length': compact_size(mining_difficulty_threshold_hex),
            'mining_difficulty_threshold': mining_difficulty_threshold_hex,
            'nonce_length': compact_size(nonce_hex),
            'nonce': nonce_hex,
            'transaction_count_length': compact_size(transaction_count_hex),
            'transaction_count': transaction_count_hex,
            'transactions': transactions_hex_values,
        }


    @property
    def hex(self) -> HexString:
        v = self.hex_values
        s = ''
        s += v['version_length']
        s += v['version']
        pb = v['previous_block']
        s += pb['block_height_length']
        s += pb['block_height']
        s += pb['block_hash']
        s += v['merkle_root']
        for key in 'timestamp mining_difficulty_threshold nonce transaction_count'.split():
            s += v[key + '_length']
            s += v[key]
        s += ''.join([t.hex for t in self.transactions])
        return s


    @property
    def hash(self) -> HexString:
        return hash.get_sha256(self.hex)


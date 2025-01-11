# Local components
from .block import Block


def get_genesis_block():
    block_0_json = get_genesis_block_json()
    block_0 = Block.from_json(block_0_json)
    return block_0


def get_genesis_block_json():
    return {
        'version': 1,
        'previous_block': {
            'block_height': None,
            'block_hash': '00000000',
        },
        'timestamp': '2024-11-18T08:09:09Z',
        'mining_difficulty_threshold': 0,
        'nonce': 0,
        'merkle_root': None,
        'transaction_count': 1,
        'transactions': [
            {
                'input_count': 1,
                'output_count': 1,
                'fee': 0,
                'inputs': [
                    {
                        'previous_output': {
                            'block_height': None,
                            'transaction_hash': '00000000',
                            'output_index': None,
                        },
                        'unlock_script': 'Wisdom comes from the desert.'.encode().hex(),
                    }
                ],
                'outputs': [
                    {
                        'value': 5000000000,
                        'lock_script': 'OP_DUPLICATE OP_HASH_160 {pkh} OP_EQUAL_VERIFY OP_CHECK_SIGNATURE'.format(pkh='f575f780'),
                    }
                ],
            }
        ]
    }


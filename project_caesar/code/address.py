# Local imports
from .public_key import get_public_key_hash
from ..utils import hash


def public_key_to_address(public_key):
    pk_hash = get_public_key_hash(public_key)
    # Add network version byte: '00' for mainnet.
    x = '00' + pk_hash
    a = hash.toy_hash(x)
    b = 'csr_' + a
    return b


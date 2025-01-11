# Local imports
from ..utils import hash


def secret_key_to_public_key(secret_key):
    # Toy public key derivation function: Add a constant to the secret key.
    # Take modulo 2^32 to keep the result in the 4-byte range.
    n_bytes = 4
    n_bits = 8 * n_bytes
    secret_key_int = int(secret_key, 16)
    constant = 0xdeadbeef
    constant_int = int(constant)
    public_key_int = (secret_key_int + constant_int) % (2 ** n_bits)
    public_key = hex(public_key_int)[2:]
    return public_key


def get_public_key_hash(public_key):
    return hash.toy_hash(public_key)


# Imports
import os
import random


# Local imports
from .models.hex_string import HexString
from ..submodules import ecdsa_python3 as ecdsa
from ..utils import module_logger


# Logger
logger, log, deb = module_logger.create_logger(__file__)


def create_secret_key_toy():
    # Toy secret key generation function: Generate a random 4-byte hex string.
    n_bytes = 4
    return ''.join(random.choice('0123456789abcdef') for _ in range(n_bytes * 2))


def generate_secret_key() -> HexString:
    n = 32
    value = os.urandom(n).hex()
    secret_key = HexString(value=value, length=n)
    return secret_key

# Imports
import random


def create_secret_key():
    # Toy secret key generation function: Generate a random 4-byte hex string.
    n_bytes = 4
    return ''.join(random.choice('0123456789abcdef') for _ in range(n_bytes * 2))


# Local components
from ..code.models.hex_string import HexString
from ..submodules import sha256_python3 as sha256




def toy_hash(data_hex):
    # A toy hash function that shifts each byte by 3 bits.
    # Take modulo 2^32 to keep the result in the 4-byte range.
    data_int = int(data_hex, 16)
    shifted = (data_int << 3)
    result_int = shifted & 0xFFFFFFFF
    result = hex(result_int)[2:]
    # Pad the result to ensure it is 8 characters long
    padded_result = result.zfill(8)
    return padded_result



def get_sha256(x: HexString) -> HexString:
  if not HexString.is_valid_hex(x):
        raise ValueError(f"Invalid hex string: {x}")
  x_bytes = bytes.fromhex(x)
  return sha256.hexdigest(x_bytes)


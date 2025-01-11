

def compact_size(hex_value):
    """
    Calculates the Compact Size encoding for the length of a hex value.

    Args:
        hex_value (str): The hex string (without '0x' prefix).

    Returns:
        bytes: The variadic byte value encoding the length.
    """

    if hex_value is None:
        return ''

    length = len(hex_value) // 2  # Number of bytes in the hex value

    endianness = 'little'

    if length < 0xFD:
        x = length.to_bytes(1, endianness)  # 1 byte for lengths < 253
    elif length <= 0xFFFF:
        x = b'\xFD' + length.to_bytes(2, endianness)  # 0xFD + 2 bytes for lengths <= 65,535
    elif length <= 0xFFFFFFFF:
        x = b'\xFE' + length.to_bytes(4, endianness)  # 0xFE + 4 bytes for lengths <= 4,294,967,295
    else:
        x = b'\xFF' + length.to_bytes(8, endianness)  # 0xFF + 8 bytes for larger lengths

    # Convert to hex
    y = x.hex()
    y = ensure_even_hex_length(y)
    return y


def int_to_hex(n):
    if n is None:
        return ''
    x = hex(n)[2:]
    return ensure_even_hex_length(x)


def ensure_even_hex_length(value):
    if len(value) % 2 != 0:
        value = '0' + value
    return value


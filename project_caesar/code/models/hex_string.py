# Imports
import re




class HexString(str):
    """
    A custom class for a hex string that validates its content.
    Inherits from `str` so it behaves like a string with additional validation.
    """

    @classmethod
    def __new__(cls, value: str):
        # Create an instance of the hex string class
        instance = super().__new__(cls, value)

        # Perform validation on initialization
        if not cls.is_valid_hex(value):
            raise ValueError(f"Invalid hex string: {value}")

        return instance


    @staticmethod
    def is_valid_hex(value: str) -> bool:
        """
        Check if the string is a valid hex string.
        Optionally supports strings with a 0x prefix.
        """
        if value.startswith('0x') or value.startswith('0X'):
            value = value[2:]  # Remove the 0x prefix if it exists

        # Check if the string consists only of valid hexadecimal characters
        return bool(re.match(r'^[0-9a-fA-F]+$', value))


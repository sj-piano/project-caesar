# Imports
from pydantic import BaseModel, Field, field_validator
import re


class HexString(BaseModel):
    """
    A custom class for a hex string with validation for content and length, using Pydantic v2.
    """
    value: str
    length: int | None = None

    @field_validator('value', mode='before')
    def strip_prefix(cls, value: str) -> str:
        """
        Strips the 0x prefix from the hex string.
        """
        if value.startswith('0x') or value.startswith('0X'):
            value = value[2:]
        return value

    @field_validator('value', mode='after')
    def validate_hex_characters(cls, value: str) -> str:
        """
        Validates that the value is a valid hex string.
        """
        if not all(c in "0123456789abcdefABCDEF" for c in value):
            raise ValueError(f"Invalid hex string: {value}")
        return value

    @field_validator('value', mode='after')
    def validate_length(cls, value: str, info) -> str:
        """
        Validates the length of the hex string after all previous validators have run.
        """
        length = info.data.get('length')
        if length is not None and len(value) != length * 2:
            raise ValueError(
                f"Invalid length for hex string. Expected {length * 2} hex characters "
                f"(or {length} bytes), but got {len(value)} characters."
            )
        return value




class HexString2(str):
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


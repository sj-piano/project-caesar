# Components
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


# Local components
from .gaius import script_to_hex
from .models.hex_string import HexString
from .models.json_serializable import JsonSerializable
from ..utils.hex_utils import compact_size, int_to_hex




# Todo: A from_json method that returns an Output
class Output(JsonSerializable):
    """
    Represents an output in a blockchain transaction, containing a value and a lock script.

    Attributes:
        value (Optional[int]): The value of the output, typically in satoshis or the smallest unit of the currency.
        lock_script (Optional[str]): The lock script of the output, usually representing the conditions under which the output can be spent.
    """

    value: Optional[int] = Field(default=None, description="The value of the output.")
    lock_script: Optional[str] = Field(default=None, description="The lock script of the output.")

    class Config:
        json_encoders = {
            # Future custom serialization logic if required.
        }

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Output":
        instance = super().from_json(json_data)
        return instance


    @property
    def hex_values(self) -> Dict[str, HexString]:
        """
        Returns the hex-encoded values of the output's attributes, along with their lengths.

        Returns:
            Dict[str, str]: A dictionary containing 'value_length', 'value', 'lock_script_length', and 'lock_script' as hex-encoded strings.
        """
        if self.value is None or self.lock_script is None:
            raise ValueError("Both 'value' and 'lock_script' must be set before accessing hex_values.")

        value_hex = int_to_hex(self.value)
        lock_script_hex = script_to_hex(self.lock_script)

        return {
            'value_length': compact_size(value_hex),
            'value': value_hex,
            'lock_script_length': compact_size(lock_script_hex),
            'lock_script': lock_script_hex,
        }

    @property
    def hex(self) -> HexString:
        """
        Returns the full hex-encoded string of the output.

        This combines the length and value of both the value and lock script.

        Returns:
            str: The full hex string representation of the output.
        """
        v = self.hex_values
        hex_string = ''
        hex_string += v['value_length']
        hex_string += v['value']
        hex_string += v['lock_script_length']
        hex_string += v['lock_script']
        return hex_string


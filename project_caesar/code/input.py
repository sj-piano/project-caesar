# Components
from typing import Any, Dict, Optional
from pydantic import Field


# Local components
from .gaius import script_to_hex
from .models.hex_string import HexString
from .models.json_serializable import JsonSerializable
from ..utils.hex_utils import compact_size, int_to_hex




class Input(JsonSerializable):
    """
    Represents an input in a blockchain transaction, which typically includes a previous output
    and an unlock script.

    Attributes:
        previous_output (dict): The previous output being referenced by this input.
            Contains 'block_height', 'transaction_hash', and 'output_index'.
        unlock_script (Optional[str]): The unlock script for this input, usually used to validate
            the conditions for spending the input.
    """


    previous_output: dict = Field(
        default_factory=lambda: {
            'block_height': None,
            'transaction_hash': None,
            'output_index': None,
        },
        description="Details of the previous output referenced by this input.",
    )
    unlock_script: Optional[str] = Field(default=None, description="The unlock script for this input.")

    class Config:
        json_encoders = {
            # Future custom serialization logic if required.
        }


    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Input":
        instance = super().from_json(json_data)
        return instance


    @property
    def hex_values(self) -> Dict[str, HexString]:
        """
        Returns the hex-encoded values of the input's attributes, along with their lengths.

        Returns:
            Dict[str, Any]: A dictionary with hex-encoded values for previous_output and unlock_script.
        """
        previous_output = self.previous_output
        block_height_hex = int_to_hex(previous_output['block_height'])
        transaction_hash = previous_output['transaction_hash']
        output_index_hex = int_to_hex(previous_output['output_index'])
        unlock_script_hex = script_to_hex(self.unlock_script)

        return {
            'previous_output': {
                'block_height_length': compact_size(block_height_hex),
                'block_height': block_height_hex,
                'transaction_hash': transaction_hash,
                'output_index_length': compact_size(output_index_hex),
                'output_index': output_index_hex,
            },
            'unlock_script_length': compact_size(unlock_script_hex),
            'unlock_script': unlock_script_hex,
        }


    @property
    def hex(self) -> HexString:
        """
        Returns the full hex-encoded string of the input, combining all the hex-encoded components.

        Returns:
            str: The full hex string representation of the input.
        """
        v = self.hex_values
        hex_string = ''
        hex_string += v['previous_output']['block_height_length']
        hex_string += v['previous_output']['block_height']
        hex_string += v['previous_output']['transaction_hash']
        hex_string += v['previous_output']['output_index_length']
        hex_string += v['previous_output']['output_index']
        hex_string += v['unlock_script_length']
        hex_string += v['unlock_script']
        return hex_string


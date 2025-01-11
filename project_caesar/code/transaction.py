# Components
from typing import Any, Dict, List, Optional
from pydantic import Field


# Local imports
from ..utils import hash, misc


# Local components
from .input import Input
from .models.hex_string import HexString
from .models.json_serializable import JsonSerializable
from .output import Output
from ..utils.hex_utils import compact_size, int_to_hex
from ..utils.misc import stop




class Transaction(JsonSerializable):
    """
    Represents a transaction in a blockchain, containing inputs and outputs.
    """


    input_count: Optional[int] = Field(default=None, description="The total number of inputs in the transaction.")
    output_count: Optional[int] = Field(default=None, description="The total number of outputs in the transaction.")
    fee: Optional[int] = Field(default=None, description="The fee value in the transaction.")
    inputs: Optional[List[Input]] = Field(default=None, description="The inputs in the transaction.")
    outputs: Optional[List[Output]] = Field(default=None, description="The outputs in the transaction.")

    class Config:
        json_encoders = {
            # Future custom serialization logic if required.
        }


    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "Transaction":
        instance = super().from_json(json_data)
        return instance


    @property
    def hex_values(self) -> Dict[str, HexString]:
        input_count_hex = int_to_hex(self.input_count)
        output_count_hex = int_to_hex(self.output_count)
        fee_hex = int_to_hex(self.fee)
        inputs_hex_values = [i.hex_values for i in self.inputs]
        outputs_hex_values = [o.hex_values for o in self.outputs]
        return {
            'input_count_length': compact_size(input_count_hex),
            'input_count': input_count_hex,
            'output_count_length': compact_size(output_count_hex),
            'output_count': output_count_hex,
            'fee_length': compact_size(fee_hex),
            'fee': fee_hex,
            'inputs': inputs_hex_values,
            'outputs': outputs_hex_values,
        }


    @property
    def hex(self) -> HexString:
        v = self.hex_values
        s = ''
        for key in 'input_count output_count fee'.split():
            s += v[key + '_length']
            s += v[key]
        s += ''.join([i.hex for i in self.inputs])
        s += ''.join([o.hex for o in self.outputs])
        return s


    @property
    def hash(self) -> HexString:
        return hash.get_sha256(self.hex)


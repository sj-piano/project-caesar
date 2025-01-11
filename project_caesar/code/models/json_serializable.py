# Imports
import json


# Components
from typing import Any, Dict, Optional
from pydantic import BaseModel, ValidationError




class JsonSerializable(BaseModel):
    """
    A base class for providing JSON serialization and deserialization functionality to Pydantic models.
    """


    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "JsonSerializable":
        """
        Creates an instance of the class from a JSON dictionary.

        Args:
            json_data (Dict[str, Any]): The JSON data to create the instance from.

        Returns:
            JsonSerializable: An instance of the class populated with the provided data.

        Raises:
            ValueError: If any invalid property is found in the provided JSON data.
        """
        try:
            # Attempt to parse the JSON data into a Pydantic model instance
            return cls.model_validate(json_data)
        except ValidationError as e:
            # Handle the case where the input data is invalid
            raise ValueError(f"Invalid data for class {cls.__name__}: {e}")


    def to_json(self) -> Dict[str, Optional[str]]:
        return self.model_dump(exclude_none=True)


    @property
    def json(self) -> Dict[str, Any]:
        return self.to_json()


    @property
    def text(self):
        return json.dumps(self.json, indent=4)


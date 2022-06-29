from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.traits.variables import Variables


class Effect(BaseModel):
    maxUnits: int = 0
    minUnits: int = 0
    style: int = 0
    variables: Variables = Field(default_factory=Variables)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Effect":
        data['variables'] = Variables.from_dict(data['variables']).to_dict()
        return Effect(**data)

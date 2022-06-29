from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.traits.trait import Trait


class Traits(BaseModel):
    traits: List[Trait] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Traits":
        data = {'traits': [Trait.from_dict(v).to_dict() for v in data]}
        return Traits(**data)

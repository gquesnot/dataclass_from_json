from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.comps.comp import Comp


class Comps(BaseModel):
    comps: List[Comp] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Comps":
        data = {'comps': [Comp.from_dict(v).to_dict() for v in data]}
        return Comps(**data)

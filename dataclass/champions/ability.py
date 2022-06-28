from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.champions.variable import Variable


class Ability(BaseModel):
    desc: Optional[str] = None
    icon: str = ''
    name: Optional[str] = None
    variables: List[Variable] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Ability":
        data['variables'] = [Variable.from_dict(v).to_dict() for v in data['variables']]
        return Ability(**data)

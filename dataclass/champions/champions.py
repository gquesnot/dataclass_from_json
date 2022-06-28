from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.champions.champion import Champion


class Champions(BaseModel):
    champions: List[Champion] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Champions":
        data = {'champions': [Champion.from_dict(v).to_dict() for v in data]}
        return Champions(**data)

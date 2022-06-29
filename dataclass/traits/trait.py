from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.traits.effect import Effect


class Trait(BaseModel):
    apiName: str = ''
    desc: str = ''
    effects: List[Effect] = Field(default_factory=list)
    icon: str = ''
    name: str = ''

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Trait":
        data['effects'] = [Effect.from_dict(v).to_dict() for v in data['effects']]
        return Trait(**data)

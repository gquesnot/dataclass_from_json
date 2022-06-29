from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.champions.ability import Ability
from dataclass.champions.stats import Stats


class Champion(BaseModel):
    ability: Ability = Field(default_factory=Ability)
    apiName: str = ''
    cost: int = 0
    icon: Optional[str] = None
    name: str = ''
    stats: Stats = Field(default_factory=Stats)
    traits: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Champion":
        data['ability'] = Ability.from_dict(data['ability']).to_dict()
        data['stats'] = Stats.from_dict(data['stats']).to_dict()
        return Champion(**data)

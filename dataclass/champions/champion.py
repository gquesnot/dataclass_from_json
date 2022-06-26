from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.champions.ability import Ability
from dataclass.champions.stats import Stats


@dataclass
class Champion(BaseDataclass):
    ability: Ability = field(default_factory=Ability)
    apiName: str = field(default="")
    cost: int = field(default=0)
    icon: Optional[str] = field(default=None)
    name: str = field(default="")
    stats: Stats = field(default_factory=Stats)
    traits: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Champion":
        data['ability'] = Ability.from_dict(data['ability']).to_dict()
        data['stats'] = Stats.from_dict(data['stats']).to_dict()
        return from_dict(cls, data=data)

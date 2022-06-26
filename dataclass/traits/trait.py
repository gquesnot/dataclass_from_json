from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.traits.effect import Effect


@dataclass
class Trait(BaseDataclass):
    apiName: str = field(default="")
    desc: str = field(default="")
    effects: List[Effect] = field(default_factory=list)
    icon: str = field(default="")
    name: str = field(default="")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Trait":
        data['effects'] = [Effect.from_dict(v).to_dict() for v in data['effects']]
        return from_dict(cls, data=data)

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.traits.trait import Trait


@dataclass
class Traits(BaseDataclass):
    traits: List[Trait] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Traits":
        data = {'traits': [Trait.from_dict(v).to_dict() for v in data]}
        return from_dict(cls, data=data)

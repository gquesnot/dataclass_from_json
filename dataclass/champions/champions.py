from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.champions.champion import Champion


@dataclass
class Champions(BaseDataclass):
    champions: List[Champion] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Champions":
        data = {'champions': [Champion.from_dict(v).to_dict() for v in data]}
        return from_dict(cls, data=data)

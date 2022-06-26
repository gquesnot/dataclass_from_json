from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.champions.variable import Variable


@dataclass
class Ability(BaseDataclass):
    desc: Optional[str] = field(default=None)
    icon: str = field(default="")
    name: Optional[str] = field(default=None)
    variables: List[Variable] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Ability":
        data['variables'] = [Variable.from_dict(v).to_dict() for v in data['variables']]
        return from_dict(cls, data=data)

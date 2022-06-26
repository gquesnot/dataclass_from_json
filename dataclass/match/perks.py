from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.statPerks import StatPerks
from dataclass.match.style import Style


@dataclass
class Perks(BaseDataclass):
    statPerks: StatPerks = field(default_factory=StatPerks)
    styles: List[Style] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Perks":
        data['statPerks'] = StatPerks.from_dict(data['statPerks']).to_dict()
        data['styles'] = [Style.from_dict(v).to_dict() for v in data['styles']]
        return from_dict(cls, data=data)

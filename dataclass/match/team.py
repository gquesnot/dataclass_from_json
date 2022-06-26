from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.ban import Ban
from dataclass.match.objectives import Objectives


@dataclass
class Team(BaseDataclass):
    bans: List[Ban] = field(default_factory=list)
    objectives: Objectives = field(default_factory=Objectives)
    teamId: int = field(default=0)
    win: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Team":
        data['bans'] = [Ban.from_dict(v).to_dict() for v in data['bans']]
        data['objectives'] = Objectives.from_dict(data['objectives']).to_dict()
        return from_dict(cls, data=data)

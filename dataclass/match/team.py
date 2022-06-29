from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.ban import Ban
from dataclass.match.objectives import Objectives


class Team(BaseModel):
    bans: List[Ban] = Field(default_factory=list)
    objectives: Objectives = Field(default_factory=Objectives)
    teamId: int = 0
    win: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Team":
        data['bans'] = [Ban.from_dict(v).to_dict() for v in data['bans']]
        data['objectives'] = Objectives.from_dict(data['objectives']).to_dict()
        return Team(**data)

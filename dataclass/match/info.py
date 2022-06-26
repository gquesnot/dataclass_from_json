from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.participant import Participant
from dataclass.match.team import Team


@dataclass
class Info(BaseDataclass):
    gameCreation: int = field(default=0)
    gameDuration: int = field(default=0)
    gameEndTimestamp: int = field(default=0)
    gameId: int = field(default=0)
    gameMode: str = field(default="")
    gameName: str = field(default="")
    gameStartTimestamp: int = field(default=0)
    gameType: str = field(default="")
    gameVersion: str = field(default="")
    mapId: int = field(default=0)
    participants: List[Participant] = field(default_factory=list)
    platformId: str = field(default="")
    queueId: int = field(default=0)
    teams: List[Team] = field(default_factory=list)
    tournamentCode: str = field(default="")

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Info":
        data['participants'] = [Participant.from_dict(v).to_dict() for v in data['participants']]
        data['teams'] = [Team.from_dict(v).to_dict() for v in data['teams']]
        return from_dict(cls, data=data)

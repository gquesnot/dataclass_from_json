from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.participant import Participant
from dataclass.match.team import Team


class Info(BaseModel):
    gameCreation: int = 0
    gameDuration: int = 0
    gameEndTimestamp: int = 0
    gameId: int = 0
    gameMode: str = ''
    gameName: str = ''
    gameStartTimestamp: int = 0
    gameType: str = ''
    gameVersion: str = ''
    mapId: int = 0
    participants: List[Participant] = Field(default_factory=list)
    platformId: str = ''
    queueId: int = 0
    teams: List[Team] = Field(default_factory=list)
    tournamentCode: str = ''

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Info":
        data['participants'] = [Participant.from_dict(v).to_dict() for v in data['participants']]
        data['teams'] = [Team.from_dict(v).to_dict() for v in data['teams']]
        return Info(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.participant import Participant, Participant, Participant
from dataclass.match.team import Team, Team, Team
from dataclass.match.frame import Frame, Frame


class Info(BaseModel):
    gameCreation: Optional[int] = None
    gameDuration: Optional[int] = None
    gameEndTimestamp: Optional[int] = None
    gameId: int = 0
    gameMode: Optional[str] = None
    gameName: Optional[str] = None
    gameStartTimestamp: Optional[int] = None
    gameType: Optional[str] = None
    gameVersion: Optional[str] = None
    mapId: Optional[int] = None
    participants: List[Participant] = Field(default_factory=list)
    platformId: Optional[str] = None
    queueId: Optional[int] = None
    teams: Optional[List[Team]] = Field(default_factory=list)
    tournamentCode: Optional[str] = None
    frameInterval: Optional[int] = None
    frames: Optional[List[Frame]] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Info":
        data['participants'] = [Participant.from_dict(v).to_dict() for v in data['participants']]
        if 'teams' in data:
            data['teams'] = [Team.from_dict(v).to_dict() for v in data['teams']]
        if 'frames' in data:
            data['frames'] = [Frame.from_dict(v).to_dict() for v in data['frames']]
        return Info(**data)

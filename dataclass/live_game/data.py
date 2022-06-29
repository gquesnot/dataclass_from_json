from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.live_game.participant import Participant
from dataclass.live_game.observers import Observers
from dataclass.live_game.banned_champion import BannedChampion


class Data(BaseModel):
    gameId: int = 0
    mapId: int = 0
    gameMode: str = ''
    gameType: str = ''
    gameQueueConfigId: int = 0
    participants: List[Participant] = Field(default_factory=list)
    observers: Observers = Field(default_factory=Observers)
    platformId: str = ''
    bannedChampions: List[BannedChampion] = Field(default_factory=list)
    gameStartTime: int = 0
    gameLength: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Data":
        data['participants'] = [Participant.from_dict(v).to_dict() for v in data['participants']]
        data['observers'] = Observers.from_dict(data['observers']).to_dict()
        data['bannedChampions'] = [BannedChampion.from_dict(v).to_dict() for v in data['bannedChampions']]
        return Data(**data)

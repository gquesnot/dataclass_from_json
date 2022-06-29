from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.metadata import Metadata, Metadata, Metadata
from dataclass.match.info import Info, Info, Info
from dataclass.match.participant import Participant
from dataclass.match.observers import Observers
from dataclass.match.banned_champion import BannedChampion


class Data(BaseModel):
    metadata: Optional[Metadata] = Field(default_factory=Metadata)
    info: Optional[Info] = Field(default_factory=Info)
    gameId: Optional[int] = None
    mapId: Optional[int] = None
    gameMode: Optional[str] = None
    gameType: Optional[str] = None
    gameQueueConfigId: Optional[int] = None
    participants: Optional[List[Participant]] = Field(default_factory=list)
    observers: Optional[Observers] = Field(default_factory=Observers)
    platformId: Optional[str] = None
    bannedChampions: Optional[List[BannedChampion]] = Field(default_factory=list)
    gameStartTime: Optional[int] = None
    gameLength: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Data":
        if 'metadata' in data:
            data['metadata'] = Metadata.from_dict(data['metadata']).to_dict()
        if 'info' in data:
            data['info'] = Info.from_dict(data['info']).to_dict()
        if 'participants' in data:
            data['participants'] = [Participant.from_dict(v).to_dict() for v in data['participants']]
        if 'observers' in data:
            data['observers'] = Observers.from_dict(data['observers']).to_dict()
        if 'bannedChampions' in data:
            data['bannedChampions'] = [BannedChampion.from_dict(v).to_dict() for v in data['bannedChampions']]
        return Data(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.position import Position, Position
from dataclass.match.victim_damage_dealt_index import VictimDamageDealtIndex, VictimDamageDealtIndex
from dataclass.match.victim_damage_received_index import VictimDamageReceivedIndex, VictimDamageReceivedIndex


class Event(BaseModel):
    realTimestamp: Optional[int] = None
    timestamp: int = 0
    type: str = ''
    itemId: Optional[int] = None
    participantId: Optional[int] = None
    levelUpType: Optional[str] = None
    skillSlot: Optional[int] = None
    afterId: Optional[int] = None
    beforeId: Optional[int] = None
    goldGain: Optional[int] = None
    creatorId: Optional[int] = None
    wardType: Optional[str] = None
    killerId: Optional[int] = None
    level: Optional[int] = None
    assistingParticipantIds: Optional[List[Union[int, int]]] = Field(default_factory=list)
    bounty: Optional[int] = None
    killStreakLength: Optional[int] = None
    position: Optional[Position] = Field(default_factory=Position)
    shutdownBounty: Optional[int] = None
    victimDamageDealt: Optional[List[VictimDamageDealtIndex]] = Field(default_factory=list)
    victimDamageReceived: Optional[List[VictimDamageReceivedIndex]] = Field(default_factory=list)
    victimId: Optional[int] = None
    killType: Optional[str] = None
    multiKillLength: Optional[int] = None
    killerTeamId: Optional[int] = None
    monsterSubType: Optional[str] = None
    monsterType: Optional[str] = None
    laneType: Optional[str] = None
    teamId: Optional[int] = None
    buildingType: Optional[str] = None
    towerType: Optional[str] = None
    gameId: Optional[int] = None
    winningTeam: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Event":
        if 'position' in data:
            data['position'] = Position.from_dict(data['position']).to_dict()
        if 'victimDamageDealt' in data:
            data['victimDamageDealt'] = [VictimDamageDealtIndex.from_dict(v).to_dict() for v in data['victimDamageDealt']]
        if 'victimDamageReceived' in data:
            data['victimDamageReceived'] = [VictimDamageReceivedIndex.from_dict(v).to_dict() for v in data['victimDamageReceived']]
        return Event(**data)

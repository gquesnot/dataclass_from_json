from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.champion_stats import ChampionStats, ChampionStats
from dataclass.match.damage_stats import DamageStats, DamageStats
from dataclass.match.position import Position, Position


class ParticipantFrame(BaseModel):
    championStats: ChampionStats = Field(default_factory=ChampionStats)
    currentGold: int = 0
    damageStats: DamageStats = Field(default_factory=DamageStats)
    goldPerSecond: int = 0
    jungleMinionsKilled: int = 0
    level: int = 0
    minionsKilled: int = 0
    participantId: int = 0
    position: Position = Field(default_factory=Position)
    timeEnemySpentControlled: int = 0
    totalGold: int = 0
    xp: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "ParticipantFrame":
        data['championStats'] = ChampionStats.from_dict(data['championStats']).to_dict()
        data['damageStats'] = DamageStats.from_dict(data['damageStats']).to_dict()
        data['position'] = Position.from_dict(data['position']).to_dict()
        return ParticipantFrame(**data)

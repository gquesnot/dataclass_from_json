from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class DamageStats(BaseModel):
    magicDamageDone: int = 0
    magicDamageDoneToChampions: int = 0
    magicDamageTaken: int = 0
    physicalDamageDone: int = 0
    physicalDamageDoneToChampions: int = 0
    physicalDamageTaken: int = 0
    totalDamageDone: int = 0
    totalDamageDoneToChampions: int = 0
    totalDamageTaken: int = 0
    trueDamageDone: int = 0
    trueDamageDoneToChampions: int = 0
    trueDamageTaken: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "DamageStats":
        return DamageStats(**data)

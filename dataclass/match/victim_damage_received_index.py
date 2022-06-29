from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class VictimDamageReceivedIndex(BaseModel):
    basic: bool = False
    magicDamage: int = 0
    name: str = ''
    participantId: int = 0
    physicalDamage: int = 0
    spellName: str = ''
    spellSlot: int = 0
    trueDamage: int = 0
    type: str = ''

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "VictimDamageReceivedIndex":
        return VictimDamageReceivedIndex(**data)

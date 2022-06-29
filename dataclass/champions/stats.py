from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Stats(BaseModel):
    armor: float = 0.0
    attackSpeed: Optional[float] = None
    critChance: Optional[float] = None
    critMultiplier: float = 0.0
    damage: Optional[float] = None
    hp: float = 0.0
    initialMana: float = 0.0
    magicResist: Optional[float] = None
    mana: float = 0.0
    _range: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Stats":
        data['_range'] = data['range']
        del data['range']

        return Stats(**data)

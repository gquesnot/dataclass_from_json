from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Stats(BaseDataclass):
    armor: float = field(default=.0)
    attackSpeed: Optional[float] = field(default=None)
    critChance: Optional[float] = field(default=None)
    critMultiplier: float = field(default=.0)
    damage: Optional[float] = field(default=None)
    hp: float = field(default=.0)
    initialMana: float = field(default=.0)
    magicResist: Optional[float] = field(default=None)
    mana: float = field(default=.0)
    range: float = field(default=.0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Stats":
        return from_dict(cls, data=data)

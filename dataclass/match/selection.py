from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Selection(BaseDataclass):
    perk: int = field(default=0)
    var1: int = field(default=0)
    var2: int = field(default=0)
    var3: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Selection":
        return from_dict(cls, data=data)

from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Ban(BaseDataclass):
    championId: int = field(default=0)
    pickTurn: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Ban":
        return from_dict(cls, data=data)

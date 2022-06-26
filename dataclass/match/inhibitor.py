from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Inhibitor(BaseDataclass):
    first: int = field(default=0)
    kills: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Inhibitor":
        return from_dict(cls, data=data)

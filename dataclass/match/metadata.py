from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Metadata(BaseDataclass):
    dataVersion: str = field(default="")
    matchId: str = field(default="")
    participants: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Metadata":
        return from_dict(cls, data=data)

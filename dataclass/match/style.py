from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.selection import Selection


@dataclass
class Style(BaseDataclass):
    description: str = field(default="")
    selections: List[Selection] = field(default_factory=list)
    style: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Style":
        data['selections'] = [Selection.from_dict(v).to_dict() for v in data['selections']]
        return from_dict(cls, data=data)

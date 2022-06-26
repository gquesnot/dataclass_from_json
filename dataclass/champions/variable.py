from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Variable(BaseDataclass):
    name: str = field(default="")
    value: Optional[List[float]] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Variable":
        return from_dict(cls, data=data)

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Union

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Effect(BaseDataclass):
    maxUnits: int = field(default=0)
    minUnits: int = field(default=0)
    style: int = field(default=0)
    variables: Dict[str, Union[float, str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Effect":
        return from_dict(cls, data=data)

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Union, Optional
from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass


@dataclass
class Item(BaseDataclass):
    desc: str = field(default="")
    effects: Union[List[Union[str, float]], Dict[str, Any]] = field(default_factory=list)
    _from: List[int] = field(default_factory=list)
    icon: str = field(default="")
    id: int = field(default=0)
    name: str = field(default="")
    unique: int = field(default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['from'] = data['_from']
        del data['_from']
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Item":
        data['_from'] = data['from']
        del data['from']
        return from_dict(cls, data=data)

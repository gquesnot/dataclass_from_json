from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Union, Optional
from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.items.item import Item


@dataclass
class Items(BaseDataclass):
    items: List[Item] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Items":
        data = {'items': [Item.from_dict(v).to_dict() for v in data]}
        return from_dict(cls, data=data)

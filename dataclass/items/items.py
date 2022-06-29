from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.items.item import Item


class Items(BaseModel):
    items: List[Item] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Items":
        data = {'items': [Item.from_dict(v).to_dict() for v in data]}
        return Items(**data)

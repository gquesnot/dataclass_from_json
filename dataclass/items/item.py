from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Item(BaseModel):
    desc: str = ''
    effects: Dict[str, Optional[Union[Optional[float], Optional[str]]]] = Field(default_factory=dict)
    _from: List[int] = Field(default_factory=list)
    icon: str = ''
    id: int = 0
    name: str = ''
    unique: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Item":
        data['_from'] = data['from']
        del data['from']

        return Item(**data)

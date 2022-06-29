from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Selection(BaseModel):
    perk: int = 0
    var1: int = 0
    var2: int = 0
    var3: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Selection":
        return Selection(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class StatPerks(BaseModel):
    defense: int = 0
    flex: int = 0
    offense: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "StatPerks":
        return StatPerks(**data)

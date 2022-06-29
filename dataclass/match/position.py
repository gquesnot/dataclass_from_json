from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Position(BaseModel):
    x: int = 0
    y: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Position":
        return Position(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Ban(BaseModel):
    championId: int = 0
    pickTurn: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Ban":
        return Ban(**data)

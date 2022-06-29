from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Baron(BaseModel):
    first: bool = False
    kills: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Baron":
        return Baron(**data)

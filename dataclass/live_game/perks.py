from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Perks(BaseModel):
    perkIds: List[int] = Field(default_factory=list)
    perkStyle: int = 0
    perkSubStyle: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Perks":
        return Perks(**data)

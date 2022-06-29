from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Metadata(BaseModel):
    dataVersion: str = ''
    matchId: str = ''
    participants: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Metadata":
        return Metadata(**data)

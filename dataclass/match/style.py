from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.selection import Selection, Selection, Selection


class Style(BaseModel):
    description: str = ''
    selections: List[Selection] = Field(default_factory=list)
    style: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Style":
        data['selections'] = [Selection.from_dict(v).to_dict() for v in data['selections']]
        return Style(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Variable(BaseModel):
    name: str = ''
    value: Optional[List[float]] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Variable":
        return Variable(**data)

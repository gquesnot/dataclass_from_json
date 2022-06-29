from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.data import Data


class Match(BaseModel):
    data: Data = Field(default_factory=Data)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Match":
        data['data'] = Data.from_dict(data['data']).to_dict()
        return Match(**data)

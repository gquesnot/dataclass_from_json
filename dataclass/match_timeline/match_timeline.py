from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match_timeline.data import Data


class MatchTimeline(BaseModel):
    data: Optional[Data] = Field(default_factory=Data)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "MatchTimeline":
        if 'data' in data:
            data['data'] = Data.from_dict(data['data']).to_dict()
        return MatchTimeline(**data)

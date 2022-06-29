from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.live_game.data import Data


class Live_game(BaseModel):
    data: Data = Field(default_factory=Data)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Live_game":
        data['data'] = Data.from_dict(data['data']).to_dict()
        return Live_game(**data)

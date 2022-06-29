from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.comps.champions import Champions


class Early(BaseModel):
    description: str = ''
    champions: Champions = Field(default_factory=Champions)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Early":
        data['champions'] = Champions.from_dict(data['champions']).to_dict()
        return Early(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.metadata import Metadata
from dataclass.match.info import Info


class Data(BaseModel):
    metadata: Metadata = Field(default_factory=Metadata)
    info: Info = Field(default_factory=Info)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Data":
        data['metadata'] = Metadata.from_dict(data['metadata']).to_dict()
        data['info'] = Info.from_dict(data['info']).to_dict()
        return Data(**data)

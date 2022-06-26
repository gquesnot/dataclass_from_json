from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.info import Info
from dataclass.match.metadata import Metadata


@dataclass
class Data(BaseDataclass):
    metadata: Metadata = field(default_factory=Metadata)
    info: Info = field(default_factory=Info)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Data":
        data['metadata'] = Metadata.from_dict(data['metadata']).to_dict()
        data['info'] = Info.from_dict(data['info']).to_dict()
        return from_dict(cls, data=data)

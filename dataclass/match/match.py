from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.data import Data


@dataclass
class Match(BaseDataclass):
    data: Data = field(default_factory=Data)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Match":
        data['data'] = Data.from_dict(data['data']).to_dict()
        return from_dict(cls, data=data)

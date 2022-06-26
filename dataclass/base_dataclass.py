from abc import ABC
from dataclasses import dataclass, asdict
from typing import Any, Dict

from dacite import from_dict


@dataclass
class BaseDataclass(ABC):

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseDataClass":
        return from_dict(cls, data=data)

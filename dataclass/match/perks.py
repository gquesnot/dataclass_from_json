from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.stat_perks import StatPerks
from dataclass.match.style import Style


class Perks(BaseModel):
    statPerks: StatPerks = Field(default_factory=StatPerks)
    styles: List[Style] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Perks":
        data['statPerks'] = StatPerks.from_dict(data['statPerks']).to_dict()
        data['styles'] = [Style.from_dict(v).to_dict() for v in data['styles']]
        return Perks(**data)

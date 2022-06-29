from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.comps.positions import Positions
from dataclass.comps.hextech_augment import HextechAugment
from dataclass.comps.early import Early
from dataclass.comps.mid import Mid
from dataclass.comps.late import Late


class Comp(BaseModel):
    name: str = ''
    slug: str = ''
    tier: int = 0
    whenToMake: str = ''
    description: str = ''
    compTips: List[str] = Field(default_factory=list)
    positions: Positions = Field(default_factory=Positions)
    priorityItems: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    formationHash: str = ''
    hextechAugments: List[HextechAugment] = Field(default_factory=list)
    early: Early = Field(default_factory=Early)
    mid: Mid = Field(default_factory=Mid)
    late: Late = Field(default_factory=Late)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Comp":
        data['positions'] = Positions.from_dict(data['positions']).to_dict()
        data['hextechAugments'] = [HextechAugment.from_dict(v).to_dict() for v in data['hextechAugments']]
        data['early'] = Early.from_dict(data['early']).to_dict()
        data['mid'] = Mid.from_dict(data['mid']).to_dict()
        data['late'] = Late.from_dict(data['late']).to_dict()
        return Comp(**data)

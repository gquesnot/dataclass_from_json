from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.baron import Baron
from dataclass.match.champion import Champion
from dataclass.match.dragon import Dragon
from dataclass.match.inhibitor import Inhibitor
from dataclass.match.rift_herald import RiftHerald
from dataclass.match.tower import Tower


class Objectives(BaseModel):
    baron: Baron = Field(default_factory=Baron)
    champion: Champion = Field(default_factory=Champion)
    dragon: Dragon = Field(default_factory=Dragon)
    inhibitor: Inhibitor = Field(default_factory=Inhibitor)
    riftHerald: RiftHerald = Field(default_factory=RiftHerald)
    tower: Tower = Field(default_factory=Tower)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Objectives":
        data['baron'] = Baron.from_dict(data['baron']).to_dict()
        data['champion'] = Champion.from_dict(data['champion']).to_dict()
        data['dragon'] = Dragon.from_dict(data['dragon']).to_dict()
        data['inhibitor'] = Inhibitor.from_dict(data['inhibitor']).to_dict()
        data['riftHerald'] = RiftHerald.from_dict(data['riftHerald']).to_dict()
        data['tower'] = Tower.from_dict(data['tower']).to_dict()
        return Objectives(**data)

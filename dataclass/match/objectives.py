from dataclasses import dataclass, asdict, field
from typing import Dict, Any

from dacite import from_dict

from dataclass.base_dataclass import BaseDataclass
from dataclass.match.baron import Baron
from dataclass.match.champion import Champion
from dataclass.match.dragon import Dragon
from dataclass.match.inhibitor import Inhibitor
from dataclass.match.riftHerald import RiftHerald
from dataclass.match.tower import Tower


@dataclass
class Objectives(BaseDataclass):
    baron: Baron = field(default_factory=Baron)
    champion: Champion = field(default_factory=Champion)
    dragon: Dragon = field(default_factory=Dragon)
    inhibitor: Inhibitor = field(default_factory=Inhibitor)
    riftHerald: RiftHerald = field(default_factory=RiftHerald)
    tower: Tower = field(default_factory=Tower)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Objectives":
        data['baron'] = Baron.from_dict(data['baron']).to_dict()
        data['champion'] = Champion.from_dict(data['champion']).to_dict()
        data['dragon'] = Dragon.from_dict(data['dragon']).to_dict()
        data['inhibitor'] = Inhibitor.from_dict(data['inhibitor']).to_dict()
        data['riftHerald'] = RiftHerald.from_dict(data['riftHerald']).to_dict()
        data['tower'] = Tower.from_dict(data['tower']).to_dict()
        return from_dict(cls, data=data)

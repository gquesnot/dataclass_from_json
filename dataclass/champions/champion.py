from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.champions.ability import Ability
from dataclass.champions.stats import Stats


class Champion(BaseModel):
    """blabla.
       Attributes:
           attr1 (str): Description of `attr1`.
           attr2 (:obj:`int`, optional): Description of `attr2`.

       """
    ability: Ability = Field(default_factory=Ability)
    apiName: str = ''
    cost: int = 0
    icon: Optional[str] = None
    name: str = ''
    stats: Stats = Field(default_factory=Stats)
    traits: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Champion":
        """
        Args:
            data:   Dict[str, Any]

        Returns:    Champion

        """
        data['ability'] = Ability.from_dict(data['ability']).to_dict()
        data['stats'] = Stats.from_dict(data['stats']).to_dict()
        return Champion(**data)

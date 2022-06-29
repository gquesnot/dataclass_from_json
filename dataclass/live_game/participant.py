from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.live_game.perks import Perks


class Participant(BaseModel):
    teamId: int = 0
    spell1Id: int = 0
    spell2Id: int = 0
    championId: int = 0
    profileIconId: int = 0
    summonerName: str = ''
    bot: bool = False
    summonerId: str = ''
    gameCustomizationObjects: List[Union[]] = Field(default_factory=list)
    perks: Perks = Field(default_factory=Perks)

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Participant":
        data['perks'] = Perks.from_dict(data['perks']).to_dict()
        return Participant(**data)

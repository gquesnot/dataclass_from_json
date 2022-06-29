from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Positions(BaseModel):
    leona: Optional[int] = None
    morgana: Optional[int] = None
    braum: Optional[int] = None
    camille: Optional[int] = None
    zyra: Optional[int] = None
    syndra: Optional[int] = None
    draven: Optional[int] = None
    orianna: Optional[int] = None
    gnar: Optional[int] = None
    irelia: Optional[int] = None
    blitzcrank: Optional[int] = None
    senna: Optional[int] = None
    ekko: Optional[int] = None
    ezreal: Optional[int] = None
    seraphine: Optional[int] = None
    reksai: Optional[int] = None
    sivir: Optional[int] = None
    poppy: Optional[int] = None
    lulu: Optional[int] = None
    corki: Optional[int] = None
    ziggs: Optional[int] = None
    vex: Optional[int] = None
    jaycearcane: Optional[int] = None
    vi: Optional[int] = None
    _tahm-kench: Optional[int] = None
    silco: Optional[int] = None
    zeri: Optional[int] = None
    jhin: Optional[int] = None
    ahri: Optional[int] = None
    brand: Optional[int] = None
    zac: Optional[int] = None
    renata: Optional[int] = None
    viktor: Optional[int] = None
    chogath: Optional[int] = None
    alistar: Optional[int] = None
    khazix: Optional[int] = None
    kassadin: Optional[int] = None
    malzahar: Optional[int] = None
    talon: Optional[int] = None
    nocturne: Optional[int] = None
    singed: Optional[int] = None
    warwick: Optional[int] = None
    twitch: Optional[int] = None
    zilean: Optional[int] = None
    jinx: Optional[int] = None
    tryndamere: Optional[int] = None
    quinn: Optional[int] = None
    _jarvan-iv: Optional[int] = None
    swain: Optional[int] = None
    sejuani: Optional[int] = None
    lucian: Optional[int] = None
    _miss-fortune: Optional[int] = None
    darius: Optional[int] = None
    ashe: Optional[int] = None
    kaisa: Optional[int] = None
    caitlyn: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Positions":
        data['_tahm-kench'] = data['tahm-kench']
        del data['tahm-kench']

        data['_jarvan-iv'] = data['jarvan-iv']
        del data['jarvan-iv']

        data['_miss-fortune'] = data['miss-fortune']
        del data['miss-fortune']

        return Positions(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class ChampionStats(BaseModel):
    abilityHaste: int = 0
    abilityPower: int = 0
    armor: int = 0
    armorPen: int = 0
    armorPenPercent: int = 0
    attackDamage: int = 0
    attackSpeed: int = 0
    bonusArmorPenPercent: int = 0
    bonusMagicPenPercent: int = 0
    ccReduction: int = 0
    cooldownReduction: int = 0
    health: int = 0
    healthMax: int = 0
    healthRegen: int = 0
    lifesteal: int = 0
    magicPen: int = 0
    magicPenPercent: int = 0
    magicResist: int = 0
    movementSpeed: int = 0
    omnivamp: int = 0
    physicalVamp: int = 0
    power: int = 0
    powerMax: int = 0
    powerRegen: int = 0
    spellVamp: int = 0

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "ChampionStats":
        return ChampionStats(**data)

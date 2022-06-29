from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Variables(BaseModel):
    _{2a50526a}: Optional[float] = None
    _{3b173c39}: Optional[float] = None
    _{5263ba40}: Optional[float] = None
    _{a859d7b0}: Optional[float] = None
    Armor: Optional[float] = None
    MagicResist: Optional[float] = None
    _{5c51b509}: Optional[float] = None
    _{c9b0e3af}: Optional[float] = None
    _{867bc055}: Optional[float] = None
    _{ed1f9fc2}: Optional[str] = None
    _{5cc08b27}: Optional[float] = None
    _{94c6a08c}: Optional[float] = None
    BonusAS: Optional[float] = None
    _{17cfa971}: Optional[float] = None
    _{47343861}: Optional[float] = None
    _{98396b21}: Optional[float] = None
    BonusArmor: Optional[float] = None
    ShieldAmount: Optional[float] = None
    DamagePercent: Optional[float] = None
    _{5064373e}: Optional[str] = None
    _{6c155e99}: Optional[str] = None
    _{f9f3a081}: Optional[str] = None
    _{02ce80f2}: Optional[float] = None
    _{190fb0a2}: Optional[float] = None
    _{2f805979}: Optional[float] = None
    _{2fb1d11d}: Optional[float] = None
    _{3f1cec4d}: Optional[float] = None
    _{66d8ecb1}: Optional[float] = None
    _{6b5aee70}: Optional[float] = None
    _{76882e8f}: Optional[float] = None
    _{7c799240}: Optional[float] = None
    _{7f322ebf}: Optional[str] = None
    _{82e43c84}: Optional[float] = None
    _{994006f0}: Optional[float] = None
    _{9cc303b4}: Optional[str] = None
    _{b6322d58}: Optional[float] = None
    _{c26236e7}: Optional[float] = None
    _{f3cab19f}: Optional[float] = None
    _{f90dd382}: Optional[str] = None
    _{ce492058}: Optional[float] = None
    _{471b1a16}: Optional[float] = None
    _{d0539890}: Optional[float] = None
    _{45564848}: Optional[float] = None
    _{97ea7bfc}: Optional[float] = None
    MagicDamage: Optional[float] = None
    ShieldDuration: Optional[float] = None
    _{2fb31c01}: Optional[float] = None
    _{f49783e7}: Optional[float] = None
    BonusAD: Optional[float] = None
    _{b4a90a5d}: Optional[float] = None
    BonusHealth: Optional[float] = None
    _{268f634e}: Optional[float] = None
    _{9f2eb1e2}: Optional[float] = None
    DamageReduction: Optional[float] = None
    _{e86b1aa9}: Optional[float] = None
    _{7b9ae201}: Optional[float] = None
    Health: Optional[float] = None
    _{7f1304b2}: Optional[float] = None
    _{2f744e2b}: Optional[float] = None
    _{faa12163}: Optional[str] = None
    _{16394c87}: Optional[float] = None
    _{75994f47}: Optional[float] = None
    _{df962703}: Optional[float] = None
    _{51aec5d2}: Optional[float] = None
    _{cbb3a34f}: Optional[float] = None
    HPPercent: Optional[float] = None
    _{70ed38c6}: Optional[float] = None
    _{d2b7f6f1}: Optional[float] = None
    AttackSpeed: Optional[float] = None
    Duration: Optional[float] = None
    HealthRegen: Optional[float] = None
    HealthThreshold: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Variables":
        data['_{2a50526a}'] = data['{2a50526a}']
        del data['{2a50526a}']

        data['_{3b173c39}'] = data['{3b173c39}']
        del data['{3b173c39}']

        data['_{5263ba40}'] = data['{5263ba40}']
        del data['{5263ba40}']

        data['_{a859d7b0}'] = data['{a859d7b0}']
        del data['{a859d7b0}']

        data['_{5c51b509}'] = data['{5c51b509}']
        del data['{5c51b509}']

        data['_{c9b0e3af}'] = data['{c9b0e3af}']
        del data['{c9b0e3af}']

        data['_{867bc055}'] = data['{867bc055}']
        del data['{867bc055}']

        data['_{ed1f9fc2}'] = data['{ed1f9fc2}']
        del data['{ed1f9fc2}']

        data['_{5cc08b27}'] = data['{5cc08b27}']
        del data['{5cc08b27}']

        data['_{94c6a08c}'] = data['{94c6a08c}']
        del data['{94c6a08c}']

        data['_{17cfa971}'] = data['{17cfa971}']
        del data['{17cfa971}']

        data['_{47343861}'] = data['{47343861}']
        del data['{47343861}']

        data['_{98396b21}'] = data['{98396b21}']
        del data['{98396b21}']

        data['_{5064373e}'] = data['{5064373e}']
        del data['{5064373e}']

        data['_{6c155e99}'] = data['{6c155e99}']
        del data['{6c155e99}']

        data['_{f9f3a081}'] = data['{f9f3a081}']
        del data['{f9f3a081}']

        data['_{02ce80f2}'] = data['{02ce80f2}']
        del data['{02ce80f2}']

        data['_{190fb0a2}'] = data['{190fb0a2}']
        del data['{190fb0a2}']

        data['_{2f805979}'] = data['{2f805979}']
        del data['{2f805979}']

        data['_{2fb1d11d}'] = data['{2fb1d11d}']
        del data['{2fb1d11d}']

        data['_{3f1cec4d}'] = data['{3f1cec4d}']
        del data['{3f1cec4d}']

        data['_{66d8ecb1}'] = data['{66d8ecb1}']
        del data['{66d8ecb1}']

        data['_{6b5aee70}'] = data['{6b5aee70}']
        del data['{6b5aee70}']

        data['_{76882e8f}'] = data['{76882e8f}']
        del data['{76882e8f}']

        data['_{7c799240}'] = data['{7c799240}']
        del data['{7c799240}']

        data['_{7f322ebf}'] = data['{7f322ebf}']
        del data['{7f322ebf}']

        data['_{82e43c84}'] = data['{82e43c84}']
        del data['{82e43c84}']

        data['_{994006f0}'] = data['{994006f0}']
        del data['{994006f0}']

        data['_{9cc303b4}'] = data['{9cc303b4}']
        del data['{9cc303b4}']

        data['_{b6322d58}'] = data['{b6322d58}']
        del data['{b6322d58}']

        data['_{c26236e7}'] = data['{c26236e7}']
        del data['{c26236e7}']

        data['_{f3cab19f}'] = data['{f3cab19f}']
        del data['{f3cab19f}']

        data['_{f90dd382}'] = data['{f90dd382}']
        del data['{f90dd382}']

        data['_{ce492058}'] = data['{ce492058}']
        del data['{ce492058}']

        data['_{471b1a16}'] = data['{471b1a16}']
        del data['{471b1a16}']

        data['_{d0539890}'] = data['{d0539890}']
        del data['{d0539890}']

        data['_{45564848}'] = data['{45564848}']
        del data['{45564848}']

        data['_{97ea7bfc}'] = data['{97ea7bfc}']
        del data['{97ea7bfc}']

        data['_{2fb31c01}'] = data['{2fb31c01}']
        del data['{2fb31c01}']

        data['_{f49783e7}'] = data['{f49783e7}']
        del data['{f49783e7}']

        data['_{b4a90a5d}'] = data['{b4a90a5d}']
        del data['{b4a90a5d}']

        data['_{268f634e}'] = data['{268f634e}']
        del data['{268f634e}']

        data['_{9f2eb1e2}'] = data['{9f2eb1e2}']
        del data['{9f2eb1e2}']

        data['_{e86b1aa9}'] = data['{e86b1aa9}']
        del data['{e86b1aa9}']

        data['_{7b9ae201}'] = data['{7b9ae201}']
        del data['{7b9ae201}']

        data['_{7f1304b2}'] = data['{7f1304b2}']
        del data['{7f1304b2}']

        data['_{2f744e2b}'] = data['{2f744e2b}']
        del data['{2f744e2b}']

        data['_{faa12163}'] = data['{faa12163}']
        del data['{faa12163}']

        data['_{16394c87}'] = data['{16394c87}']
        del data['{16394c87}']

        data['_{75994f47}'] = data['{75994f47}']
        del data['{75994f47}']

        data['_{df962703}'] = data['{df962703}']
        del data['{df962703}']

        data['_{51aec5d2}'] = data['{51aec5d2}']
        del data['{51aec5d2}']

        data['_{cbb3a34f}'] = data['{cbb3a34f}']
        del data['{cbb3a34f}']

        data['_{70ed38c6}'] = data['{70ed38c6}']
        del data['{70ed38c6}']

        data['_{d2b7f6f1}'] = data['{d2b7f6f1}']
        del data['{d2b7f6f1}']

        return Variables(**data)

from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class HextechAugment(BaseModel):
    name: str = ''
    slug: str = ''
    tier: int = 0
    bonus: str = ''

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "HextechAugment":
        return HextechAugment(**data)

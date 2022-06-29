from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Observers(BaseModel):
    encryptionKey: str = ''

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Observers":
        return Observers(**data)

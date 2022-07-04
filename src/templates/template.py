from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
{imports}

class {className}(BaseModel{variant}):
{attributes}

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict(){to_dict_mapping}
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "{className}": {from_dict_mapping}
        return {className}(**data)

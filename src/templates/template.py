from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Union, Optional
from dacite import from_dict

from {json_path}.base_dataclass import BaseDataclass
{imports}

@dataclass
class {className}(BaseDataclass):
{attributes}

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self){to_dict_mapping}{to_dict_matching}
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "{className}":{from_dict_matching}{from_dict_mapping}
        return from_dict(cls, data=data)

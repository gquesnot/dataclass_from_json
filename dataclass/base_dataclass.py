from abc import ABC
from typing import Any, Dict
from dacite import from_dict
from pydantic import Field, dataclasses
from pydantic.dataclasses import dataclass


@dataclass
class BaseDataclass(ABC):
    pass

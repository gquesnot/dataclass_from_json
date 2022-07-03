from abc import ABC
from typing import Any, Dict
from pydantic.dataclasses import dataclass


@dataclass
class BaseDataclass(ABC):
    pass

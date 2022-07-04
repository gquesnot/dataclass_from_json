from abc import ABC
from typing import Any, Dict
from pydantic.dataclasses import dataclass
from strenum import StrEnum


@dataclass
class BaseEnum(StrEnum):

    def keys(self):
        return list(self._members_.values())

    def values(self):
        return list(self._members_.keys())

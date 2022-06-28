from dataclasses import dataclass, field
from typing import Optional

from src.enums.type_enum import MyTypeBase, MyTypeWithMapping


@dataclass
class SchemaMatching:
    from_: Optional[str] = field(default=None)


@dataclass
class SchemaMapping:
    className: Optional[str] = field(default=None)
    type_: Optional[MyTypeBase] = field(default=None)
    nullable: bool = field(default=False)


@dataclass
class SchemaMappingMatching:
    key: str
    nullable: bool = field(default=False)
    mapping: SchemaMapping = field(default_factory=SchemaMapping)
    matching: SchemaMatching = field(default_factory=SchemaMatching)

    def hasMatching(self) -> bool:
        return self.matching.from_ is not None

    def hasMapping(self) -> bool:
        return self.mapping.className is not None

    def hasBoth(self) -> bool:
        return self.hasMapping() and self.hasMatching()

    def from_dict_str(self) -> str:
        result = ""
        if self.hasMapping() and self.mapping.type_ == MyTypeWithMapping.LIST_ROOT:
            return ' ' * 8 + "data = {" \
                             f"'{self.key}': [{self.getFromDictToDict('v')} for v in data]" \
                             "}"
        if self.nullable:
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        base = f"{self.getStrBefore()}data['{self.key}'] = "
        if self.hasMatching():
            result += f"{base}data['{self.matching.from_}']\n"
            result += f"{self.getStrBefore()}del data['{self.matching.from_}']"
            if not self.hasMapping():
                result += "\n"
        if self.hasMapping():
            if self.mapping.type_ == MyTypeWithMapping.DICT_LIST:
                result += f"{base}[{self.getFromDictToDict('v')} for v in data['{self.key}'].values()]\n"
            elif self.mapping.type_ == MyTypeWithMapping.LIST:
                result += f"{base}[{self.getFromDictToDict('v')} for v in data['{self.key}']]"
            elif self.mapping.type_ == MyTypeWithMapping.DICT:
                result += f"{base}{{k: {self.getFromDictToDict('v')} for k, v in data['{self.key}'].items()}}"
            else:
                dataName = f"data['{self.key}']"
                result += f"{base}{self.getFromDictToDict(dataName)}"
        return result

    def getStrBefore(self):
        return ' ' * (8 if not self.nullable else 12)

    def getFromDictToDict(self, dataName: str):
        return f"{self.mapping.className}.from_dict({dataName}).to_dict()"

    def to_dict_str(self) -> str:
        result = ""
        if self.nullable and self.hasMatching():
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        if self.hasMatching():
            result += f"{self.getStrBefore()}data['{self.matching.from_}'] = data['{self.key}']"
        return result

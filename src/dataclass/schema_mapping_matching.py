from dataclasses import dataclass, field
from typing import Optional

from src.enums.complex_type import ComplexType


@dataclass
class SchemaMatching:
    from_: Optional[str] = field(default=None)
    rootListNotClass: bool = field(default=False)


@dataclass
class SchemaMapping:
    className: Optional[str] = field(default=None)


@dataclass
class SchemaMappingMatching:
    key: str
    type: Optional["MyType"] = field(default=None)
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
        if self.type and self.type.isListRoot():

            if self.type.child.isClass():
                return ' ' * 8 + \
                    "data = {" f"'{self.key}': [{self.getFromDictToDict('v')} for v in data]" "}"
            else:
                return ' ' * 8 + "data = {" + f"'{self.key}': data" + "}"
        if self.type and self.type.nullable:
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        base = f"{self.getStrBefore()}data['{self.key}'] = "
        if self.hasMatching():
            result += f"{base}data['{self.matching.from_}']\n"
            result += f"{self.getStrBefore()}del data['{self.matching.from_}']"
            if not self.hasMapping():
                result += "\n"
        if self.hasMapping():
            if self.type.isList():
                result += f"{base}[{self.getFromDictToDict('v')} for v in data['{self.key}']]"
            elif self.type.isDict():
                result += f"{base}{{k: {self.getFromDictToDict('v')} for k, v in data['{self.key}'].items()}}"
            else:
                dataName = f"data['{self.key}']"
                result += f"{base}{self.getFromDictToDict(dataName)}"
        return result

    def getStrBefore(self):
        return ' ' * (12 if self.type and self.type.nullable else 8)

    def getFromDictToDict(self, dataName: str):
        return f"{self.mapping.className}.from_dict({dataName}).to_dict()"

    def to_dict_str(self) -> str:
        result = ""
        if self.hasMatching() and self.hasMapping() and self.type.nullable:
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        if self.hasMatching():
            result += f"{self.getStrBefore()}data['{self.matching.from_}'] = data['{self.key}']"
        return result

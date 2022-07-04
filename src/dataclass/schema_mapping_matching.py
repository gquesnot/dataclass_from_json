from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SchemaMatching:
    from_: Optional[str] = field(default=None)
    root_list_not_class: bool = field(default=False)


@dataclass
class SchemaMapping:
    className: Optional[str] = field(default=None)


@dataclass
class SchemaMappingMatching:
    key: str
    type: Optional["CustomType"] = field(default=None)
    mapping: SchemaMapping = field(default_factory=SchemaMapping)
    matching: SchemaMatching = field(default_factory=SchemaMatching)

    def has_matching(self) -> bool:
        return self.matching.from_ is not None

    def has_mapping(self) -> bool:
        return self.mapping.className is not None

    def has_both(self) -> bool:
        return self.has_mapping() and self.has_matching()

    def from_dict_str(self) -> str:
        result = ""
        if self.type and self.type.is_list_root():

            if self.type.child.is_class():
                return (
                        " " * 8 + "data = {"
                                  f"'{self.key}': [{self.get_from_dict_to_dict('v')} for v in data]"
                                  "}"
                )
            else:
                return " " * 8 + "data = {" + f"'{self.key}': data" + "}"
        if self.type and self.type.nullable:
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        base = f"{self.get_str_before()}data['{self.key}'] = "
        if self.has_matching():
            result += f"{base}data['{self.matching.from_}']\n"
            result += f"{self.get_str_before()}del data['{self.matching.from_}']"
            if not self.has_mapping():
                result += "\n"
        if self.has_mapping():
            if self.type.is_list():
                result += (
                    f"{base}[{self.get_from_dict_to_dict('v')} for v in data['{self.key}']]"
                )
            elif self.type.is_dict():
                result += f"{base}{{k: {self.get_from_dict_to_dict('v')} for k, v in data['{self.key}'].items()}}"
            else:
                data_name = f"data['{self.key}']"
                result += f"{base}{self.get_from_dict_to_dict(data_name)}"
        return result

    def get_str_before(self):
        return " " * (12 if self.type and self.type.nullable else 8)

    def get_from_dict_to_dict(self, data_name: str):
        return f"{self.mapping.className}.from_dict({data_name}).to_dict()"

    def to_dict_str(self) -> str:
        result = ""
        if self.has_matching() and self.has_mapping() and self.type.nullable:
            result += f"{' ' * 8}if '{self.key}' in data:\n"
        if self.has_matching():
            result += f"{self.get_str_before()}data['{self.matching.from_}'] = data['{self.key}']"
        return result

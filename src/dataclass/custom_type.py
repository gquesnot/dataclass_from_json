from dataclasses import dataclass, field
from typing import Optional

from src.enums.complex_type import ComplexType
from src.enums.simple_type import SimpleType
from src.utils.string_manipulation import to_class_style, camel_case, key_is_a_valid_dict_attribute


@dataclass
class CustomType:
    simple: Optional[SimpleType] = field(default=None)
    complex: Optional[ComplexType] = field(default=None)
    child: Optional["CustomType"] = field(default=None)
    name: Optional[str] = field(default=None)
    nullable: bool = field(default=False)

    def __add__(self, other):
        if not self.nullable and other.nullable:
            self.set_nullable()
        if self.is_list_empty() and not other.is_list_empty():
            return other
        return self

    @classmethod
    def from_data(cls, name, data, has_nullable=False):
        new_type = cls(name=name, nullable=data is None or has_nullable)

        new_type.simple = new_type.get_simple(data)
        if new_type.is_complex() and new_type.simple != SimpleType.NONE:
            new_type.complex, has_child, child_data, nullable = new_type.get_complex(data)
            if has_child:
                new_type.child = cls.from_data("", child_data, nullable)
        return new_type

    @staticmethod
    def get_simple(value):
        if isinstance(value, list):
            return SimpleType.LIST
        elif isinstance(value, dict):
            return SimpleType.DICT
        elif isinstance(value, str):
            return SimpleType.STRING
        elif isinstance(value, bool):
            return SimpleType.BOOL
        elif isinstance(value, float):
            return SimpleType.FLOAT
        elif isinstance(value, int):
            return SimpleType.INT
        elif value is None:
            return SimpleType.NONE
        else:
            raise Exception("Unknown Simple type_: " + str(type(value)))

    def get_default_with_field(self):
        default = self.get_default()
        if (self.is_list() or self.is_dict() or self.has_class()) and not self.nullable:
            return f"Field(default_factory={default})"
        else:
            return f"Field(default={default})"

    def to_string(self):
        result = ""
        if self.is_none():
            return "Any"
        elif self.is_simple():
            result = self.simple.value
        elif self.is_list_root():

            if self.child.is_simple():
                result = f"List[{self.child.simple.value}]"
            else:
                result = f"List[{self.child.to_string()}]"
        elif self.is_complex() and not self.is_none():
            if self.is_class():
                result = to_class_style(self.name)
            elif self.is_dict():
                if self.has_class():
                    result = f"Dict[str, {to_class_style(self.name)}]"
                else:
                    result = f"Dict[str, {self.child.to_string()}]"
            elif self.is_list():
                if self.has_class():
                    result = f"List[{to_class_style(self.name)}]"
                elif self.is_list_empty():
                    result = f"List[Any]"
                else:
                    result = f"List[{self.child.to_string()}]"
            else:
                raise Exception("Unknown complex type_: " + str(self.complex))
        else:
            raise Exception("Unknown type_: " + str(self.simple))
        return f"Optional[{result}]" if self.nullable else result

    def get_default(self):
        if self.nullable or self.is_none():
            return "None"
        elif self.simple == SimpleType.STRING:
            return "''"
        elif self.simple == SimpleType.INT:
            return "0"
        elif self.simple == SimpleType.FLOAT:
            return "0.0"
        elif self.simple == SimpleType.BOOL:
            return "False"
        elif self.simple == SimpleType.LIST:
            return "list"
        elif self.simple == SimpleType.DICT:
            return "dict"
        elif self.is_class():
            return camel_case(self.name)
        else:
            raise Exception("Unknown type_: " + str(self.simple))

    def get_complex(self, value):
        if isinstance(value, list):
            if len(value) == 0:
                return ComplexType.LIST_EMPTY, False, None, True
            types, nullable, is_valid = self.get_all_types_and_without_none(value)
            if is_valid:
                type_ = types.pop()
                if self.is_simple(type_):
                    child_value = value[0] if len(value) else None
                    return ComplexType.LIST_SIMPLE, True, child_value, nullable
                else:
                    if type_ == SimpleType.LIST:
                        return (
                            ComplexType.LIST_LIST,
                            True,
                            self.get_best_list(value),
                            nullable,
                        )
                    elif type_ == SimpleType.DICT:
                        return ComplexType.LIST_CLASS, False, None, nullable
                    else:
                        raise Exception("Unknown list child type_: " + str(type_))
            else:
                raise Exception("Invalid list: " + str(types))
        elif isinstance(value, dict):
            types, nullable, has_one_value = self.get_all_types_and_without_none(
                value.values()
            )
            all_keys_are_valid = all([key_is_a_valid_dict_attribute(k) for k in value.keys()])
            key_are_all_num = all([k.isnumeric() for k in value.keys()])
            name_end_by_s = self.name[-1] == "s"
            if has_one_value:
                type_ = types.pop()
                if self.is_simple(type_):
                    if not all_keys_are_valid or key_are_all_num or name_end_by_s:
                        child_value = (
                            list(value.values())[0] if len(value.values()) else None
                        )
                        return ComplexType.DICT_SIMPLE, True, child_value, nullable
                    else:
                        return ComplexType.CLASS, False, None, nullable
                else:
                    if type_ == SimpleType.LIST:
                        return (
                            ComplexType.DICT_LIST,
                            True,
                            self.get_best_list(value.values()),
                            nullable,
                        )
                    elif type_ == SimpleType.DICT:
                        return ComplexType.DICT_CLASS, False, None, nullable
                    else:
                        raise Exception("Unknown dict child type_: " + str(type_))
            else:
                if all_keys_are_valid and not key_are_all_num:
                    return ComplexType.CLASS, False, None, nullable
                elif all([self.is_simple(t) for t in types]) and key_are_all_num:
                    return ComplexType.DICT_SIMPLE, True, None, nullable
                else:
                    raise Exception("Invalid dict: " + str(types))
        else:
            raise Exception("Unknown Complex type_: " + str(type(value)))

    def get_all_types_and_without_none(self, datas):
        all_types = set([self.get_simple(v) for v in datas])
        nullable = SimpleType.NONE in all_types
        if nullable:
            all_types = all_types - {SimpleType.NONE}
        if SimpleType.FLOAT in all_types and SimpleType.INT in all_types:
            all_types -= {SimpleType.INT}
        if len(all_types) == 0:
            return {SimpleType.ANY}, False, True
        elif len(all_types) == 1:
            return all_types, nullable, True
        else:
            return all_types, nullable, False

    @staticmethod
    def get_best_list(values):
        res = None
        for v in values:
            if isinstance(v, list):
                if res is None:
                    res = v
                elif len(res) < len(v):
                    res = v
        return res

    def set_nullable(self):
        self.nullable = True

    def is_complex(self, type_: Optional[SimpleType] = None) -> bool:
        return not self.is_simple(type_)

    def is_simple(self, type_: Optional[SimpleType] = None) -> bool:
        type_ = type_ if type_ is not None else self.simple
        return type_ not in [SimpleType.LIST, SimpleType.DICT, SimpleType.NONE]

    def is_list_root(self):
        return self.complex == ComplexType.LIST_ROOT

    def is_class(self):
        return self.complex == ComplexType.CLASS

    def has_class(self):
        return (
                self.is_dict_class()
                or self.is_list_class()
                or self.is_class()
                or self.is_list_root()
        )

    def is_dict(self):
        return self.is_dict_simple() or self.is_dict_class() or self.is_dict_list()

    def is_list(self):
        return (
                self.is_list_simple()
                or self.is_list_class()
                or self.is_list_list()
                or self.is_list_empty()
        )

    def is_list_class(self):
        return self.complex == ComplexType.LIST_CLASS

    def is_list_empty(self):
        return self.complex == ComplexType.LIST_EMPTY

    def is_list_simple(self):
        return self.complex == ComplexType.LIST_SIMPLE

    def is_list_list(self):
        return self.complex == ComplexType.LIST_LIST

    def is_dict_class(self):
        return self.complex == ComplexType.DICT_CLASS

    def is_dict_simple(self):
        return self.complex == ComplexType.DICT_SIMPLE

    def is_dict_list(self):
        return self.complex == ComplexType.DICT_LIST

    def is_none(self):
        return self.simple == SimpleType.NONE or self.simple is None

    def has_child(self):
        return self.child is not None

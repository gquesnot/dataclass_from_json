from strenum import StrEnum

from src.utils.string_manipulation import keyIsAValidDictAttribute


class MyTypeBase(StrEnum):
    pass


class SimpleType(MyTypeBase):
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    NONE = "None"


class ComplexType(MyTypeBase):
    LIST = "List"
    DICT = "Dict"
    DICT_LIST = "DictList"
    LIST_ROOT = "ListRoot"
    CLASS = "Class"
    DEFAULT= "Default"


def type_from_value(value):
    if isinstance(value, list):
        return ComplexType.LIST, None
    elif isinstance(value, dict):
        keys = list(value.keys())
        if len(keys) == 0:
            return ComplexType.DICT, None
        allNumeric = all([key.isnumeric() for key in keys])
        allValidKeys = all([keyIsAValidDictAttribute(key) for key in keys])
        if allNumeric:
            return ComplexType.DICT_LIST, None
        elif not allValidKeys:
            return ComplexType.DICT, None
        else:
            return ComplexType.CLASS, None
    elif isinstance(value, str):
        return ComplexType.DEFAULT, SimpleType.STRING
    elif isinstance(value, bool):
        return ComplexType.DEFAULT, SimpleType.BOOL
    elif isinstance(value, int):
        return ComplexType.DEFAULT, SimpleType.INT
    elif isinstance(value, float):
        return ComplexType.DEFAULT, SimpleType.FLOAT

    elif value is None:
        return ComplexType.DEFAULT, SimpleType.NONE
    else:
        raise Exception("Unknown type_: " + str(type(value)))


def get_default_value(type_: "MyTypeBase", nullable):
    if nullable or type_ == SimpleType.NONE:
        return "None"
    elif type_ == SimpleType.STRING:
        return "''"
    elif type_ == SimpleType.INT:
        return "0"
    elif type_ == SimpleType.FLOAT:
        return "0.0"
    elif type_ == SimpleType.BOOL:
        return "False"
    else:
        raise Exception("Unknown type_: " + str(type_))



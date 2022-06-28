from strenum import StrEnum

from src.utils.string_manipulation import keyIsAValidDictAttribute


class MyTypeBase(StrEnum):
    pass


class MyTypeDefault(MyTypeBase):
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    NONE = "None"
    ANY = "Any"
    DEFAULT = "Default"


class MyTypeWithMapping(MyTypeBase):
    LIST = "List"
    DICT = "Dict"
    DICT_LIST = "DictList"
    LIST_ROOT = "ListRoot"
    CLASS = "Class"


def type_from_value(value):
    if isinstance(value, list):
        return MyTypeWithMapping.LIST
    elif isinstance(value, dict):
        keys = list(value.keys())
        if len(keys) == 0:
            return MyTypeWithMapping.DICT
        allNumeric = all([key.isnumeric() for key in keys])
        allValidKeys = all([keyIsAValidDictAttribute(key) for key in keys])
        if allNumeric:
            return MyTypeWithMapping.DICT_LIST
        elif not allValidKeys:
            return MyTypeWithMapping.DICT
        else:
            return MyTypeWithMapping.CLASS
    elif isinstance(value, str):
        return MyTypeDefault.STRING
    elif isinstance(value, bool):
        return MyTypeDefault.BOOL
    elif isinstance(value, int):
        return MyTypeDefault.INT
    elif isinstance(value, float):
        return MyTypeDefault.FLOAT

    elif value is None:
        return MyTypeDefault.NONE
    else:
        raise Exception("Unknown type_: " + str(type(value)))


def get_default_value(type_: "MyTypeBase", nullable):
    if nullable or type_ == MyTypeDefault.NONE:
        return "None"
    elif type_ == MyTypeDefault.STRING:
        return "''"
    elif type_ == MyTypeDefault.INT:
        return "0"
    elif type_ == MyTypeDefault.FLOAT:
        return "0.0"
    elif type_ == MyTypeDefault.BOOL:
        return "False"
    else:
        raise Exception("Unknown type_: " + str(type_))



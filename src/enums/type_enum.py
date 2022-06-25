from strenum import StrEnum


class MyTypeEnum(StrEnum):
    LIST = "List"
    DICT = "Dict"
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    NONE = "None"
    ANY = "Any"
    CLASS = "Class"

    @classmethod
    def from_value(cls, value):
        if isinstance(value, list):
            return cls.LIST.value
        elif isinstance(value, dict):
            return cls.DICT.value
        elif isinstance(value, str):
            return cls.STRING.value
        elif isinstance(value, int):
            return cls.INT.value
        elif isinstance(value, float):
            return cls.FLOAT.value
        elif isinstance(value, bool):
            return cls.BOOL.value
        elif value is None:
            return cls.NONE.value
        else:
            raise Exception("Unknown type: " + str(type(value)))

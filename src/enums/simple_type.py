from strenum import StrEnum


class SimpleType(StrEnum):
    LIST = "List"
    DICT = "Dict"
    STRING = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    ANY = "Any"
    NONE = "None"
    EMPTY = "Empty"

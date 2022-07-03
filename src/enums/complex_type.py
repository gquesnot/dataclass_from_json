from strenum import StrEnum


class ComplexType(StrEnum):
    DICT_SIMPLE = "DictSimple"
    DICT_CLASS = "DictClass"
    DICT_LIST = "DictList"
    CLASS = "Class"
    LIST_ROOT = "ListRoot"
    LIST_EMPTY = "ListEmpty"
    LIST_LIST = "ListWithList"
    LIST_SIMPLE = "ListSimple"
    LIST_CLASS = "ListClass"

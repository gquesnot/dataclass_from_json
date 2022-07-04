import keyword
from re import sub


def camel_case(s):
    """
    Convert a string to camel case.
    """
    s = s.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(s) == 0:
        return s
    return s[0] + "".join(i.capitalize() for i in s[1:])


def snake_case(s):
    """
    Convert a string to snake case.
    """
    s = sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return sub("([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def remove_extension(s):
    """
    Remove the extension from a file name.
    """
    return s.split(".")[0]


def to_class_style(s):
    """
    Convert a string to class style.
    """
    return s[0].upper() + s[1:]


def check_s(s):
    """
    Check if a string end with s or S
    """
    return s[-1] == "s"


def string_is_a_dict_key(s: str):
    """
    Check if a string is a valid dict key.
    """

    if s.isalnum():
        return check_s(s)
    return True


def dict_has_valid_attribute(d: dict):
    """
    Check if a dict is a dict.
    """

    for key in d.keys():
        if not key.isalnum():
            return False
    return True


def get_x_space(x):
    return " " * x


def key_is_a_valid_dict_attribute(key: str):
    return key.isalnum()


def key_is_a_valid_attribute(key: str):
    """
    Check if a key is a valid attribute.
    """

    # check if the key is a valid attribute name
    # 1. check if the key is a valid python keyword
    # 2. check if the key is not a Type
    if keyword.iskeyword(key):
        return False
    if not key.isidentifier():
        return False
    if key in (
            "float",
            "int",
            "str",
            "bool",
            "None",
            "list",
            "dict",
            "set",
            "tuple",
            "range",
            "tuple",
            "frozenset",
            "type",
    ):
        return False

    return True


def get_base_type_str(value) -> str:
    if value is None:
        return "None"
    else:
        return value.__class__.__name__


def is_base_type(value):
    return (
            isinstance(value, str)
            or isinstance(value, int)
            or isinstance(value, float)
            or isinstance(value, bool)
            or value is None
    )


def get_sub_key(key):
    if check_s(key):
        key = key[:-1]
    else:
        key = key + "Index"
    return key


def get_list_dict_sub_key(parent_name, parent_key):
    return get_sub_key(parent_name)

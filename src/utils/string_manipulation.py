import keyword
from re import sub


def camelCase(s):
    """
    Convert a string to camel case.
    """
    s = s.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(s) == 0:
        return s
    return s[0] + ''.join(i.capitalize() for i in s[1:])


def snakeCase(s):
    """
    Convert a string to snake case.
    """
    s = sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def removeExtension(s):
    """
    Remove the extension from a file name.
    """
    return s.split('.')[0]


def toClassStyle(s):
    """
    Convert a string to class style.
    """
    return s[0].upper() + s[1:]


def checkS(s):
    """
    Check if a string end with s or S
    """
    return s[-1] == "s"


def stringIsADictKey(s: str):
    """
    Check if a string is a valid dict key.
    """

    if s.isalnum():
        return checkS(s)
    return True


def dictHasValidAttribute(d: dict):
    """
    Check if a dict is a dict.
    """

    for key in d.keys():
        if not key.isalnum():
            return False
    return True


def getXSpace(x):
    return " " * x

def keyIsAValidAttribute(key: str):
    """
    Check if a key is a valid attribute.
    """

    # check if the key is a valid attribute name
    # 1. check if the key is a valid python keyword
    # 2. check if the key is a valid python variable name
    # 3. check if the key contains invalid character
    if keyword.iskeyword(key):
        return False
    if not key.isidentifier():
        return False
    return True


def getBaseTypeStr(value) -> str:
    if value is None:
        return "None"
    else:
        return value.__class__.__name__


def isBaseType(value):
    return isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value,
                                                                                                      bool) or value is None


def getSubKey(key):
    if checkS(key):
        key = key[:-1]
    else:
        key = key + "Index"
    return key

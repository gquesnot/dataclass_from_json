from dataclasses import dataclass, field
from typing import Optional

from src.enums.complex_type import ComplexType
from src.enums.simple_type import SimpleType
from src.utils.string_manipulation import toClassStyle, camelCase, keyIsAValidDictAttribute


@dataclass
class CustomType:
    simple: Optional[SimpleType] = field(default=None)
    complex: Optional[ComplexType] = field(default=None)
    child: Optional["CustomType"] = field(default=None)
    name: Optional[str] = field(default=None)
    nullable: bool = field(default=False)

    def __add__(self, other):
        if not self.nullable and other.nullable:
            self.setNullable()
        if self.isListEmpty() and not other.isListEmpty():
            return other
        return self


    @classmethod
    def from_data(cls, name, data, hasNullable=False):
        newType = cls(name=name, nullable=data is None or hasNullable)

        newType.simple = newType.getSimple(data)
        if newType.isComplex() and newType.simple != SimpleType.NONE:
            newType.complex, hasChild, childData, nullable = newType.getComplex(data)
            if hasChild:
                newType.child = cls.from_data("", childData, nullable)
        return newType

    @staticmethod
    def getSimple(value):
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

    def getDefaultWithField(self):
        default = self.getDefault()
        if (self.isList() or self.isDict() or self.hasClass()) and not self.nullable:
            return f"Field(default_factory={default})"
        else:
            return f"Field(default={default})"

    def toString(self):
        result = ""
        if self.isNone():
            return "Any"
        elif self.isSimple():
            result = self.simple.value
        elif self.isListRoot():

            if self.child.isSimple():
                result = f"List[{self.child.simple.value}]"
            else:
                result = f"List[{self.child.toString()}]"
        elif self.isComplex() and not self.isNone():
            if self.isClass():
                result = toClassStyle(self.name)
            elif self.isDict():
                if self.hasClass():
                    result = f"Dict[str, {toClassStyle(self.name)}]"
                else:
                    result = f"Dict[str, {self.child.toString()}]"
            elif self.isList():
                if self.hasClass():
                    result = f"List[{toClassStyle(self.name)}]"
                elif self.isListEmpty():
                    result = f"List[Any]"
                else:
                    result = f"List[{self.child.toString()}]"
            else:
                raise Exception("Unknown complex type_: " + str(self.complex))
        else:
            raise Exception("Unknown type_: " + str(self.simple))
        return f"Optional[{result}]" if self.nullable else result

    def getDefault(self):
        if self.nullable or self.isNone():
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
        elif self.isClass():
            return camelCase(self.name)
        else:
            raise Exception("Unknown type_: " + str(self.simple))

    def getComplex(self, value):
        if isinstance(value, list):
            if len(value) == 0:
                return ComplexType.LIST_EMPTY, False, None, True
            types, nullable, isValid = self.getAllTypesAndWithoutNone(value)
            if isValid:
                type_ = types.pop()
                if self.isSimple(type_):
                    childValue = value[0] if len(value) else None
                    return ComplexType.LIST_SIMPLE, True, childValue, nullable
                else:
                    if type_ == SimpleType.LIST:
                        return ComplexType.LIST_LIST, True, self.getBestList(value), nullable
                    elif type_ == SimpleType.DICT:
                        return ComplexType.LIST_CLASS, False, None, nullable
                    else:
                        raise Exception("Unknown list child type_: " + str(type_))
            else:
                raise Exception("Invalid list: " + str(types))
        elif isinstance(value, dict):
            types, nullable, hasOneValue = self.getAllTypesAndWithoutNone(value.values())
            allKeysAreValid = all([keyIsAValidDictAttribute(k) for k in value.keys()])
            keyAreAllNum = all([k.isnumeric() for k in value.keys()])
            nameEndByS = self.name[-1] == "s"
            if hasOneValue:
                type_ = types.pop()
                if self.isSimple(type_):
                    if not allKeysAreValid or keyAreAllNum or nameEndByS:
                        childValue = list(value.values())[0] if len(value.values()) else None
                        return ComplexType.DICT_SIMPLE, True, childValue, nullable
                    else:
                        return ComplexType.CLASS, False, None, nullable
                else:
                    if type_ == SimpleType.LIST:
                        return ComplexType.DICT_LIST, True, self.getBestList(value.values()), nullable
                    elif type_ == SimpleType.DICT:
                        return ComplexType.DICT_CLASS, False, None, nullable
                    else:
                        raise Exception("Unknown dict child type_: " + str(type_))
            else:
                if allKeysAreValid and not keyAreAllNum:
                    return ComplexType.CLASS, False, None, nullable
                elif all([self.isSimple(t) for t in types]) and keyAreAllNum:
                    return ComplexType.DICT_SIMPLE, True, None, nullable
                else:
                    raise Exception("Invalid dict: " + str(types))
        else:
            raise Exception("Unknown Complex type_: " + str(type(value)))

    def getAllTypesAndWithoutNone(self, datas):
        allTypes = set([self.getSimple(v) for v in datas])
        nullable = SimpleType.NONE in allTypes
        if nullable:
            allTypes = allTypes - {SimpleType.NONE}
        if SimpleType.FLOAT in allTypes and SimpleType.INT in allTypes:
            allTypes -= {SimpleType.INT}
        if len(allTypes) == 0:
            return {SimpleType.ANY}, False, True
        elif len(allTypes) == 1:
            return allTypes, nullable, True
        else:
            return allTypes, nullable, False

    @staticmethod
    def getBestList(values):
        res = None
        for v in values:
            if isinstance(v, list):
                if res is None:
                    res = v
                elif len(res) < len(v):
                    res = v
        return res

    def setNullable(self):
        self.nullable = True

    def isComplex(self, type_: Optional[SimpleType] = None) -> bool:
        return not self.isSimple(type_)

    def isSimple(self, type_: Optional[SimpleType] = None) -> bool:
        type_ = type_ if type_ is not None else self.simple
        return type_ not in [SimpleType.LIST, SimpleType.DICT, SimpleType.NONE]

    def isListRoot(self):
        return self.complex == ComplexType.LIST_ROOT

    def isClass(self):
        return self.complex == ComplexType.CLASS

    def hasClass(self):
        return self.isDictClass() or self.isListClass() or self.isClass() or self.isListRoot()

    def isDict(self):
        return self.isDictSimple() or self.isDictClass() or self.isDictList()

    def isList(self):
        return self.isListSimple() or self.isListClass() or self.isListList() or self.isListEmpty()

    def isListClass(self):
        return self.complex == ComplexType.LIST_CLASS

    def isListEmpty(self):
        return self.complex == ComplexType.LIST_EMPTY

    def isListSimple(self):
        return self.complex == ComplexType.LIST_SIMPLE

    def isListList(self):
        return self.complex == ComplexType.LIST_LIST

    def isDictClass(self):
        return self.complex == ComplexType.DICT_CLASS

    def isDictSimple(self):
        return self.complex == ComplexType.DICT_SIMPLE

    def isDictList(self):
        return self.complex == ComplexType.DICT_LIST

    def isNone(self):
        return self.simple == SimpleType.NONE or self.simple == None

    def hasChild(self):
        return self.child is not None

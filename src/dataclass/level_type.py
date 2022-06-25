from dataclasses import dataclass, field
from typing import Optional, List

from src.enums.type_enum import MyTypeEnum
from src.utils.string_manipulation import toClassStyle


@dataclass
class LevelType:
    primary: Optional[str] = None
    secondary: List[str] = field(default_factory=list)
    nullable: bool = False

    def __eq__(self, other):
        return self.primary == other.primary and self.secondary == other.secondary

    def addSecondary(self, secondary):
        self.secondary.extend(secondary)
        self.secondary = list(set(self.secondary))
        if MyTypeEnum.INT.value in self.secondary and MyTypeEnum.FLOAT.value in self.secondary:
            self.secondary.remove(MyTypeEnum.INT.value)

    def canAdd(self, other):
        return self.primary == other.primary or other.primary is None and other.nullable is True

    def __add__(self, other):
        if isinstance(other, LevelType):
            if self.canAdd(other):
                self.addSecondary(other.secondary)
                self.nullable = other.nullable if other.nullable is True else self.nullable
                return self
        return self

    def __str__(self):
        sCpy = self.secondary.copy()
        if len(self.secondary) == 0:
            result = MyTypeEnum.ANY.value
        elif len(self.secondary) == 1:
            result = str(sCpy.pop())
        else:
            result = ", ".join(x for x in sCpy)
            result = f"Union[{result}]"

        if self.primary == MyTypeEnum.LIST.value:
            result = f"List[{result}]"
        elif self.primary == MyTypeEnum.DICT.value:
            result = f"Dict[str, {result}]"
        elif self.primary is not None:
            result = f"{self.primary}"
        if self.nullable and result != MyTypeEnum.NONE.value:
            result = f"Optional[{result}]"
        return result


@dataclass()
class LevelMultiType:
    types: List[LevelType] = field(default_factory=list)
    nullable: bool = False

    def addType(self, data):
        newType = LevelType()
        if isinstance(data, list):
            newType.primary = MyTypeEnum.LIST.value
        elif isinstance(data, dict):
            newType.primary = MyTypeEnum.DICT.value
        elif data is None:
            newType.nullable = True
        else:
            newType.addSecondary([MyTypeEnum.from_value(data)])
        self.addNewType(newType)

    @staticmethod
    def addTypeAny():
        newType = LevelType()
        newType.secondary = [MyTypeEnum.ANY.value]

    def addChildren(self, children: List["Level"]):
        mainType = self.types[0]
        for child in children:

            if child.type_ is not None:
                if len(child.type_.types) > 1:
                    print('WARNING: Multiple types for child ', child)
                    # base = child.type_.types[0]
                    # for type_ in child.type_.types[1:]:
                    #     if base.canAdd(type_):
                    #         base = base + type_
                    # if mainType.canAdd(base):
                    #     mainType = mainType + base
                else:

                    # if mainType.canAdd(child.type_.types[0]):
                    #     mainType = mainType + child.type_.types[0]
                    mainType.addSecondary(child.type_.types[0].secondary)

    def addNewType(self, type_: LevelType):
        found = False
        for i, t in enumerate(self.types):
            if t.canAdd(type_):
                self.types[i] = t + type_
                found = True
                break
        if not found:
            self.types.append(type_)

    def addClass(self, class_):
        newType = LevelType()
        newType.primary = class_
        self.addNewType(newType)

    def addRootClass(self, className):
        newType = LevelType(primary=toClassStyle(className))
        self.types = [newType]

    def addRootList(self, children):
        if len(children) != 1:
            raise Exception("Root list must have only one child")
        newType = LevelType(primary=MyTypeEnum.LIST.value, secondary=[children[0].type_.types[0].primary])
        self.addNewType(newType)

    def __str__(self):
        typesCpy = self.types.copy()
        if len(self.types) == 0:
            return "None"
        elif len(self.types) == 1:
            return str(typesCpy[0])
        else:
            result = ", ".join(str(x) for x in typesCpy)
            result = f"Union[{result}]"
            return result

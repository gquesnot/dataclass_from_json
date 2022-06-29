from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from typing import Optional, List, Union

from src.enums.type_enum import SimpleType, ComplexType


@dataclass
class SchemaType:
    type: Optional[ComplexType] = None
    name: Optional[str] = None
    children: List["SchemaType"] = field(default_factory=list)
    nullable: bool = False

    def hasType(self):
        return self.type is not None


    def isComplex(self) -> bool:
        return self.type != ComplexType.DEFAULT

    def isSimple(self) -> bool:
        return self.type == ComplexType.DEFAULT

    def hasNullableChildren(self) -> bool:
        return any([child.nullable for child in self.children])

    def isClass(self) -> bool:
        return self.type == ComplexType.CLASS

    def isList(self) -> bool:
        return self.type == ComplexType.LIST

    def isDict(self) -> bool:
        return self.type == ComplexType.DICT

    def isListRoot(self) -> bool:
        return self.type == ComplexType.LIST_ROOT

    def isNullable(self) -> bool:
        return self.nullable

    def addChild(self, child):
        if self.isComplex():
            if child in self.children:
                childFound = self.children[self.children.index(child)]
                if not childFound.nullable and child.nullable:
                    childFound.nullable = True
            else:
                self.children.append(child)
        else:
            raise Exception("Cannot add child to simple type")

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.name == other.name and self.children == other.children

    def getType(self, withNullable=True) -> str:
        if self.isComplex():
            if self.isList():
                return self.addNullableAround(f"List[{self.getTypesOfChildren()}]", withNullable)
            elif self.isDict():
                return self.addNullableAround(f"Dict[{self.getTypesOfChildren()}]", withNullable)
            elif self.isClass():
                return self.addNullableAround(f"{self.name}", withNullable)
            elif self.isListRoot():
                return self.addNullableAround(f"List[{self.getTypesOfChildren()}]", withNullable)
        elif self.isSimple():
            return self.addNullableAround(f"{self.type.value}", withNullable)
        else:
            raise Exception("Unknown type_: " + str(type(self)))

    def addNullableAround(self, type_, withNullable=True) -> str:
        return f"Optional[{type_}]" if self.nullable and withNullable else type_

    def getTypesOfChildren(self) -> str:
        return self.addNullableAround(", ".join([child.getType(withNullable=False) for child in self.children]),
                                      self.hasNullableChildren())

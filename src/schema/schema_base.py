from abc import ABC, abstractmethod
from dataclasses import field
from typing import Optional, List, Any, Union

from src.schema.schema_type import SchemaType
from src.enums.type_enum import MyTypeBase, ComplexType, type_from_value, SimpleType


class SchemaBase(ABC):
    """
    This class is used to be the base class for all type_ of datas
    """

    root: "SchemaRoot"
    parent: Optional["SchemaBase"] = field(default_factory=lambda: None)
    type_: SchemaType
    name: str = ""
    path: str = ""
    nullable: bool = False
    datas: List[Any] = field(default_factory=list)

    def __init__(self, name: str, root: "SchemaRoot", parent: Optional["SchemaBase"] = None):
        """
        This method is used to initialize the class
        """
        self.name = name
        self.parent = parent
        self.root = root
        self.nullable = False
        self.datas = []
        self.type_ = SchemaType()

        if self.parent is not None and self.parent.type_ != ComplexType.LIST_ROOT:
            self.path = self.parent.path + "." + self.name
        elif self.parent is not None and self.parent.type_ == ComplexType.LIST_ROOT:
            self.path = self.name
        else:
            self.path = ""

    def __str__(self):
        return f" {self.name} : {self.type_} | {self.path}"

    def addData(self, data, complexType: ComplexType, simpleType: Optional[Union[ComplexType, str, SimpleType]] = None, simpleTypeNullable=False):
        """
        This method is used to add data to the class
        """

        if data is None:
            self.type_.nullable = True
        if complexType == ComplexType.DEFAULT and self.type_.type == ComplexType.:
            self.type_.addChild(SchemaType(type=complexType,children=[self.] ))

        else:
            self.type_.addSecondary(complexType, simpleType, simpleTypeNullable)

        elif isinstance(type_, ComplexType):
            self.type_.primary = type_
            if type_ == ComplexType.LIST_ROOT and secondaryClass != "":
                self.type_.secondary = [secondaryClass]
        else:
            self.type_.addSecondary(type_)
        self.datas.append(data)

    @abstractmethod
    def getSecondaryAttributes(self):
        for data in self.datas:
            if data is None:
                self.type_.nullable = True
            else:
                type_ = type_from_value(data)
                self.type_.addSecondary(type_)


    @abstractmethod
    def getType(self) -> SchemaType:
        return self.type_


    def __len__(self):
        return len(self.datas)

    def setNullable(self):
        #print(f"{self} is Nullable")
        self.nullable = True
        self.type_.nullable = True

    def needMapping(self):
        return isinstance(self.type_.primary, ComplexType) and self.type_.primary != ComplexType.LIST_ROOT

    @abstractmethod
    def scanRequired(self):
        pass

    def scanForClass(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    def scanForMappings(self):
        pass

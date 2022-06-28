from abc import ABC, abstractmethod
from dataclasses import field
from typing import Optional, List, Any

from src.schema.schema_type import SchemaType
from src.enums.type_enum import MyTypeBase, MyTypeWithMapping, type_from_value


class SchemaBase(ABC):
    """
    This class is used to be the base class for all type_ of datas
    """

    root: "SchemaRoot"
    parent: Optional["SchemaBase"] = field(default_factory=lambda: None)
    type_: Optional[MyTypeBase]
    type__: Optional["SchemaType"] = field(default_factory=lambda:None)
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
        self.type_ = None
        self.type__ = SchemaType()

        if self.parent is not None and self.parent.type_ != MyTypeWithMapping.LIST_ROOT:
            self.path = self.parent.path + "." + self.name
        elif self.parent is not None and self.parent.type_ == MyTypeWithMapping.LIST_ROOT:
            self.path = self.name
        else:
            self.path = ""

    def __str__(self):
        return f" {self.name} : {self.type__} | {self.path}"

    def addData(self, data, type_: MyTypeBase, secondaryClass:str=""):
        """
        This method is used to add data to the class
        """

        if data is None:
            self.type__.nullable = True
        elif isinstance(type_, MyTypeWithMapping):
            self.type__.primary = type_
            if type_ == MyTypeWithMapping.LIST_ROOT and secondaryClass != "":
                self.type__.secondary = [secondaryClass]
        else:
            self.type__.addSecondary(type_)
        self.datas.append(data)

    @abstractmethod
    def getSecondaryAttributes(self):
        for data in self.datas:
            if data is None:
                self.type__.nullable = True
            else:
                type_ = type_from_value(data)
                self.type__.addSecondary(type_)


    @abstractmethod
    def getType(self) -> SchemaType:
        return self.type__


    def __len__(self):
        return len(self.datas)

    def setNullable(self):
        print(f"{self} is Nullable")
        self.nullable = True
        self.type__.nullable = True

    def needMapping(self):
        return isinstance(self.type__.primary, MyTypeWithMapping) and self.type__.primary != MyTypeWithMapping.LIST_ROOT

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

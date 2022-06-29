from typing import Optional

from src.schema.schema_base import SchemaBase
from src.enums.type_enum import ComplexType
from src.utils.string_manipulation import getSubKey


class SchemaList(SchemaBase):
    """
    This class is used to be a class that represent a list
    """

    def getSecondaryAttributes(self):
        if self.child is not None:
            self.child.getSecondaryAttributes()
            for elem in self.datas:
                if elem is None:
                    self.type_.nullable = True
                    break
            self.type_.addSecondary(self.child.type_)


    child: Optional["SchemaBase"] = None

    def __init__(self, name: str, data, type_: ComplexType, root: "SchemaRoot",
                 parent: Optional["SchemaBase"] = None):
        super().__init__(name, root, parent)
        self.child = None
        self.addData(data, type_)

    def addData(self, data, type_: ComplexType):
        if data is None:
            self.setNullable()
        else:

            if ComplexType.DICT_LIST == self.type_.primary and isinstance(data, dict):
                data = list(data.values())
            super().addData(data, type_)
            subkey = getSubKey(self.name)
            for el in data:
                self.child = self.root.addSchemaOrData(subkey, el, self)

    def scanRequired(self):

        if self.child is not None:
            self.child.scanRequired()
            # self.nullable = self.type_.nullable

    def generate(self):
        if self.child:
            self.child.generate()

    def scanForClass(self):
        pass

    def getType(self):
        return self.type_

    def scanForMappings(self):
        if self.child:
            self.child.scanForMappings()

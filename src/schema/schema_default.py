from typing import Optional

from src.schema.schema_base import SchemaBase
from src.enums.type_enum import SimpleType


class SchemaDefault(SchemaBase):
    """
    This class is used to be the base class for all simple type_
    """

    def getSecondaryAttributes(self):
        super().getSecondaryAttributes()

    def generate(self):
        return

    def getType(self):
        return super().getType()

    def scanRequired(self):
        pass

    def __init__(self, name: str, data, type_: SimpleType, root: "SchemaRoot",
                 parent: Optional["SchemaBase"] = None):
        super().__init__(name, root, parent)
        self.addData(data, type_)

    def addData(self, data, type_: SimpleType):
        """
        This method is used to add data to the class
        """
        super().addData(data, type_)

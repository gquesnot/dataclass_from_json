from typing import Optional, Union

from src.classes.schema_base import SchemaBase
from src.dataclass.custom_type import CustomType


class SchemaDefault(SchemaBase):
    """
    This class is used to be the base class for all simple type_
    """

    def __init__(self, name: str, path, type_: "CustomType", root: "SchemaRoot",
                 parent: Optional[Union['SchemaDict', 'SchemaList', 'SchemaClass']] = None):
        super().__init__(name, path, type_, root, parent)

    def addData(self, data):
        """
        This method is used to add data to the class
        """
        if data is None:
            self.type.setNullable()
        else:
            super().addData(data)

    def scanForMappings(self):
        pass

    def generateClass(self):
        return

    def scanRequired(self):
        pass

from typing import Optional, Union

from src.classes.schema_base import SchemaBase
from src.utils.string_manipulation import getListDictSubKey


class SchemaList(SchemaBase):
    """
    This class is used to be a class that represent a list
    """

    child: Optional[Union['SchemaDefault', 'SchemaList', 'SchemaClass']] = None

    def __init__(self,
                 name: str,
                 path: str,
                 type_: "MyType",
                 root: "SchemaRoot",
                 parent: Optional[Union['SchemaDict',
                                        'SchemaList',
                                        'SchemaClass']] = None):
        super().__init__(name, path, type_, root, parent)
        self.child = None

    def addData(self, data):
        if data is None:
            self.type.setNullable()
        else:
            if self.type.isDictList() and isinstance(data, dict):
                data = list(data.values())
            super().addData(data)
            parentKey = self.name.replace('_list', '')
            subKey = getListDictSubKey(parentKey, self.parent.name)
            childNullable = self.type.hasChild() and self.type.child.nullable
            if self.type.hasClass():
                self.type.name = subKey
            for el in data:
                self.child = self.root.addSchemaOrData(
                    subKey, el, self, childNullable, forceChildClass=self.type.hasClass())

    def scanRequired(self):
        if self.child is not None:
            self.child.scanRequired()

    def generateClass(self):
        if self.child:
            self.child.generateClass()

    def scanForMappings(self):
        if self.child:
            self.child.scanForMappings()

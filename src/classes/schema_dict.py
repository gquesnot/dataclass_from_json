from typing import Optional, Union, Set

from src.classes.schema_base import SchemaBase
from src.utils.string_manipulation import getListDictSubKey


class SchemaDict(SchemaBase):
    child: Optional[Union['SchemaDefault', 'SchemaList', 'SchemaClass']] = None
    keys: Set[str]

    def __init__(self,
                 name: str,
                 path,
                 type_: "MyType",
                 root: "SchemaRoot",
                 parent: Optional[Union['SchemaDict',
                                        'SchemaList',
                                        'SchemaClass']] = None):
        super().__init__(name, path, type_, root, parent)
        self.child = None
        self.keys = set()

    def addData(self, data):
        super().addData(data)
        self.keys = self.keys | set(data.keys())
        parentKey = self.name.replace('_dict', '')
        subKey = getListDictSubKey(parentKey, self.parent.name)
        if self.type.hasClass():
            self.type.name = subKey
        for key, value in data.items():
            childNullable = self.type.hasChild() and self.type.child.nullable

            if self.type.isDictClass() or self.type.isDictList() or self.type.isDictSimple():
                self.child = self.root.addSchemaOrData(
                    subKey, value, self, childNullable, forceChildClass=self.type.hasClass())
            else:
                raise Exception("Not a dict type", self.type, self)

    def scanRequired(self):
        if self.child is not None:
            self.child.scanRequired()

    def scanForMappings(self):
        if self.child is not None:
            self.child.scanForMappings()

    def generateClass(self):
        if self.child is not None:
            self.child.generateClass()

from typing import Optional, Union, Set

from src.classes.schema_base import SchemaBase
from src.utils.string_manipulation import get_list_dict_sub_key


class SchemaDict(SchemaBase):
    child: Optional[Union["SchemaDefault", "SchemaList", "SchemaClass"]] = None
    keys: Set[str]

    def __init__(
            self,
            name: str,
            path,
            type_: "CustomType",
            root: "SchemaRoot",
            parent: Optional[Union["SchemaDict", "SchemaList", "SchemaClass"]] = None,
    ):
        super().__init__(name, path, type_, root, parent)
        self.child = None
        self.keys = set()

    def add_data(self, data):
        super().add_data(data)
        self.keys = self.keys | set(data.keys())
        parent_key = self.name.replace("_dict", "")
        sub_key = get_list_dict_sub_key(parent_key, self.parent.name)
        if self.type.has_class():
            self.type.name = sub_key
        for key, value in data.items():
            child_nullable = self.type.has_child() and self.type.child.nullable

            if (
                    self.type.is_dict_class()
                    or self.type.is_dict_list()
                    or self.type.is_dict_simple()
            ):
                self.child = self.root.add_schema_or_data(
                    sub_key,
                    value,
                    self,
                    child_nullable,
                    force_child_class=self.type.has_class(),
                )
            else:
                raise Exception("Not a dict type", self.type, self)

    def scan_required(self):
        if self.child is not None:
            self.child.scan_required()

    def scan_for_mappings(self):
        if self.child is not None:
            self.child.scan_for_mappings()

    def generate_class(self):
        if self.child is not None:
            self.child.generate_class()

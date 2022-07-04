from typing import Optional, Union

from src.classes.schema_base import SchemaBase
from src.utils.string_manipulation import get_list_dict_sub_key


class SchemaList(SchemaBase):
    """
    This class is used to be a class that represent a list
    """

    child: Optional[Union["SchemaDefault", "SchemaList", "SchemaClass"]] = None

    def __init__(
            self,
            name: str,
            path: str,
            type_: "CustomType",
            root: "SchemaRoot",
            parent: Optional[Union["SchemaDict", "SchemaList", "SchemaClass"]] = None,
    ):
        super().__init__(name, path, type_, root, parent)
        self.child = None

    def add_data(self, data):
        if data is None:
            self.type.set_nullable()
        else:
            if self.type.is_dict_class() and isinstance(data, dict):
                data = list(data.values())
            super().add_data(data)
            parent_key = self.name.replace("_list", "")
            sub_key = get_list_dict_sub_key(parent_key, self.parent.name)
            child_nullable = self.type.has_child() and self.type.child.nullable
            if self.type.has_class():
                self.type.name = sub_key
            for el in data:
                self.child = self.root.add_schema_or_data(
                    sub_key,
                    el,
                    self,
                    child_nullable,
                    force_child_class=self.type.has_class(),
                )

    def scan_required(self):
        if self.child is not None:
            self.child.scan_required()

    def generate_class(self):
        if self.child:
            self.child.generate_class()

    def scan_for_mappings(self):
        if self.child:
            self.child.scan_for_mappings()

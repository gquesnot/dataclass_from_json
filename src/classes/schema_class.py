from copy import copy
from typing import Dict, Set, List, Optional, Union

from src.dataclass.schema_mapping_matching import SchemaMappingMatching, SchemaMatching
from src.dataclass.custom_type import CustomType
from src.classes.schema_base import SchemaBase
from src.classes.schema_dict import SchemaDict
from src.classes.schema_list import SchemaList

from src.utils.handle_path import multiple_path_joins, create_dir
from src.utils.string_manipulation import (
    to_class_style,
    get_sub_key,
    key_is_a_valid_attribute,
    snake_case,
)


class SchemaClass(SchemaBase):
    """
    This class is used to be a class that represent a dict
    """

    def get_signature(self):
        return set(self.properties.keys())

    required: Set[str]
    imports: Dict[str, List[str]]
    mappings: Dict[str, SchemaMappingMatching]
    properties: Dict[str, Union["SchemaClass", "SchemaList", "SchemaDefault"]]

    def __init__(
            self,
            name: str,
            path: str,
            data,
            type_: "CustomType",
            root: "SchemaRoot",
            parent: Optional[Union["SchemaDict", "SchemaList", "SchemaClass"]] = None,
    ):

        self.mappings = dict()
        self.properties = dict()
        self.required = set()
        self.imports = dict()
        super().__init__(name, path, type_, root, parent)
        if self.parent is None and self.type.is_list_root():
            data = {name: data}
            sub_key = get_sub_key(name)
            self.type.name = to_class_style(sub_key)
        if self.parent is None:
            self.add_data(data)

    def add_import(self, k, v):
        if k not in self.imports:
            self.imports[k] = []
        self.imports[k].append(v)

    def add_data(self, data):
        if data is None:
            self.type.set_nullable()
        else:
            super().add_data(data)
            for k, v in data.items():
                new_key = k if key_is_a_valid_attribute(k) else f"_{k}"
                if new_key != k:
                    self.add_matching(k, new_key)
                new_schema = self.root.add_schema_or_data(new_key, v, self)
                self.properties[new_key] = new_schema

    def add_matching(self, key, new_key, root_list_not_class=False, nullable=False):
        if key not in self.mappings:
            self.mappings[new_key] = SchemaMappingMatching(
                key=new_key,
                type=CustomType(nullable=True),
                matching=SchemaMatching(from_=key, root_list_not_class=root_list_not_class),
            )
        else:
            self.mappings[new_key].matching.from_ = key
            self.mappings[new_key].matching.root_list_not_class = root_list_not_class

    def scan_required(self):
        base_len = len(self.datas)
        for k, v in self.properties.items():
            if v is None:
                continue
            elif len(v.datas) == base_len:
                self.required.add(k)
            else:
                v.type.set_nullable()
        for k, v in self.properties.items():
            if v is None:
                continue
            v.scan_required()

    def scan_for_mappings(self):
        for k, v in self.properties.items():
            if v is None:
                continue
            new_mapping = SchemaMappingMatching(key=k)
            if v.type.has_class() and not self.type.is_list_root():
                class_name = to_class_style(v.type.name)
                new_mapping.type = v.type
                new_mapping.mapping.className = class_name
                self.add_import(self.get_import_string(self.get_ini_file_path(), True) + f".{snake_case(class_name)}", class_name)
                self.mappings[k] = new_mapping
                v.scan_for_mappings()
            elif self.type.is_list_root():
                self.type.child = v.child.type
                new_mapping.matching.root_list_not_class = not self.type.has_class()
                new_mapping.type = self.type
                self.mappings[k] = new_mapping
                if self.type.has_class() and v.child.type.is_class():
                    self.add_import(
                        self.get_import_string(self.get_ini_file_path(), False, False)+f".{snake_case(v.child.type.name)}", to_class_style(v.child.type.name)
                    )
                    new_mapping.mapping.className = to_class_style(v.child.name)
                    v.scan_for_mappings()

    def dtc_to_string(self):
        blue_print = self.get_blue_print()
        attributes = []
        for k, v in self.properties.items():
            if v is None:
                attr_type = "Any"
                default_value = "None"
            else:
                attr_type = v.type.to_string()
                default_value = v.type.get_default_with_field()
            attribute = f"{' ' * 4}{k}: {attr_type} = {default_value}"
            if attr_type is not None:
                attributes.append(attribute)
            else:
                raise ("*** ATTRIBUTE ERROR", k, v)
        blue_print["attributes"] = "\n".join(attributes)
        if len(self.imports) > 0:
            blue_print["imports"] = (
                    "\n".join(
                        [
                            f"from {k} import "
                            + ", ".join([str(v) for v in imports])
                            for k, imports in self.imports.items()
                        ]
                    )
                    + "\n"
            )
        if len(self.mappings) > 0:
            from_mapping = [
                value
                for value in [v.from_dict_str() for k, v in self.mappings.items()]
                if value != ""
            ]
            to_mapping = [
                value
                for value in [v.to_dict_str() for k, v in self.mappings.items()]
                if value != ""
            ]
            if len(from_mapping) > 0:
                blue_print["from_dict_mapping"] = "\n" + "\n".join(from_mapping)
        return copy(self.root.template).format(**blue_print)

    def get_base_file_path(self):
        return [self.root.dtc_path, snake_case(self.root.name)]

    def get_ini_file_path(self) -> list:
        after = [self.root.dtc_path, snake_case(self.root.name)]
        if not self.parent:
            return after
        result = []
        parent = self.parent
        while parent:
            if parent.type.is_class():
                result.append(f"{snake_case(parent.name)}_")
            parent = parent.parent
        after.reverse()
        result.extend(after)
        result.reverse()
        return result

    def get_import_string(self, paths,with_name=False, _after=True):
        return ".".join(paths + ([snake_case(self.name)+ ("_" if _after else '')] if with_name else []))

    def generate_class(self):
        if self.type.has_class():
            dataclass_str = self.dtc_to_string()
            final_path = self.get_ini_file_path()
            create_dir(final_path)
            final_path.append(f"{snake_case(self.name)}.py")
            print(f"Writing {final_path}")
            with open(
                    multiple_path_joins(final_path),
                    "w",
            ) as f:
                f.write(dataclass_str)
            for k, v in self.properties.items():
                if v is None:
                    continue
                if v.type.has_class():
                    v.generate_class()

    def get_blue_print(self) -> Dict[str, str]:
        return {
            "json_path": self.root.dtc_path,
            "imports": "",
            "className": to_class_style(self.name),
            "attributes": "",
            "to_dict_mapping": "",
            "from_dict_mapping": "",
            "variant": "",
        }

    def __str__(self):
        return super().__str__()

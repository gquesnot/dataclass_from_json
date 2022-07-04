import json
import os
import shutil
from typing import Optional, Dict, Any

from src.dataclass.custom_type import CustomType
from src.enums.simple_type import SimpleType
from src.enums.complex_type import ComplexType
from src.classes.schema_default import SchemaDefault
from src.classes.schema_class import SchemaClass
from src.classes.schema_dict import SchemaDict
from src.classes.schema_list import SchemaList
from src.utils.handle_path import multiple_path_joins
from src.utils.string_manipulation import snake_case, to_class_style, remove_extension


class SchemaRoot:
    root: Optional[SchemaClass] = None

    modules: Dict[str, Any] = {}
    children: Dict[str, Any] = dict()
    imports: Dict[str, Any] = dict()
    name: str
    class_template: str
    enum_template = str
    template_path: str
    dtc_path: str = "dataclass"
    json_path: str = "jsons"

    def __init__(
            self, json_path="jsons", dtc_path="dataclass"
    ):
        self.class_template = ""
        self.enum_template = ""
        self.json_path = json_path
        self.dtc_path = dtc_path
        self.template_path = multiple_path_joins(["src", "templates"])
        self.get_templates()
        self.copy_base_data_class()
        self.copy_base_enum()

    def get_templates(self):
        with open(multiple_path_joins([self.template_path, "class_template.py"]), "r") as f:
            self.class_template = f.read()
        with open(multiple_path_joins([self.template_path, "enum_template.py"]), "r") as f:
            self.enum_template = f.read()

    def copy_base_enum(self):
        template_base_enum_path = multiple_path_joins(
            [self.template_path, "base_enum.py"]
        )
        dest_base_enum_path = multiple_path_joins([self.dtc_path, "base_enum.py"])
        shutil.copyfile(template_base_enum_path, dest_base_enum_path)

    def copy_base_data_class(self):
        template_base_data_class_path = multiple_path_joins(
            [self.template_path, "base_dataclass.py"]
        )
        dest_base_data_class_path = multiple_path_joins([self.dtc_path, "base_dataclass.py"])
        shutil.copyfile(template_base_data_class_path, dest_base_data_class_path)

    def reset(self):
        self.root = None
        self.children = dict()
        self.imports = dict()

    def generate(self, name):
        self.reset()
        self.name = name
        data = self.get_data()
        self.clear_dest_directory()
        if isinstance(data, dict):
            type_ = CustomType(simple=SimpleType.DICT, complex=ComplexType.CLASS)
        else:
            type_ = CustomType(simple=SimpleType.LIST, complex=ComplexType.LIST_ROOT)
        self.root = SchemaClass(self.name, self.name, data, type_, self, None)
        self.root.scan_required()
        self.root.scan_for_mappings()
        self.root.generate_class()
        self.generate_init_file()

    def get_data(self):
        with open(multiple_path_joins([self.json_path, self.name + ".json"]), "r") as f:
            data = json.load(f)
        return data

    @staticmethod
    def clear_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def clear_dest_directory(self):
        self.clear_dir(multiple_path_joins([self.dtc_path, snake_case(self.name)]))

    def get_path(self, parent, name):
        return parent.path + "." + name if parent is not None else name

    def get_child_or_new_child(
            self, name: str, type_: CustomType, data: Any, parent, force_nullable=False
    ):
        if type_.is_complex() and not type_.is_class():
            if type_.is_list():
                name = f"{name}_list"
            elif type_.is_dict():
                name = f"{name}_dict"
        path = self.get_path(parent, name)
        if not force_nullable:
            force_nullable = path in self.children and self.children[path] is None
        if path in self.children and not force_nullable:

            child = self.children[path]
            child.type += type_
        elif not type_.is_none():
            if force_nullable:
                type_.set_nullable()
            if type_.is_simple():
                child = SchemaDefault(name, path, type_, self, parent)
            elif type_.is_list():
                child = SchemaList(name, path, type_, self, parent)
            elif type_.is_dict():
                child = SchemaDict(name, path, type_, self, parent)
            elif type_.is_class():
                child = SchemaClass(name, path, data, type_, self, parent)
            else:
                raise Exception(f"Unknown type: {type_}")
            # print(child)
            self.children[path] = child
        else:
            return None
        child.add_data(data)
        return child

    def add_schema_or_data(
            self, name, data, parent=None, force_nullable=False, force_child_class=False
    ):
        if force_child_class:
            type_ = CustomType(
                simple=SimpleType.DICT, complex=ComplexType.CLASS, name=name
            )
        else:
            type_ = CustomType.from_data(name, data)

        return self.get_child_or_new_child(name, type_, data, parent, force_nullable)

    # dynamic loading
    def load_from_json(self, name, print_schema=False):
        with open(multiple_path_joins([self.json_path, name + ".json"]), "r") as f:
            data = json.load(f)
        self.load(name)
        return self.get(name, data, print_schema=print_schema)

    def load(self, name):
        if name not in self.modules:
            self.modules[name] = dict()
            path = multiple_path_joins([self.dtc_path, snake_case(name)])
            files = os.listdir(path)

            classes_name = [
                to_class_style(remove_extension(file))
                for file in files
                if not file.startswith("__")
            ]
            if len(classes_name) == 0:
                raise Exception(
                    f"Generate the Dataclass before , No One Found in {path}"
                )
            self.modules[name] = __import__(
                f"{self.dtc_path}.{snake_case(name)}", fromlist=classes_name
            )

    def get(self, name, datas, print_schema=False):
        if name not in self.modules:
            self.load(name)
        _class = getattr(self.modules[name], to_class_style(name))
        if print_schema:
            print(_class.schema_json(indent=2))
        return _class().from_dict(datas)

    def generate_init_file(self):
        for k, child in self.children.items():
            if child.type.is_class():
                self.imports[child.get_import_string(child.get_ini_file_path(), True, False)] = child.name
        self.imports[self.root.get_import_string(self.root.get_ini_file_path(), True, False)] = self.root.name
        with open(
                multiple_path_joins([self.dtc_path, snake_case(self.name), "__init__.py"]), "w"
        ) as f:
            f.write(
                "\n".join(
                    [
                        f"from {path} import {to_class_style(import_)}"
                        for path, import_ in self.imports.items()
                    ]
                )
                + "\n"
            )

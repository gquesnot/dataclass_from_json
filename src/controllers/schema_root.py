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
from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import snakeCase, toClassStyle, removeExtension


class SchemaRoot:
    root: Optional[SchemaClass] = None

    modules: Dict[str, Any] = {}
    children: Dict[str, Any] = dict()
    imports: Dict[str, Any] = dict()
    name: str
    template: str
    dtc_path: str = "dataclass"
    json_path: str = "jsons"
    template_path: str = "src\\templates"

    def __init__(
            self,
            json_path="jsons",
            dtc_path="dataclass",
            template_path="src/templates"):
        self.template = ""
        self.json_path = json_path
        self.dtc_path = dtc_path
        self.template_path = template_path
        self.getTemplate()
        self.copyBaseDataClass()

    def getTemplate(self):
        with open(multiplePathJoins([self.template_path, "template.py"]), "r") as f:
            self.template = f.read()

    def copyBaseDataClass(self):
        templateBaseDataClassPath = multiplePathJoins(
            [self.template_path, "base_dataclass.py"])
        destBaseDataClassPath = multiplePathJoins(
            [self.dtc_path, "base_dataclass.py"])
        shutil.copyfile(templateBaseDataClassPath, destBaseDataClassPath)

    def reset(self):
        self.root = None
        self.children = dict()
        self.imports = dict()

    def generate(self, name):
        self.reset()
        self.name = name
        data = self.getData()
        self.clearDestDirectory()
        if isinstance(data, dict):
            type_ = CustomType(simple=SimpleType.DICT,
                               complex=ComplexType.CLASS)
        else:
            type_ = CustomType(simple=SimpleType.LIST,
                               complex=ComplexType.LIST_ROOT)
        self.root = SchemaClass(self.name, self.name, data, type_, self, None)
        self.root.scanRequired()
        self.root.scanForMappings()
        self.root.generateClass()
        self.generateInitFile()

    def getData(self):
        with open(multiplePathJoins([self.json_path, self.name + ".json"]), 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def clearDir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def clearDestDirectory(self):
        self.clearDir(multiplePathJoins([self.dtc_path, snakeCase(self.name)]))

    def getPath(self, parent, name):
        return parent.path + "." + name if parent is not None else name

    def getChildOrNewChild(
            self,
            name: str,
            type_: CustomType,
            data: Any,
            parent,
            forceNullable=False):
        if type_.isComplex() and not type_.isClass():
            if type_.isList():
                name = f"{name}_list"
            elif type_.isDict():
                name = f"{name}_dict"
        path = self.getPath(parent, name)
        if not forceNullable:
            forceNullable = path in self.children and self.children[path] is None
        if path in self.children and not forceNullable:

            child = self.children[path]
            child.type += type_
        elif not type_.isNone():
            if forceNullable:
                type_.setNullable()
            if type_.isSimple():
                child = SchemaDefault(name, path, type_, self, parent)
            elif type_.isList():
                child = SchemaList(name, path, type_, self, parent)
            elif type_.isDict():
                child = SchemaDict(name, path, type_, self, parent)
            elif type_.isClass():
                child = SchemaClass(name, path, data, type_, self, parent)
            else:
                raise Exception(f"Unknown type: {type_}")
            # print(child)
            self.children[path] = child
        else:
            return None
        child.addData(data)
        return child

    def addSchemaOrData(
            self,
            name,
            data,
            parent=None,
            forceNullable=False,
            forceChildClass=False):
        if forceChildClass:
            type_ = CustomType(simple=SimpleType.DICT,
                               complex=ComplexType.CLASS, name=name)
        else:
            type_ = CustomType.from_data(name, data)

        return self.getChildOrNewChild(
            name, type_, data, parent, forceNullable)

    # dynamic loading
    def loadFromJson(self, name):
        with open(multiplePathJoins([self.json_path, name + ".json"]), 'r') as f:
            data = json.load(f)
        self.load(name)
        return self.get(name, data)

    def load(self, name):
        if name not in self.modules:
            self.modules[name] = dict()
            path = multiplePathJoins([self.dtc_path, snakeCase(name)])
            files = os.listdir(path)

            classesName = [toClassStyle(removeExtension(file))
                           for file in files if not file.startswith("__")]
            if len(classesName) == 0:
                raise Exception(
                    f"Generate the Dataclass before , No One Found in {path}")
            self.modules[name] = __import__(
                f"{self.dtc_path}.{snakeCase(name)}",
                fromlist=classesName)

    def get(self, name, datas):
        if name not in self.modules:
            self.load(name)
        _class = getattr(self.modules[name], toClassStyle(name))
        return _class().from_dict(datas)

    def generateInitFile(self):
        for k, child in self.children.items():
            if child.type.isClass():
                self.imports[child.name] = child.name
        self.imports[self.root.name] = self.root.name
        with open(multiplePathJoins([self.dtc_path, snakeCase(self.name), "__init__.py"]), "w") as f:
            f.write(
                "\n".join(
                    [f"from {self.dtc_path}.{snakeCase(self.name)}.{snakeCase(import_)} import {toClassStyle(import_)}"
                     for import_ in
                     self.imports]) + "\n")

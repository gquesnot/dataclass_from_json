import json
import os
import shutil
from typing import Optional

from src.enums.type_enum import ComplexType, type_from_value
from src.schema.schema_base import SchemaBase
from src.schema.schema_default import SchemaDefault
from src.schema.schema_dict import SchemaDict
from src.schema.schema_list import SchemaList
from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import snakeCase


class SchemaRoot:
    root: Optional[SchemaBase] = None
    children: dict = dict()
    name: str
    template: str
    dtc_path: str = "dataclass"
    json_path: str = "jsons"
    template_path: str = "src\\templates"

    def __init__(self, json_path="jsons", dtc_path="dataclass", template_path="src/templates"):
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
        templateBaseDataClassPath = multiplePathJoins([self.template_path, "base_dataclass.py"])
        destBaseDataClassPath = multiplePathJoins([self.dtc_path, "base_dataclass.py"])
        shutil.copyfile(templateBaseDataClassPath, destBaseDataClassPath)

    def reset(self):
        self.root = None
        self.children = dict()

    def generate(self, name):
        self.reset()

        self.name = name
        data = self.getData()
        self.clearDestDirectory()
        self.handlePathInit()
        type_ = ComplexType.DICT if isinstance(data, dict) else ComplexType.LIST_ROOT
        self.root = SchemaDict(self.name, data, type_, self, None)
        self.root.scanRequired()
        self.root.getSecondaryAttributes()
        self.root.scanForMappings()
        self.root.generate()

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


    def addSchemaOrData(self, name, data, parent):
        if parent is None:
            path = name
        else:
            path = parent.path + "." + name
        type_ = type_from_value(data)
        if path in self.children:
            self.children[path].addData(data, type_)
        else:
            if type_ == ComplexType.DICT:
                self.children[path] = SchemaDict(name, data, type_, self, parent)
            elif type_ == ComplexType.CLASS:
                self.children[path] = SchemaDict(name, data, type_, self, parent)
            elif type_ == ComplexType.LIST:
                self.children[path] = SchemaList(name, data, type_, self, parent)
            elif type_ == ComplexType.DICT_LIST:
                data = list(data.values())
                self.children[path] = SchemaList(name, data, type_, self, parent)
            else:
                self.children[path] = SchemaDefault(name, data, type_, self, parent)
        return self.children[path]

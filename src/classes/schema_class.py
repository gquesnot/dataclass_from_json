from copy import copy
from typing import Dict, Set, List, Optional, Union

from src.dataclass.schema_mapping_matching import SchemaMappingMatching, SchemaMatching
from src.dataclass.custom_type import CustomType
from src.classes.schema_base import SchemaBase
from src.classes.schema_dict import SchemaDict
from src.classes.schema_list import SchemaList

from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import toClassStyle, getSubKey, keyIsAValidAttribute, snakeCase


class SchemaClass(SchemaBase):
    """
    This class is used to be a class that represent a dict
    """

    def getSignature(self):
        return set(self.properties.keys())

    required: Set[str]
    imports: Dict[str, List[str]]
    mappings: Dict[str, SchemaMappingMatching]
    properties: Dict[str, Union["SchemaClass", "SchemaList", "SchemaDefault"]]

    def __init__(self,
                 name: str,
                 path: str,
                 data,
                 type_: "CustomType",
                 root: "SchemaRoot",
                 parent: Optional[Union['SchemaDict',
                                        'SchemaList',
                                        'SchemaClass']] = None):

        self.mappings = dict()
        self.properties = dict()
        self.required = set()
        self.imports = dict()
        super().__init__(name, path, type_, root, parent)
        if self.parent is None and self.type.isListRoot():
            data = {name: data}
            subKey = getSubKey(name)
            self.type.name = toClassStyle(subKey)
        if self.parent is None:
            self.addData(data)

    def addImport(self, k, v):
        if k not in self.imports:
            self.imports[k] = []
        self.imports[k].append(v)

    def addData(self, data):
        if data is None:
            self.type.setNullable()
        else:
            super().addData(data)
            for k, v in data.items():
                newKey = k if keyIsAValidAttribute(k) else f"_{k}"
                if newKey != k:
                    self.addMatching(k, newKey)
                newSchema = self.root.addSchemaOrData(newKey, v, self)
                self.properties[newKey] = newSchema

    def addMatching(self, key, newKey, rootListNotClass=False, nullable=False):
        if key not in self.mappings:
            self.mappings[newKey] = SchemaMappingMatching(
                key=newKey, type=CustomType(
                    nullable=True), matching=SchemaMatching(
                    from_=key, rootListNotClass=rootListNotClass))
        else:
            self.mappings[newKey].matching.from_ = key
            self.mappings[newKey].matching.rootListNotClass = rootListNotClass

    def scanRequired(self):
        baseLen = len(self.datas)
        for k, v in self.properties.items():
            if v is None:
                continue
            elif len(v.datas) == baseLen:
                self.required.add(k)
            else:
                v.type.setNullable()
        for k, v in self.properties.items():
            if v is None:
                continue
            v.scanRequired()

    def scanForMappings(self):
        for k, v in self.properties.items():
            if v is None:
                continue
            newMapping = SchemaMappingMatching(key=k)
            if v.type.hasClass() and not self.type.isListRoot():
                className = toClassStyle(v.type.name)
                newMapping.type = v.type
                newMapping.mapping.className = className
                self.addImport(snakeCase(v.type.name), className)
                self.mappings[k] = newMapping
                v.scanForMappings()
            elif self.type.isListRoot():
                self.type.child = v.child.type
                newMapping.matching.rootListNotClass = not self.type.hasClass()
                newMapping.type = self.type
                self.mappings[k] = newMapping
                if self.type.hasClass() and v.child.type.isClass():
                    self.addImport(snakeCase(v.child.type.name),
                                   toClassStyle(v.child.type.name))
                    newMapping.mapping.className = toClassStyle(v.child.name)
                    v.scanForMappings()

    def dtcToString(self):
        bluePrint = self.getBluePrint()
        attributes = []
        for k, v in self.properties.items():
            if v is None:
                attrType = "Any"
                defaultValue = "None"
            else:
                attrType = v.type.toString()
                defaultValue = v.type.getDefaultWithField()
            attribute = f"{' ' * 4}{k}: {attrType} = {defaultValue}"
            if attrType is not None:
                attributes.append(attribute)
            else:
                raise ('*** ATTRIBUTE ERROR', k, v)
        bluePrint['attributes'] = "\n".join(attributes)
        if len(self.imports) > 0:
            bluePrint['imports'] = "\n".join([
                f"from {self.root.dtc_path}.{snakeCase(self.root.name)}.{snakeCase(k)} import " + ", ".join(
                    [str(v) for v in imports])
                for k, imports in self.imports.items()
            ]) + "\n"
        if len(self.mappings) > 0:
            fromMapping = [
                value for value in [
                    v.from_dict_str() for k,
                    v in self.mappings.items()] if value != ""]
            toMapping = [
                value for value in [
                    v.to_dict_str() for k,
                    v in self.mappings.items()] if value != ""]
            if len(fromMapping) > 0:
                bluePrint["from_dict_mapping"] = "\n" + "\n".join(fromMapping)
            # if len(toMapping) > 0:
            #    bluePrint["to_dict_mapping"] = "\n" + "\n".join(toMapping)
        return copy(self.root.template).format(**bluePrint)

    def generateClass(self):
        if self.type.hasClass():
            dataclassStr = self.dtcToString()
            with open(multiplePathJoins([self.root.dtc_path, snakeCase(self.root.name), f"{snakeCase(self.name)}.py"]),
                      'w') as f:
                f.write(dataclassStr)
            for k, v in self.properties.items():
                if v is None:
                    continue
                if v.type.hasClass():
                    v.generateClass()

    def getBluePrint(self) -> Dict[str, str]:
        return {
            "json_path": self.root.dtc_path,
            "imports": "",
            "className": toClassStyle(self.name),
            "attributes": "",
            "to_dict_mapping": "",
            "from_dict_mapping": "",
            "variant": "",
        }

    def __str__(self):
        return super().__str__()

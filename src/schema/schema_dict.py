from copy import copy
from typing import Dict, Set, List, Optional

from src.dataclass.level_mapping import SchemaMappingMatching, SchemaMapping, SchemaMatching
from src.enums.type_enum import MyTypeWithMapping, get_default_value
from src.schema.schema_base import SchemaBase
from src.schema.schema_list import SchemaList
from src.schema.schema_type import SchemaType
from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import toClassStyle, getSubKey, keyIsAValidAttribute, camelCase, snakeCase


class SchemaDict(SchemaBase):
    """
    This class is used to be a class that represent a dict
    """

    def getSecondaryAttributes(self):
        for k, v in self.properties.items():
            v.getSecondaryAttributes()

        if self.type__.primary == MyTypeWithMapping.CLASS:
            self.type__.addSecondary(toClassStyle(self.name))
        elif self.type__.primary == MyTypeWithMapping.DICT:
            for k, v in self.properties.items():
                self.type__.addSecondary(v.type__)

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

    required: Set[str]

    imports: Dict[str, List[str]]
    mappings: Dict[str, SchemaMappingMatching]
    properties: Dict[str, "SchemaBase"]

    def __init__(self, name: str, data, type_: MyTypeWithMapping, root: "SchemaRoot",
                 parent: Optional["SchemaBase"] = None):
        super().__init__(name, root, parent)
        self.mappings = dict()
        self.properties = dict()
        self.required = set()
        self.imports = dict()
        if self.parent is None and type_ == MyTypeWithMapping.LIST_ROOT:
            data = {name: data}
            subKey = getSubKey(name)
            self.mappings[subKey] = SchemaMappingMatching(key=name,
                                                          mapping=SchemaMapping(className=toClassStyle(subKey),
                                                                                type_=type_))
            self.imports[subKey] = [toClassStyle(subKey)]
        self.addData(data, type_, secondaryClass=toClassStyle(getSubKey(name)))

    def addImport(self, k, v):
        if k not in self.imports:
            self.imports[k] = []
        self.imports[k].append(v)

    def addData(self, data, type_: MyTypeWithMapping, secondaryClass: str = ""):
        if data is None:
            self.setNullable()
        else:
            super().addData(data, type_, secondaryClass)
            for k, v in data.items():
                newKey = k if keyIsAValidAttribute(k) else f"{k}_"
                if newKey != k and self.type__.primary != MyTypeWithMapping.LIST_ROOT:
                    self.addMatching(k, newKey)
                self.properties[k] = self.root.addSchemaOrData(newKey, v, self)

    def scanRequired(self):
        baseLen = len(self)
        for k, v in self.properties.items():
            #    print(self, k, baseLen, len(v))
            if len(v) == baseLen:
                self.required.add(k)
            else:
                v.setNullable()
        # print('_____')
        for k, v in self.properties.items():
            v.scanRequired()

    def addNullableToAttributeStr(self, attribute, nullable):
        return attribute if not nullable else f"Optional[{attribute}]"

    def getAttributeAsStr(self, k, attribute: "SchemaBase"):
        before = ' ' * 4
        if isinstance(attribute.type__.primary, MyTypeWithMapping):

            if attribute.type__.hasClass():
                if attribute.type__.primary == MyTypeWithMapping.CLASS or attribute.type__.primary == MyTypeWithMapping.LIST_ROOT:
                    className = attribute.type__.secondary[0]
                elif isinstance(attribute.type__.secondary[0], str):
                    className = attribute.type__.secondary[0]
                else:
                    className = attribute.type__.secondary[0].secondary[0]
                if attribute.type__.primary == MyTypeWithMapping.CLASS:
                    return f"{before}{attribute.name}: {self.addNullableToAttributeStr(className, attribute.type__.nullable)}" \
                           f" = Field(default_factory={className})"
                elif attribute.type__.primary == MyTypeWithMapping.LIST_ROOT:
                    return f"{before}{attribute.name}: List[{self.addNullableToAttributeStr(className, attribute.type__.nullable)}]" \
                           f" = Field(default_factory=list)"
                elif isinstance(attribute.type__.secondary[0], str):
                    return self.getDictListAttributeStr(className, attribute, before)
            else:
                className = attribute.type__.secondary[0].value
                return self.getDictListAttributeStr(className, attribute, before)
        else:
            return f"{before}{attribute.name}: {self.addNullableToAttributeStr(attribute.type__.secondary[0].value, attribute.type__.nullable)}" \
                   f" = {get_default_value(attribute.type__.secondary[0], attribute.type__.nullable)}"

    def getDictListAttributeStr(self, className, attribute,before):
        if attribute.type__.primary == MyTypeWithMapping.LIST:
            return f"{before}{attribute.name}: {self.addNullableToAttributeStr('List[' + self.addNullableToAttributeStr(className, attribute.type__.secondaryNullable()) + ']', attribute.type__.nullable)}" \
                           f" = Field(default_factory=list)"
        else:
            f"{before}{attribute.name}: {self.addNullableToAttributeStr('Dict[str, ' + self.addNullableToAttributeStr(className, attribute.type__.secondaryNullable()) + ']', attribute.type__.nullable)}" \
            f" = Field(default_factory=dict)"

    def scanForMappings(self):
        for k, v in self.properties.items():
            if self.parent is None and self.type__.primary == MyTypeWithMapping.LIST_ROOT:
                v.scanForMappings()
            else:
                if isinstance(v, SchemaDict):
                    self.addMapping(k, v)
                    v.scanForMappings()
                elif isinstance(v, SchemaList):
                    self.addMapping(k, v)
                    v.scanForMappings()
                # if len(self.mappings) > 0:
                #     print(self)
                #     for k, v in self.mappings.items():
                #         print(k, v)
                #     for k, v in self.imports.items():
                #         print('import', k, v)
                #     print('_____')

    def addMatching(self, key, newKey):
        if newKey not in self.mappings:
            self.mappings[newKey] = SchemaMappingMatching(key=newKey, matching=SchemaMatching(from_=key))
        else:
            self.mappings[newKey].matching.from_ = key

    def addMapping(self, k, v):
        type_ = v.getType()
        if type_.primary == MyTypeWithMapping.CLASS or isinstance(type_.primary, MyTypeWithMapping):
            if type_.hasClass():
                if type_.primary == MyTypeWithMapping.CLASS:
                    className = type_.secondary[0]
                    self.addImport(camelCase(className), className)
                else:
                    secondary = type_.secondary[0]
                    if isinstance(secondary[0], SchemaType):
                        className = secondary[0].secondary[0]
                    else:
                        className = type_.secondary[0]
                    self.addImport(camelCase(className), className)

                if v.name in self.mappings and self.mappings[v.name].hasMapping():
                    print(f"{v.name} already exists in {self}")
                if k in self.mappings:
                    self.mappings[v.name].mapping.className = className
                    self.mappings[v.name].mapping.type_ = type_.primary
                    self.mappings[v.name].nullable = type_.nullable
                else:
                    self.mappings[v.name] = SchemaMappingMatching(key=v.name,
                                                                  mapping=SchemaMapping(type_=type_.primary,
                                                                                        className=className),
                                                                  nullable=type_.nullable)

    def getType(self):
        return self.type__
        # if self.type_ == MyTypeWithMapping.CLASS:
        #     result = [MyTypeWithMapping.CLASS, [toClassStyle(self.name)]]
        # else:
        #     tmp = set()
        #     for k, v in self.properties.items():
        #         tmp.add(v.getType())
        #     result = [self.type_, [list(tmp)]]
        # if self.nullable:
        #     result[1].append(MyTypeDefault.NONE)
        # return result

    def dtcToString(self):
        bluePrint = self.getBluePrint()
        bluePrint['attributes'] = "\n".join([
            self.getAttributeAsStr(k, attribute)
            for k, attribute in self.properties.items()
        ])

        if len(self.imports) > 0:
            bluePrint['imports'] = "\n".join([
                f"from {self.root.dtc_path}.{snakeCase(self.root.name)}.{snakeCase(k)} import " + ", ".join(
                    [str(v) for v in imports])
                for k, imports in self.imports.items()
            ]) + "\n"
        if len(self.mappings) > 0:
            for k, v in self.mappings.items():
                if isinstance(v, dict):
                    print(self, k, v)
            fromMapping = [value for value in [v.from_dict_str() for k, v in self.mappings.items()] if value != ""]
            toMapping = [value for value in [v.to_dict_str() for k, v in self.mappings.items()] if value != ""]
            if len(fromMapping) > 0:
                bluePrint["from_dict_mapping"] = "\n" + "\n".join(fromMapping)
            if len(toMapping) > 0:
                bluePrint["to_dict_mapping"] = "\n" + "\n".join(toMapping)

        return copy(self.root.template).format(**bluePrint)

    def generate(self):

        if self.type__.hasClass():
            dataclassStr = self.dtcToString()
            with open(multiplePathJoins([self.root.dtc_path, snakeCase(self.root.name), f"{snakeCase(self.name)}.py"]),
                      'w') as f:
                f.write(dataclassStr)
            for k, v in self.properties.items():
                if isinstance(v.type__.primary, MyTypeWithMapping):
                    v.generate()

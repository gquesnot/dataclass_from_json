import re
from copy import copy
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from src.dataclass.level_mapping import SchemaMapping
from src.dataclass.level_type import LevelType, LevelMultiType
from src.enums.type_enum import MyTypeEnum
from src.enums.weird_type import WeirdType
from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import getSubKey, toClassStyle, snakeCase


@dataclass
class Level:
    name: str
    path: str
    depth: int = 0
    isSubKey: bool = False
    nullable: bool = False
    params: Dict[str, Any] = field(default_factory=dict)
    dtcBluePrint: Dict[str, str] = field(default_factory=dict)
    datas: List[Any] = field(default_factory=list)
    root: Optional["LevelRoot"] = None
    parent: Optional["Level"] = None
    type_: LevelMultiType = field(default_factory=LevelMultiType)
    realType: Optional[MyTypeEnum] = None
    weirdType: Optional[WeirdType] = None
    canBeNotPresent: bool = False
    isVariant: bool = False

    def __post_init__(self):
        self.params = self.getParamsBlueprint()
        self.dtcBluePrint = self.getDtcBlueprint()
        if len(self.datas) > 0:
            self.realType = MyTypeEnum.type_from_value(self.datas[0])
        for data in self.datas:
            self.addChildFromDatas(data)

    def addChildFromDatas(self, data):

        if isinstance(data, dict):
            if self.keysAreAllNum(data):
                self.weirdType = WeirdType.FAKE_DICT_LIST
                data = list(data.values())
        if isinstance(data, dict) and self.weirdType is None:
            for k, v in data.items():
                self.root.addChild(k, v, parent=self)
        elif isinstance(data, list) or self.weirdType == WeirdType.FAKE_DICT_LIST:
            subKey = getSubKey(self.name)
            for v in data:
                self.root.addChild(subKey, v, parent=self)
        elif data is None:
            self.nullable = True

    def addData(self, data):
        self.addChildFromDatas(data)
        self.datas.append(data)

    def findTypes(self):
        for data in self.datas:
            self.type_.addType(data)

    def parentFindTypes(self, children):
        hasSameType = self.childrenHasSameType(children)
        hasValidKey = self.childrenHasValidKey(children)
        length = len(self.datas)

        # todo find if we can find same class with different key
        if self.depth != 0:

            if len(children) == 0:
                self.realType = MyTypeEnum.ANY
            elif isinstance(self.datas[0], list) or self.weirdType == WeirdType.FAKE_DICT_LIST:
                if children[0].realType == MyTypeEnum.CLASS:
                    self.realType = MyTypeEnum.CLASS
                    self.type_.addNewType(
                        LevelType(primary=MyTypeEnum.LIST.value, secondary=[children[0].type_.type_[0].primary])
                    )
                else:
                    self.realType = MyTypeEnum.LIST
                    self.type_.addType(list())
                    self.type_.addChildren(children)
            elif isinstance(self.datas[0], dict):
                if not hasValidKey:
                    self.realType = MyTypeEnum.DICT
                    self.type_.addType(dict())
                    self.type_.addChildren(children)
                # elif self.name[-1] == "s" and hasSameType and type_[0].realType != MyTypeEnum.CLASS:
                #     # TODO: IS type_ Dict[Enum, Any]
                #     print('pass', self.path)
                #     self.realType = MyTypeEnum.DICT
                #     self.type_.addType(dict())
                #     self.type_.addChildren(type_)
                else:
                    # if self.name[-1] == "s":
                    #     self.name = self.name[:-1]
                    self.realType = MyTypeEnum.CLASS
                    self.type_.addClass(toClassStyle(self.name))
                    self.type_.addChildren(children)
        else:
            className = toClassStyle(self.name)
            if self.realType == MyTypeEnum.LIST:
                self.type_.addRootList(children)
            else:
                self.realType = MyTypeEnum.CLASS
                self.type_.addRootClass(className)
        if self.childHasDifferentLength(length, children) and self.realType != self.type_.types[
            0].primary != MyTypeEnum.LIST.value:
            sameKeys = [child.name for child in children if len(child.datas) == length]
            for child in children:
                if child.name not in sameKeys:
                    child.type_.type_[0].nullable = True

            # print(self)
            # print('same:\n', "\n".join([f"{' ' * 4}- {s.name}" for s in same]))
            # print('different:\n', "\n".join([f"{' ' * 4}- {s.name}" for s in different]))
        # for type_ in type_:
        #     if len(type_.datas) != length and self.type_.type_[0].primary != MyTypeEnum.LIST.value:
        #         type_.canBeNotPresent = True
        #         print(f"WARNING: {self} has different length than type_ {type_.name}")

    def childHasDifferentLength(self, length: int, children):
        for child in children:
            if len(child.datas) != length:
                return True
        return False

    def findVariants(self, length, children):
        signatures = dict()
        print(self)
        sameKeys = [child.name for child in children if len(child.datas) == length]
        print(sameKeys)
        for data in self.datas:
            signature = "_".join(list(data.keys() - sameKeys))
            if signature not in signatures:
                signatures[signature] = {"exemples": [data], "count": 1}
            else:
                signatures[signature]["exemples"].append(data['type_'])
                signatures[signature]["count"] += 1
        for signature, info in signatures.items():
            print("default class:", signature, info)

    @staticmethod
    def childrenHasSameType(children):
        if len(children) == 0:
            return False
        type_ = children[0].type_
        for child in children:
            if child.type_ != type_:
                return False
        return True

    @staticmethod
    def childrenHasValidKey(children):
        if len(children) == 0:
            return False
        for child in children:
            # make regex isalnum and can start by _
            if not re.match(r"^[a-zA-Z_]\w*$", child.name):
                return False
        return True

    def addNewParams(self, type_, key, value, isList: bool = False):
        if type_ in self.params:
            if type_ == "mapping":
                self.root.addImport(key, value)
            param = self.params[type_]
            if key not in param:
                param[key] = [value] if isList else value
            else:
                if isList:
                    param[key].append(value)
                else:
                    param[key] = value

    def generateDataclass(self, children):
        if self.root.verbose:
            self.printChildAndAncestor(children)
        isListRoot = self.depth == 0 and self.realType == MyTypeEnum.LIST
        for child in children:

            type_ = child.type_
            if isListRoot:
                self.addNewParams('attributes', self.name, {'type_': self.type_, "default": self.type_})
            else:
                self.addNewParams('attributes', child.name, {"type_": type_, "default": child.type_})
            isValidChild = child.realType == MyTypeEnum.CLASS \
                           and self.type_.types[0].primary not in (MyTypeEnum.LIST.value, MyTypeEnum.DICT.value)
            if isValidChild or isListRoot:

                if type_.type_[0].primary in (MyTypeEnum.LIST.value, MyTypeEnum.DICT.value):
                    if type_.type_[0].primary == MyTypeEnum.LIST.value:
                        newImport = str(child.type_.type_[0].secondary[0])
                        self.addNewParams('mapping', newImport, newImport, isList=True)
                    else:
                        newImport = str(child.type_.type_[0].secondary[0])
                        self.addNewParams('mapping', newImport, newImport, isList=True)
                else:
                    importType = str(child.type_.type_[0].primary)
                    self.addNewParams('mapping', child.name, importType, isList=True)
                if type_.type_[0].primary in (MyTypeEnum.LIST.value, MyTypeEnum.DICT.value) and not isListRoot:
                    self.addMapping(key=child.name, className=toClassStyle(child.type_.type_[0].secondary[0]),
                                    type_=type_.type_[0].primary, isListRoot=isListRoot,
                                    nullable=child.type_.type_[0].nullable, isWeirdDictList=child.weirdType == WeirdType.FAKE_DICT_LIST)
                elif not isListRoot:
                    self.addMapping(key=child.name, className=toClassStyle(child.name),
                                    type_=str(type_), isListRoot=isListRoot,
                                    nullable=child.type_.type_[0].nullable, isWeirdDictList=child.weirdType == WeirdType.FAKE_DICT_LIST)
                else:
                    self.addMapping(key=self.name, className=toClassStyle(child.name),
                                    type_=MyTypeEnum.LIST.value, isListRoot=isListRoot,
                                    nullable=child.type_.type_[0].nullable, isWeirdDictList=child.weirdType == WeirdType.FAKE_DICT_LIST)

            if child.isSubKey:
                self.addMatching(key=child.name, from_=child.name[1:])

        if self.realType == MyTypeEnum.CLASS \
                and self.type_.types[0].primary not in (MyTypeEnum.LIST.value, MyTypeEnum.DICT.value) \
                or isListRoot:
            with open(multiplePathJoins([self.root.dtc_path, snakeCase(self.root.name), f"{snakeCase(self.name)}.py"]),
                      'w') as f:
                f.write(self.dtcBluePrintToString(self.params))

    def printChildAndAncestor(self, children):
        print(self)
        print('\nChild and ancestor:')
        for child in children:

            if self.parent:
                print(
                    f"{' ' * 4}- type_: {child}\n"
                    f"{' ' * 4}- parent: {self}\n"
                    f"{' ' * 4}- parent.parent:  {self.parent}\n"
                )
            else:
                print(
                    f"{' ' * 4}- type_: {child}\n"
                    f"{' ' * 4}- parent: {self}\n"
                )

    def dtcBluePrintToString(self, params):
        attributes = "\n".join([
            self.getAttributeAsStr(k, attribute)
            for k, attribute in params["attributes"].items()
        ])
        self.dtcBluePrint["attributes"] = attributes

        if len(params['mapping']) > 0:
            self.dtcBluePrint["mapping"] = "\n".join([
                f"from {self.root.dtc_path}.{snakeCase(self.root.name)}.{snakeCase(k)} import " + ", ".join(
                    [str(v) for v in imports])
                for k, imports in params["mapping"].items()
            ]) + "\n"
        if len(params["mapping"]) > 0:
            for k, v in params['mapping'].items():
                if isinstance(v, dict):
                    print(self, k, v)
            fromMapping = [value for value in [v.from_dict_str() for k, v in params["mapping"].items()] if value != ""]
            toMapping = [value for value in [v.to_dict_str() for k, v in params["mapping"].items()] if value != ""]
            if len(fromMapping) > 0:
                self.dtcBluePrint["from_dict_mapping"] = "\n" + "\n".join(fromMapping)
            if len(toMapping) > 0:
                self.dtcBluePrint["to_dict_mapping"] = "\n" + "\n".join(toMapping)

        return copy(self.root.template).format(**self.dtcBluePrint)

    @staticmethod
    def getMappingAsStr(key, mapping):
        if mapping["isListRoot"]:
            return f"{' ' * 8}data = " + "{" \
                                         f"'{key}': [{mapping['className']}.from_dict(v).to_dict() for v in data]" \
                                         "}"
        base = f"{' ' * 8}data['{key}'] = "
        if mapping['type_'] == MyTypeEnum.LIST.value:
            base += f"[{mapping['className']}.from_dict(v).to_dict() for v in data['{key}']]"
        elif mapping['type_'] == MyTypeEnum.DICT.value:
            base += "{" + f"k: {mapping['className']}.from_dict(v).to_dict() for k, v in data['{key}'].items()" + "}"
        else:
            base += f"{mapping['className']}.from_dict(data['{key}']).to_dict()"
        if mapping['nullable']:
            base += f"{' ' * 8}if {key} in data:\n" \
                    f"{' ' * 4}"
        return base

    def getDtcBlueprint(self):
        return {
            "json_path": self.root.dtc_path,
            "mapping": "",
            "className": toClassStyle(self.name),
            "attributes": "",
            "to_dict_mapping": "",
            "from_dict_mapping": "",
            "variant": "",
        }

    @staticmethod
    def getParamsBlueprint():
        return {
            "mapping": dict(),
            "attributes": dict(),
            "matching": dict(),
            "mapping": dict(),
        }

    def __str__(self):
        return f"{self.path} : {self.realType if self.realType is not None else ''} {self.type_} => " \
               f"depth: {self.depth}, isSubKey: {self.isSubKey} "

    def addMapping(self, key, className, type_, nullable=False, isListRoot=False, isWeirdDictList=False):
        if key in self.params['mapping']:
            self.params['mapping'][key].className = className
            self.params['mapping'][key].type_ = type_
            self.params['mapping'][key].nullable = nullable
            self.params['mapping'][key].isListRoot = isListRoot
            self.params['mapping'][key].isWeirdDictList = isWeirdDictList
        else:
            self.params['mapping'][key] = SchemaMapping(key=key, className=className, type_=type_, nullable=nullable, isWeirdDictList=isWeirdDictList, isListRoot=isListRoot)

    def addMatching(self, key, from_):
        if key in self.params['mapping']:
            self.params['mapping'][key].from_ = from_
        else:
            self.params['mapping'][key] = SchemaMapping(key=key, from_=from_)

    def getAttributeAsStr(self, k, attribute):
        type_ = attribute["default"].type_[0]
        if type_.primary in (MyTypeEnum.LIST.value, MyTypeEnum.DICT.value) and not type_.nullable:
            default = f" = Field(default_factory={attribute['default'].type_[0].primary.lower()})"
        elif type_.primary is not None and type_.primary not in [v.value for v in
                                                                 MyTypeEnum.__members__.values()] and not type_.nullable:
            default = f" = Field(default_factory={attribute['default']})"
        else:
            default = f" = Field(default={self.getDefaultField(type_)})"
        return f"{' ' * 4}{k}: {attribute['type_']}{default}"

    @staticmethod
    def getDefaultField(type_: LevelType) -> str:
        if type_.nullable:
            return "None"
        typeStr = str(type_)
        match typeStr:
            case MyTypeEnum.INT.value:
                return "0"
            case MyTypeEnum.FLOAT.value:
                return ".0"
            case MyTypeEnum.STRING.value:
                return '""'
            case MyTypeEnum.BOOL.value:
                return "False"
            case _:
                raise Exception(f"wrong type_ or multi for getDefaultField: {typeStr}")

    def childrenAreFakeDictList(self, children):
        for child in children:
            if not child.name[1:].isnumeric():
                return False
        return True

    def keysAreAllNum(self, data):
        for k in data:
            if not k.isnumeric():
                return False
        return True

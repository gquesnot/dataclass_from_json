import json
import os
import shutil
from dataclasses import dataclass, field
from typing import Dict, Set, Any

from src.classes.level import Level
from src.enums.type_enum import MyTypeEnum
from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import removeExtension, snakeCase, keyIsAValidAttribute, toClassStyle


@dataclass
class LevelRoot:
    verbose: bool = False
    file_name: str = ""
    json_path: str = "jsons"
    dtc_path: str = "dataclass"
    template_path: str = "templates"
    template: str = ""
    imports: Dict[str, Set[Any]] = field(default_factory=dict)
    children: Dict[str, Level] = field(default_factory=dict)

    def __post_init__(self):
        self.name = removeExtension(self.file_name)
        self.imports = dict()
        self.children = dict()
        self.handleDirs()
        datas = self.getDatas()
        self.getTemplate()
        self.addChild(name=self.name, datas=datas)

    def getDatas(self):
        datas = None
        with open(multiplePathJoins([self.json_path, self.file_name])) as f:
            datas = json.load(f)
        return datas

    def getTemplate(self):
        with open(os.path.join(self.template_path, "template.py")) as f:
            self.template = f.read()

    @staticmethod
    def clearDir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def handleDirs(self):
        self.clearDir(multiplePathJoins([self.dtc_path, snakeCase(self.name)]))
        baseDtcClassPath = multiplePathJoins([self.dtc_path, "base_dataclass.py"])
        if not os.path.exists(baseDtcClassPath):
            shutil.copyfile(multiplePathJoins([self.template_path, "base_dataclass.py"]),
                            multiplePathJoins(baseDtcClassPath))

    def addChild(self, name, datas, parent=None):
        isSubKey = not keyIsAValidAttribute(name)
        if isSubKey:
            name = f"_{name}"
        path = parent.path + "." + name if parent is not None else name
        if path in self.children:
            self.children[path].addData(datas)
        else:
            self.children[path] = Level(name, datas=[datas], path=path, root=self, parent=parent,
                                        depth=0 if parent is None else parent.depth + 1,
                                        isSubKey=isSubKey
                                        )

    def findDataclasses(self):
        # order children by depth and path
        sortedChildren = sorted(self.children.values(), key=lambda x: x.depth, reverse=True)
        while len(sortedChildren) > 1:
            child = sortedChildren.pop(0)
            children = self.findChildren(child.parent)
            if len(sortedChildren) > 1:
                for child in children:
                    if child.realType != MyTypeEnum.CLASS:
                        child.findTypes()
            child.parent.parentFindTypes(children)
            sortedChildren = self.delChildren(sortedChildren, children)

    @staticmethod
    def delChildren(children, siblings):
        result = []
        for idx, child in enumerate(children):
            found = False
            for i, sib in enumerate(siblings):
                if child.parent is not None and sib.parent is not None and child.parent.path == sib.parent.path:
                    found = True
            if not found:
                result.append(child)
        return result

    def findChildren(self, parent):
        return [v for k, v in self.children.items() if v.parent is not None and v.parent.path == parent.path]

    def generateDataclass(self):
        sortedChildren = sorted(self.children.values(), key=lambda x: x.depth, reverse=True)
        while len(sortedChildren) > 1:
            child = sortedChildren.pop(0)
            children = self.findChildren(child.parent)
            child.parent.generateDataclass(children)
            if self.verbose:
                self.printParentChild(child.parent, children)
                print('_________________________________________________________\n')
            sortedChildren = self.delChildren(sortedChildren, children)

    @staticmethod
    def printParentChild(parent, children):
        print('Children:')
        print("\n".join([f"{' ' * 4}-{x}" for x in children]))

    def generateIniFile(self):
        iniFile = multiplePathJoins([self.dtc_path, snakeCase(self.name), "__init__.py"])
        self.addImport(self.name, toClassStyle(self.name))
        with open(iniFile, "w") as f:
            f.write(self.getImportsAsStr())

    def getImportsAsStr(self):
        # for k, v in self.imports.items():
        #     print(k, snakeCase(k), v)
        result = "\n".join([
            f"from {self.dtc_path}.{snakeCase(self.name)}.{snakeCase(k)} import " + ", ".join([str(v) for v in imports])
            for k, imports in self.imports.items()
        ]) + "\n"
        return result

    def addImport(self, key, value):
        if key not in self.imports:
            self.imports[key] = {value}
        self.imports[key].add(value)

    def rebuildChildrenToList(self, children):
        pass

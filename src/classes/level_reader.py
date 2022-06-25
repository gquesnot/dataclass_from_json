import os
from dataclasses import dataclass, field
from typing import Dict

from src.utils.handle_path import multiplePathJoins
from src.utils.string_manipulation import toClassStyle, removeExtension, snakeCase


@dataclass
class LevelReader:
    controller: "LevelController"
    modules: Dict[str, Dict[str, "BaseDataclass"]] = field(default_factory=dict)

    def load(self, name: str):
        if name not in self.modules:
            self.modules[name] = dict()
            path = multiplePathJoins([self.controller.dtc_path, snakeCase(name)])
            files = os.listdir(path)

            classesName = [toClassStyle(removeExtension(file)) for file in files if not file.startswith("__")]
            if len(classesName) == 0:
                raise Exception(f"Generate the Dataclass before , No One Found in {path}")
            self.modules[name] = __import__(f"{self.controller.dtc_path}.{snakeCase(name)}", fromlist=classesName)

    def get(self, name: str, datas=None):
        if "." in name:
            module, className = name.split(".")
        else:
            module = name
            className = name
        module = snakeCase(module)
        if module not in self.modules:
            self.load(module)
        _class = getattr(self.modules[module], toClassStyle(className))
        if datas is None:
            return _class
        else:
            return _class.from_dict(datas)

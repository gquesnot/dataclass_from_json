import json
import os
import pickle
from dataclasses import dataclass, field
from typing import List, Union

from src.classes.level_reader import LevelReader
from src.classes.level_root import LevelRoot
from src.utils.handle_path import multiplePathJoins
from src.utils.timeit import timeit


@dataclass
class LevelController:
    reader: LevelReader = field(init=False)
    verbose: bool = False
    json_path: str = "jsons"
    dtc_path: str = "dataclass"
    pickle_path = "pickles"

    def __post_init__(self):
        self.reader = LevelReader(controller=self)
        if not os.path.exists(self.dtc_path):
            os.makedirs(self.dtc_path)

    @timeit
    def savePickle(self, name: str, class_):
        with open(multiplePathJoins([self.pickle_path, name + ".pickle"]), "wb") as f:
            pickle.dump(class_, f)

    @timeit
    def loadPickle(self, name: str):
        with open(multiplePathJoins([self.pickle_path, name + ".pickle"]), "rb") as f:
            return pickle.load(f)

    def load(self, names: Union[List[str], str]):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self.reader.load(name)

    @timeit
    def getClass(self, names: Union[List[str], str], withDatas=False):
        isList1 = isinstance(names, list) and len(names) == 1
        if isinstance(names, str) or isList1:
            return self.getDtc(name=names if not isList1 else names[0], withDatas=withDatas)

        return [self.getDtc(name=name, withDatas=withDatas) for name in names]

    @timeit
    def get(self, name: str, datas):
        return self.reader.get(name=name, datas=datas)

    def getDtc(self, name: str, withDatas=False):
        datas = None
        if withDatas:
            with open(multiplePathJoins([self.json_path, name + ".json"]), "r") as f:
                datas = json.load(f)
        return self.reader.get(name=name, datas=datas)

    @timeit
    def generate(self, names: Union[List[str], str]):
        templatePath = multiplePathJoins(['src', 'templates'])
        if isinstance(names, str):
            names = [names]

        for name in names:
            levelParent = LevelRoot(file_name=f"{name}.json",
                                    template_path=templatePath,
                                    json_path=self.json_path,
                                    dtc_path=self.dtc_path,
                                    verbose=self.verbose)
            levelParent.findDataclasses()
            levelParent.generateDataclass()
            levelParent.generateIniFile()

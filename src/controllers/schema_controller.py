import json
import os
from typing import Dict, Any, List, Optional

import requests

from src.controllers.schema_root import SchemaRoot


class SchemaController:
    schema_root: SchemaRoot

    generate_only: bool = False
    load_only: bool = False
    show_data: bool = False
    show_schema: bool = False
    type: str = ""
    name: Optional[str] = None
    input: List[str] = list()
    output: str = ""
    verbose: bool = False
    datas: Dict[str, Any] = {}

    def __init__(self, args):
        self.schema_root = SchemaRoot(dtc_path=args.output)
        for k, v in args.__dict__.items():
            setattr(self, k, v)
        if self.type == "url" and self.name is None:
            raise Exception("name is required if type is url")

    def generate_all(self):
        self.get_datas()
        for k, v in self.datas.items():
            if not self.load_only:
                self.schema_root.generate(k, v)
            if not self.generate_only:
                data = self.schema_root.get(k, v, self.show_schema)
                if self.show_data:
                    print(data)

    def get_datas(self):
        if self.type == "json":
            self.datas = self.get_jsons_datas()
        else:
            self.datas = self.get_urls_datas()

    def get_jsons_datas(self):
        datas = {}
        for input_ in self.input:
            if os.path.exists(input_):
                if os.path.isfile(input_):
                    with open(input_, "r") as f:
                        datas[input_] = json.load(f)
                else:
                    for file in os.listdir(input_):
                        with open(os.path.join(input_, file), "r") as f:
                            datas[file] = json.load(f)

        return datas

    def get_urls_datas(self):
        datas = {}
        for input_ in self.input:
            try:
                datas[self.name] = requests.get(input_).json()
            except Exception as e:
                print(f"{input_} is not a valid url")
                print(e)

        return datas

    def __str__(self):
        return f"generate_only : {self.generate_only}\n" \
               f"load_only : {self.load_only}\n" \
               f"show_data : {self.show_data}\n" \
               f"show_schema : {self.show_schema}\n" \
               f"type : {self.type}\n" \
               f"input : {self.input}\n" \
               f"output : {self.output}\n" \
               f"verbose : {self.verbose}\n" \
               f"name: {self.name}\n"

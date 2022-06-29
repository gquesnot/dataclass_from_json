import json
from abc import ABC, abstractmethod

from src.schema.schema_root import SchemaRoot


class TestBuild():
    def __init__(self):
        self.sb = SchemaRoot(json_path="test_jsons", dtc_path="test_dataclass")

    def test_dict_simple(self):
        self.sb.generate("dict_simple")

    def test_dict_nested(self):
        self.sb.generate("dict_nested")

    def test_dict_real(self):
        self.sb.generate("dict_real")

    def test_list_root_simple(self):
        self.sb.generate("list_root_simple")

    def test_list_root_simple_obj(self):
        self.sb.generate("list_root_simple_obj")

    def test_list_obj(self):
        self.sb.generate("list_obj")

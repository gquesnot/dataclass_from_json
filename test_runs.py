import json
from abc import ABC, abstractmethod

from dataclass.champions.champions import Champions
from dataclass.items.items import Items
from dataclass.match.match import Match
from src.schema.schema_root import SchemaRoot


class BaseRun(ABC):

    @abstractmethod
    def test_run(self):
        pass


class TestMatch(BaseRun):
    def test_run(self):
        with open('jsons/match.json', 'r') as f:
            data = json.load(f)
        match = Match.from_dict(data)
        assert isinstance(match, Match)


class TestChampions(BaseRun):
    def test_run(self):
        with open('jsons/champions.json', 'r') as f:
            data = json.load(f)
        champions = Champions.from_dict(data)
        assert isinstance(champions, Champions)

class TestItems(BaseRun):
    def test_run(self):
        with open('jsons/items.json', 'r') as f:
            data = json.load(f)
        items = Items.from_dict(data)
        assert isinstance(items, Items)
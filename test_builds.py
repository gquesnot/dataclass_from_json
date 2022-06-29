import json
from abc import ABC, abstractmethod

from dataclass.champions.champions import Champions
from dataclass.match.match import Match
from src.schema.schema_root import SchemaRoot


class BaseBuild(ABC):
    @abstractmethod
    def test_build(self):
        pass


class TestMatch(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("match")
        sb.generate()


class TestChampions(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("champions")
        sb.generate()


class TestItems(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("items")
        sb.generate()


class TestMatchTimeline(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("matchTimeline")
        sb.generate()


class TestTraits(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("traits")
        sb.generate()


class TestLiveGame(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("live_game")
        sb.generate()


class TestComps(BaseBuild):
    def test_build(self):
        sb = SchemaRoot("comps")
        sb.generate()



import json

from dataclass.match.match import Match
from src.schema.schema_root import SchemaRoot

json_path = "..\\jsons"

def test_build():
    sb = SchemaRoot("match", json_path=json_path, dtc_path="..\\dataclass", template_path="..\\src\\templates")
    sb.generate()

def test_init():

    with open(json_path+'\\match.json', "r") as f:
        data = json.load(f)
    match = Match.from_dict(data)
    assert isinstance(match, Match)
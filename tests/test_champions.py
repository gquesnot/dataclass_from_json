import json

from dataclass.champions.champions import Champions
from src.schema.schema_root import SchemaRoot

json_path = "..\\jsons"

def test_build():
    sb = SchemaRoot("champions", json_path=json_path, dtc_path="..\\dataclass", template_path="..\\src\\templates")
    sb.generate()

def test_init():

    with open(json_path+'\\champions.json', "r") as f:
        data = json.load(f)
    champions = Champions.from_dict(data)
    assert isinstance(champions, Champions)


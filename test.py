import json
from test_dataclass.champions import Champions

if __name__ == "__main__":
    with open("test_jsons\\champions.json", "r") as f:
        data = json.load(f)
    champions = Champions.from_dict(data)
    for champName, champion in champions.data.items():
        print(champName, type(champName))

import json

from dataclass.champions.champions import Champions

if __name__ == '__main__':
    with open('jsons/champions.json') as f:
        data = json.load(f)
    champions = Champions.from_dict(data)

    for champion in champions.champions:
        print(champion.ability.name + champion.ability.desc+ champion.ability)

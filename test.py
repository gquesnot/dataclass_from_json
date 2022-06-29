import json

from dataclass.match.match import Match

if __name__ == '__main__':
    with open('jsons/match.json') as f:
        data = json.load(f)
    match = Match(**data)
    print(match)



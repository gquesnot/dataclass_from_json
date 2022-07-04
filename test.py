import json
from test_dataclass.match_timeline import MatchTimeline

if __name__ == "__main__":
    with open("matchTimeline.json", "r") as f:
        data = json.load(f)
    match_tl = MatchTimeline.from_dict(data)

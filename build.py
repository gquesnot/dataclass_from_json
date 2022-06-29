import json
from pprint import pprint

from src.schema.schema_root import SchemaRoot

#
# @timeit
# def to_dict(data):
#     return data.to_dict()
#
#
# @timeit
# def json_dict(data):
#     return data.__dict__
#
# @timeit
# def getMatchTimeline(data):
#
#     return MatchTimeline(**data)

if __name__ == '__main__':

    sb = SchemaRoot()
    sb.generate("comps")
    print(sb)

    # lvlController = LevelController()
    #
    # with open("jsons\\live_game.json", "r") as f:
    #     data = json.load(f)
    # builder = SchemaBuilder()
    # builder.add_object(data)
    # shema=  builder.to_schema()
    # print(builder.to_json(indent=4))
    # print()

    # matchTimeline = lvlController.get("MatchTimeline", data)
    # lvlController.savePickle("matchTimeline", matchTimeline)
    # lvlController.loadPickle("matchTimeline")
    # mtl = getMatchTimeline(data)

    # print(to_dict(mtl).keys())

    # print(json_dict(mtl).keys())
    # for frame in mtl.data.info.frames:
    #     for event in frame.events:
    #         if event.position is not None:
    #             print(event.type_, event.position)

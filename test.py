import json

import sys

from dataclass.bot import Bot

sys.setrecursionlimit(10000)
if __name__ == '__main__':
    with open('jsons\\bot.json', "r") as f:
        data = json.load(f)

    Bot.from_dict(data)
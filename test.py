import json
from test_dataclass.champions import Champions
from test_dataclass.champions.champions_.data_index import StatEnum, DataIndex

if __name__ == "__main__":
    statEnum = DataIndex.get_stat_enum()
    tagEnum = DataIndex.get_tag_enum()

    # champions = Champions.from_dict(data)
    # test1=champions.get_dataindex_enum().values()
    # test = champions.get_dataindex_enum().keys()
    # print(test1)
    # for   champName, champion in champions.data.items():
    #     print(champName, type(champName))

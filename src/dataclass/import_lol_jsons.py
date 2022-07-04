import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

import requests
from decouple import config

lol_ddragon = "https://ddragon.leagueoflegends.com"
lol_static = "https://static.developer.riotgames.com/docs/lol"
lol_api_euw = "https://euw1.api.riotgames.com"
lol_api_europe = "https://europe.api.riotgames.com"


@dataclass
class ImportLolJsons:
    json_path: str
    session: Optional[requests.session] = field(default=None)
    RIOT_API_KEY: Optional[str] = field(default=None)
    len_files = 15
    datas: Dict[str, Any] = field(default_factory=dict)

    urls = {
        "versions": lol_ddragon + "/api/versions.json",
        "maps": lol_static + "/maps.json",
        "seasons": lol_static + "/seasons.json",
        "queues": lol_static + "/queues.json",
        "gameModes": lol_static + "/gameModes.json",
        "gameTypes": lol_static + "/gameTypes.json",
        "regions": lol_ddragon + "/realms/euw.json",
        "languages": lol_ddragon + "/cdn/languages.json",
        "champions": lol_ddragon + "/cdn/{version}/data/en_US/champion.json",
        "summonerSpells": lol_ddragon + "/cdn/{version}/data/en_US/summoner.json",
        "profileIcons": lol_ddragon + "/cdn/{version}/data/en_US/profileicon.json",
        "items": lol_ddragon + "/cdn/{version}/data/en_US/item.json",
        "summoner": lol_api_euw + "/lol/summoner/v4/summoners/by-name/{name}",
        "matches": lol_api_europe + "/lol/match/v5/matches/by-puuid/{puuid}/ids",
        "match": lol_api_europe + "/lol/match/v5/matches/{matchId}",
        "matchTimeline": lol_api_europe + "/lol/match/v5/matches/{matchId}/timeline",
        "featuredMatches": lol_api_euw + "/lol/spectator/v4/featured-games",
        "spectator": lol_api_euw
                     + "/lol/spectator/v4/active-games/by-summoner/{encryptedSummonerId}",
        "challenges": lol_api_euw + "/lol/challenges/v1/player-data/{puuid}",
        "championsMasteries": lol_api_euw
                              + "/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}",
    }

    def __post_init__(self):
        self.len_files = len(self.urls)
        self.session = requests.session()

    def check_jsons_ok(self):
        if len(os.listdir("test_jsons")) != self.len_files:
            print("Jsons files not found, importing...")
            return self.import_jsons()
        return True

    def do_get(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(url, params={"api_key": self.RIOT_API_KEY})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return None

    def import_jsons(self):
        self.RIOT_API_KEY = config("RIOT_API_KEY")
        if self.RIOT_API_KEY is None:
            return False
        else:
            try:
                self.datas["versions"] = self.do_get(self.urls["versions"])
                self.datas["maps"] = self.do_get(self.urls["maps"])
                self.datas["seasons"] = self.do_get(self.urls["seasons"])
                self.datas["queues"] = self.do_get(self.urls["queues"])
                self.datas["gameModes"] = self.do_get(self.urls["gameModes"])
                self.datas["gameTypes"] = self.do_get(self.urls["gameTypes"])
                self.datas["regions"] = self.do_get(self.urls["regions"])
                self.datas["languages"] = self.do_get(self.urls["languages"])
                self.datas["champions"] = self.do_get(
                    self.urls["champions"].format(version=self.datas["versions"][0])
                )
                self.datas["summonerSpells"] = self.do_get(
                    self.urls["summonerSpells"].format(
                        version=self.datas["versions"][0]
                    )
                )
                self.datas["profileIcons"] = self.do_get(
                    self.urls["profileIcons"].format(version=self.datas["versions"][0])
                )
                self.datas["items"] = self.do_get(
                    self.urls["items"].format(version=self.datas["versions"][0])
                )
                print()
                self.datas["featuredMatches"] = self.do_get(self.urls["featuredMatches"])
                summoner_name = self.datas["featuredMatches"]["gameList"][0]["participants"][0]["summonerName"]

                self.datas["summoner"] = self.do_get(
                    self.urls["summoner"].format(name=summoner_name)
                )
                self.datas["spectator"] = self.do_get(
                    self.urls["spectator"].format(
                        encryptedSummonerId=self.datas["summoner"]["id"]
                    )
                )
                self.datas["matches"] = self.do_get(
                    self.urls["matches"].format(puuid=self.datas["summoner"]["puuid"])
                )
                match_id = self.datas["matches"][0]
                self.datas["match"] = self.do_get(
                    self.urls["match"].format(matchId=match_id)
                )
                self.datas["matchTimeline"] = self.do_get(
                    self.urls["matchTimeline"].format(matchId=match_id)
                )
                self.datas["challenges"] = self.do_get(
                    self.urls["challenges"].format(
                        puuid=self.datas["summoner"]["puuid"]
                    )
                )
                self.datas["championsMasteries"] = self.do_get(
                    self.urls["championsMasteries"].format(
                        encryptedSummonerId=self.datas["summoner"]["id"]
                    )
                )
                for k, v in self.datas.items():
                    with open(f"{self.json_path}/{k}.json", "w") as f:
                        f.write(json.dumps(v))
            except Exception as e:
                print(e)
                return False
            print("Jsons imported")
        return True

import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

import requests
from decouple import config

lolDDragon = "https://ddragon.leagueoflegends.com"
lolStatic = "https://static.developer.riotgames.com/docs/lol"
lolApiEuw = "https://euw1.api.riotgames.com"
lolApiEurope= "https://europe.api.riotgames.com"

@dataclass
class ImportLolJsons:
    json_path: str
    session: Optional[requests.Session] = field(default=None)
    RIOT_API_KEY: Optional[str] = field(default=None)
    lenFiles = 15
    datas: Dict[str, Any] = field(default_factory=dict)

    urls = {
        "versions": lolDDragon+"/api/versions.json",
        "maps": lolStatic+"/maps.json",
        "seasons": lolStatic+"/seasons.json",
        "queues": lolStatic+"/queues.json",
        "gameModes": lolStatic+"/gameModes.json",
        "gameTypes": lolStatic+"/gameTypes.json",
        "regions": lolDDragon+ "/realms/euw.json",
        "languages": lolDDragon+"/cdn/languages.json",
        "champions": lolDDragon+"/cdn/{version}/data/en_US/champion.json",
        "summonerSpells": lolDDragon+"/cdn/{version}/data/en_US/summoner.json",
        "profileIcons": lolDDragon+"/cdn/{version}/data/en_US/profileicon.json",
        "items": lolDDragon+"/cdn/{version}/data/en_US/item.json",
        "summoner": lolApiEuw+"/lol/summoner/v4/summoners/by-name/{name}",
        "matches": lolApiEurope+"/lol/match/v5/matches/by-puuid/{puuid}/ids",
        "match": lolApiEurope+"/lol/match/v5/matches/{matchId}",
        "matchTimeline": lolApiEurope+"/lol/match/v5/matches/{matchId}/timeline",
        "featuredMatches": lolApiEuw+"/lol/spectator/v4/featured-games",
        "spectator": lolApiEuw+"/lol/spectator/v4/active-games/by-summoner/{encryptedSummonerId}",
        "challenges": lolApiEuw+"/lol/challenges/v1/player-data/{puuid}",
        "championsMasteries": lolApiEuw+"/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}",
    }

    def __post_init__(self):
        self.lenFiles = len(self.urls)
        self.session = requests.Session()

    def checkJsonsOk(self):
        if len(os.listdir("test_jsons")) != self.lenFiles:
            print("Jsons files not found, importing...")
            return self.import_jsons()
        return True

    def doGet(self, url: str) -> Optional[Dict[str, Any]]:
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
                #self.session.headers.update({"X-Riot-Token": self.RIOT_API_KEY})

                self.datas["versions"] = self.doGet(self.urls["versions"])
                self.datas["maps"] = self.doGet(self.urls["maps"])
                self.datas["seasons"] = self.doGet(self.urls["seasons"])
                self.datas["queues"] = self.doGet(self.urls["queues"])
                self.datas["gameModes"] = self.doGet(self.urls["gameModes"])
                self.datas["gameTypes"] = self.doGet(self.urls["gameTypes"])
                self.datas["regions"] = self.doGet(self.urls["regions"])
                self.datas["languages"] = self.doGet(self.urls["languages"])
                self.datas["champions"] = self.doGet(self.urls["champions"].format(version=self.datas["versions"][0]))
                self.datas["summonerSpells"] = self.doGet(self.urls["summonerSpells"].format(version=self.datas["versions"][0]))
                self.datas["profileIcons"] = self.doGet(self.urls["profileIcons"].format(version=self.datas["versions"][0]))
                self.datas["items"] = self.doGet(self.urls["items"].format(version=self.datas["versions"][0]))
                self.datas["featuredMatches"] = self.doGet(self.urls["featuredMatches"])
                summonerName = self.datas['featuredMatches']['gameList'][0]['participants'][0]['summonerName']

                self.datas["summoner"] = self.doGet(self.urls["summoner"].format(name=summonerName))
                self.datas['spectator'] = self.doGet(self.urls['spectator'].format(encryptedSummonerId=self.datas['summoner']['id']))
                self.datas["matches"] = self.doGet(self.urls["matches"].format(puuid=self.datas["summoner"]["puuid"]))
                matchId = self.datas["matches"][0]
                self.datas["match"] = self.doGet(self.urls["match"].format(matchId=matchId))
                self.datas["matchTimeline"] = self.doGet(self.urls["matchTimeline"].format(matchId=matchId))
                self.datas["challenges"] = self.doGet(self.urls["challenges"].format(puuid=self.datas["summoner"]["puuid"]))
                self.datas["championsMasteries"] = self.doGet(self.urls["championsMasteries"].format(encryptedSummonerId=self.datas["summoner"]["id"]))

                for k, v in self.datas.items():
                    with open(f"{self.json_path}/{k}.json", "w") as f:
                        f.write(json.dumps(v))
            except Exception as e:
                print(e)
                return False
            print("Jsons imported")
        return True

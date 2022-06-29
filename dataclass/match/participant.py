from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel
from dataclass.match.challenges import Challenges
from dataclass.match.perks import Perks


class Participant(BaseModel):
    assists: int = 0
    baronKills: int = 0
    bountyLevel: int = 0
    challenges: Challenges = Field(default_factory=Challenges)
    champExperience: int = 0
    champLevel: int = 0
    championId: int = 0
    championName: str = ''
    championTransform: int = 0
    consumablesPurchased: int = 0
    damageDealtToBuildings: int = 0
    damageDealtToObjectives: int = 0
    damageDealtToTurrets: int = 0
    damageSelfMitigated: int = 0
    deaths: int = 0
    detectorWardsPlaced: int = 0
    doubleKills: int = 0
    dragonKills: int = 0
    eligibleForProgression: bool = False
    firstBloodAssist: bool = False
    firstBloodKill: bool = False
    firstTowerAssist: bool = False
    firstTowerKill: bool = False
    gameEndedInEarlySurrender: bool = False
    gameEndedInSurrender: bool = False
    goldEarned: int = 0
    goldSpent: int = 0
    individualPosition: str = ''
    inhibitorKills: int = 0
    inhibitorTakedowns: int = 0
    inhibitorsLost: int = 0
    item0: int = 0
    item1: int = 0
    item2: int = 0
    item3: int = 0
    item4: int = 0
    item5: int = 0
    item6: int = 0
    itemsPurchased: int = 0
    killingSprees: int = 0
    kills: int = 0
    lane: str = ''
    largestCriticalStrike: int = 0
    largestKillingSpree: int = 0
    largestMultiKill: int = 0
    longestTimeSpentLiving: int = 0
    magicDamageDealt: int = 0
    magicDamageDealtToChampions: int = 0
    magicDamageTaken: int = 0
    neutralMinionsKilled: int = 0
    nexusKills: int = 0
    nexusLost: int = 0
    nexusTakedowns: int = 0
    objectivesStolen: int = 0
    objectivesStolenAssists: int = 0
    participantId: int = 0
    pentaKills: int = 0
    perks: Perks = Field(default_factory=Perks)
    physicalDamageDealt: int = 0
    physicalDamageDealtToChampions: int = 0
    physicalDamageTaken: int = 0
    profileIcon: int = 0
    puuid: str = ''
    quadraKills: int = 0
    riotIdName: str = ''
    riotIdTagline: str = ''
    role: str = ''
    sightWardsBoughtInGame: int = 0
    spell1Casts: int = 0
    spell2Casts: int = 0
    spell3Casts: int = 0
    spell4Casts: int = 0
    summoner1Casts: int = 0
    summoner1Id: int = 0
    summoner2Casts: int = 0
    summoner2Id: int = 0
    summonerId: str = ''
    summonerLevel: int = 0
    summonerName: str = ''
    teamEarlySurrendered: bool = False
    teamId: int = 0
    teamPosition: str = ''
    timeCCingOthers: int = 0
    timePlayed: int = 0
    totalDamageDealt: int = 0
    totalDamageDealtToChampions: int = 0
    totalDamageShieldedOnTeammates: int = 0
    totalDamageTaken: int = 0
    totalHeal: int = 0
    totalHealsOnTeammates: int = 0
    totalMinionsKilled: int = 0
    totalTimeCCDealt: int = 0
    totalTimeSpentDead: int = 0
    totalUnitsHealed: int = 0
    tripleKills: int = 0
    trueDamageDealt: int = 0
    trueDamageDealtToChampions: int = 0
    trueDamageTaken: int = 0
    turretKills: int = 0
    turretTakedowns: int = 0
    turretsLost: int = 0
    unrealKills: int = 0
    visionScore: int = 0
    visionWardsBoughtInGame: int = 0
    wardsKilled: int = 0
    wardsPlaced: int = 0
    win: bool = False

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Participant":
        data['challenges'] = Challenges.from_dict(data['challenges']).to_dict()
        data['perks'] = Perks.from_dict(data['perks']).to_dict()
        return Participant(**data)

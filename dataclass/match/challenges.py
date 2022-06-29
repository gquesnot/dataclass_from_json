from typing import Dict, Any, List, Union, Optional
from pydantic import Field, BaseModel


class Challenges(BaseModel):
    _12AssistStreakCount: int = 0
    abilityUses: int = 0
    acesBefore15Minutes: int = 0
    alliedJungleMonsterKills: int = 0
    baronTakedowns: int = 0
    blastConeOppositeOpponentCount: int = 0
    bountyGold: int = 0
    buffsStolen: int = 0
    completeSupportQuestInTime: int = 0
    controlWardTimeCoverageInRiverOrEnemyHalf: Optional[float] = None
    controlWardsPlaced: int = 0
    damagePerMinute: float = 0.0
    damageTakenOnTeamPercentage: float = 0.0
    dancedWithRiftHerald: int = 0
    deathsByEnemyChamps: int = 0
    dodgeSkillShotsSmallWindow: int = 0
    doubleAces: int = 0
    dragonTakedowns: int = 0
    earliestBaron: float = 0.0
    earliestDragonTakedown: Optional[float] = None
    earlyLaningPhaseGoldExpAdvantage: Optional[int] = None
    effectiveHealAndShielding: float = 0.0
    elderDragonKillsWithOpposingSoul: int = 0
    elderDragonMultikills: int = 0
    enemyChampionImmobilizations: int = 0
    enemyJungleMonsterKills: float = 0.0
    epicMonsterKillsNearEnemyJungler: int = 0
    epicMonsterKillsWithin30SecondsOfSpawn: int = 0
    epicMonsterSteals: int = 0
    epicMonsterStolenWithoutSmite: int = 0
    firstTurretKilledTime: Optional[float] = None
    flawlessAces: int = 0
    fullTeamTakedown: int = 0
    gameLength: float = 0.0
    getTakedownsInAllLanesEarlyJungleAsLaner: Optional[int] = None
    goldPerMinute: float = 0.0
    hadAfkTeammate: int = 0
    hadOpenNexus: int = 0
    highestCrowdControlScore: Optional[int] = None
    immobilizeAndKillWithAlly: int = 0
    initialBuffCount: int = 0
    initialCrabCount: int = 0
    jungleCsBefore10Minutes: int = 0
    junglerTakedownsNearDamagedEpicMonster: int = 0
    kTurretsDestroyedBeforePlatesFall: int = 0
    kda: float = 0.0
    killAfterHiddenWithAlly: int = 0
    killParticipation: float = 0.0
    killedChampTookFullTeamDamageSurvived: int = 0
    killingSprees: Optional[int] = None
    killsNearEnemyTurret: int = 0
    killsOnOtherLanesEarlyJungleAsLaner: Optional[int] = None
    killsOnRecentlyHealedByAramPack: int = 0
    killsUnderOwnTurret: int = 0
    killsWithHelpFromEpicMonster: int = 0
    knockEnemyIntoTeamAndKill: int = 0
    landSkillShotsEarlyGame: int = 0
    laneMinionsFirst10Minutes: int = 0
    laningPhaseGoldExpAdvantage: Optional[int] = None
    legendaryCount: int = 0
    lostAnInhibitor: int = 0
    maxCsAdvantageOnLaneOpponent: Optional[int] = None
    maxKillDeficit: int = 0
    maxLevelLeadLaneOpponent: Optional[int] = None
    moreEnemyJungleThanOpponent: float = 0.0
    multiKillOneSpell: int = 0
    multiTurretRiftHeraldCount: int = 0
    multikills: int = 0
    multikillsAfterAggressiveFlash: int = 0
    mythicItemUsed: Optional[int] = None
    outerTurretExecutesBefore10Minutes: int = 0
    outnumberedKills: int = 0
    outnumberedNexusKill: int = 0
    perfectDragonSoulsTaken: int = 0
    perfectGame: int = 0
    pickKillWithAlly: int = 0
    poroExplosions: int = 0
    quickCleanse: int = 0
    quickFirstTurret: int = 0
    quickSoloKills: int = 0
    riftHeraldTakedowns: int = 0
    saveAllyFromDeath: int = 0
    scuttleCrabKills: int = 0
    shortestTimeToAceFromFirstTakedown: Optional[float] = None
    skillshotsDodged: int = 0
    skillshotsHit: int = 0
    snowballsHit: int = 0
    soloBaronKills: int = 0
    soloKills: int = 0
    soloTurretsLategame: int = 0
    stealthWardsPlaced: int = 0
    survivedSingleDigitHpCount: int = 0
    survivedThreeImmobilizesInFight: int = 0
    takedownOnFirstTurret: int = 0
    takedowns: int = 0
    takedownsAfterGainingLevelAdvantage: int = 0
    takedownsBeforeJungleMinionSpawn: int = 0
    takedownsFirstXMinutes: int = 0
    takedownsInAlcove: int = 0
    takedownsInEnemyFountain: int = 0
    teamBaronKills: int = 0
    teamDamagePercentage: float = 0.0
    teamElderDragonKills: int = 0
    teamRiftHeraldKills: int = 0
    threeWardsOneSweeperCount: int = 0
    tookLargeDamageSurvived: int = 0
    turretPlatesTaken: int = 0
    turretTakedowns: int = 0
    turretsTakenWithRiftHerald: int = 0
    twentyMinionsIn3SecondsCount: int = 0
    unseenRecalls: int = 0
    visionScoreAdvantageLaneOpponent: Optional[float] = None
    visionScorePerMinute: float = 0.0
    wardTakedowns: int = 0
    wardTakedownsBefore20M: int = 0
    wardsGuarded: int = 0
    junglerKillsEarlyJungle: Optional[int] = None
    killsOnLanersEarlyJungleAsJungler: Optional[int] = None
    teleportTakedowns: Optional[int] = None
    highestWardKills: Optional[int] = None
    highestChampionDamage: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = self.dict()
        return data

    @classmethod
    def from_dict(cls, data: Any) -> "Challenges":
        data['_12AssistStreakCount'] = data['12AssistStreakCount']
        del data['12AssistStreakCount']

        return Challenges(**data)

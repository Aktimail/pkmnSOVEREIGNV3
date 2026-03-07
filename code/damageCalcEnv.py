class DamageCalcEnv:
    def __init__(self, attacker, defender, move, battle_data):
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.battleData = battle_data

        self.ignoreWeather = False
        self.weatherFinalMod = 0x1000

        self.criticalHit = False
        self.criticalHitLevel = move.criticalRate
        self.ignoreCriticalHit = False

        self.randomFactor = 0

        self.stabFinalMod = 0x1000

        self.typeEffectiveness = 0

        self.burnEffect = False

        self.globalFinalMods = []
        self.globalFinalMod = 0x1000

        self.ignoreReflectLightScreen = False

        self.basePowerValue = move.basePower
        self.basePowerMods = []
        self.basePowerFinalMod = 0x1000

        self.atkStatUser = self.attacker
        self.atkStatId = {"physical": "atk", "special": "aspe"}[self.move.category]
        self.atkBoostId = self.atkStatId
        self.atkIgnoreBoost = False
        self.atkStatValue = 0
        self.atkStatMods = []
        self.atkStatFinalMod = 0x1000

        self.defeStatUser = self.defender
        self.defeStatId = {"physical": "defe", "special": "dspe"}[self.move.category]
        self.defeBoostId = self.defeStatId
        self.defeIgnoreBoost = False
        self.defeStatValue = 0
        self.defeStatMods = []
        self.defeStatFinalMod = 0x1000

        self.damageValueOverride = None
        self.damageFactor = 0

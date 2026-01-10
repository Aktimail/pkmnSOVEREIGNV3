class DamageCalcEnv:
    def __init__(self, attacker, defender, move, battle_data):
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.battleData = battle_data

        self.fullOverride = False

        self.weatherMods = []
        self.weatherFinalMod = 0
        self.ignoreWeather = False

        self.criticalHit = False
        self.criticalHitLevel = move.criticalRate
        self.ignoreCriticalHit = False

        self.randomFactor = 0

        self.stabFinalMod = 0x1000

        self.typeEffectiveness = 0

        self.burnEffect = False

        self.globalFinalMods = []
        self.globalFinalModValue = 0

        self.basePowerValue = move.basePower
        self.basePowerMods = []
        self.basePowerFinalMod = 0

        self.atkStatUser = self.attacker
        self.atkStat = {"physical": "atk", "special": "aspe"}[self.move.category]
        self.atkStatIgnoreBoost = False
        self.atkStatValue = 0
        self.atkStatMods = []
        self.atkStatFinalMod = 0

        self.defeStatUser = self.defender
        self.defeStat = {"physical": "defe", "special": "dspe"}[self.move.category]
        self.defeStatIgnoreBoost = False
        self.defeStatValue = 0
        self.defeStatMods = []
        self.defeStatFinalMod = 0
class DamageCalcEnv:
    def __init__(self, attacker, defender, move, battle_data):
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.battleData = battle_data

        self.basePower = move.basePower
        self.basePowerMods = []

        self.atkStat = (attacker.)
        self.atkStatMods = []

        self.defeStat = 0
        self.defeStatMods = []

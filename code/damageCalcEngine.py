from battleEngineMethodManager import BattleEngineMethodManager

class DamageCalcEngine:
    def __init__(self, env):
        self.Env = env
        self.BEMM = BattleEngineMethodManager()

        self.flags = []

    @staticmethod
    def apply_mod(value, mod):
        return round((value * mod) / 0x1000)

    @staticmethod
    def chain_up(*mods):
        chained_mod = 0X1000
        for mod in mods:
            chained_mod = ((chained_mod * mod) + 0x800) >> 12
        return chained_mod

    def collect_methods(self):
        for pkmn in [self.Env.attacker, self.Env.defender]:
            self.BEMM.register(pkmn.Ability.battleEngineMethod)
            if pkmn.get_item():
                self.BEMM.register(pkmn.Item.battleEngineMethod)

        self.BEMM.register(self.Env.move.battleEngineMethod)

    def compute_base_power_param(self):
        for method in self.BEMM.emit("basePowerRules"):
            method.resolve(self.Env)

        for method in self.BEMM.emit("basePowerMods"):
            method.resolve(self.Env)

    def compute_atk_stat_param(self):

        for method in self.BEMM.emit("atkStatRules"):
            method.resolve(self.Env)

        for method in self.BEMM.emit("atkStatMods"):
            method.resolve(self.Env)

    def compute_defe_stat_param(self):

        for method in self.BEMM.emit("atkStatRules"):
            method.resolve(self.Env)

        for method in self.BEMM.emit("atkStatMods"):
            method.resolve(self.Env)

import random

from battleEngineMethodManager import BattleEngineMethodManager


class DamageCalcEngine:
    def __init__(self, env):
        self.Env = env
        self.BEM_Manager = BattleEngineMethodManager()

        self.atkLvlParam = self.Env.attacker.level
        self.basePowerParam = 0
        self.atkStatParam = 0
        self.defeStatParam = 0

        self.damageValue = 0

    @staticmethod
    def apply_mod(value, mod):
        return round((value * mod) / 0x1000)

    @staticmethod
    def chain_up(modifiers):
        chained_mod = 0X1000
        for mod in modifiers:
            chained_mod = ((chained_mod * mod) + 0x800) >> 12
        return chained_mod

    def collect_methods(self):
        for pkmn in [self.Env.attacker, self.Env.defender]:
            self.BEM_Manager.register(pkmn.Ability.battleEngineMethod)
            if pkmn.get_item():
                self.BEM_Manager.register(pkmn.Item.battleEngineMethod)

        self.BEM_Manager.register(self.Env.move.battleEngineMethod)

    def check_special_cases(self):
        for method in self.BEM_Manager.emit("specialCases"):
            method.resolve(self.Env)

    def set_weather_mod(self):
        for method in self.BEM_Manager.emit("weatherRules"):
            method.resolve(self.Env)

        for method in self.BEM_Manager.emit("weatherMods"):
            method.resolve(self.Env)

        self.Env.weatherFinalMod = self.chain_up(self.Env.weatherMods)

    def set_critical_hit(self, ignore=False):
        if not ignore:
            for method in self.BEM_Manager.emit("criticalHitRules"):
                method.resolve(self.Env)

            if not self.Env.ignoreCriticalHit:
                critical_hit_factors = [1/16, 1/8, 1/4, 1/3, 1/2]
                r = random.random()

                if self.Env.criticalHitLevel >= len(critical_hit_factors):
                    self.Env.criticalHitLevel = len(critical_hit_factors) - 1

                if r <= critical_hit_factors[self.Env.criticalHitLevel]:
                    self.Env.criticalHit = True

    def set_random_factor(self, const="random"):
        if const == "random":
            r = random.randint(0, 15)
            self.Env.randomFactor = r
        else:
            self.Env.randomFactor = const

    def set_stab_mod(self):
        if self.Env.move.type in self.Env.attacker.type:
            self.Env.stabFinalMod = 0x1800

        for method in self.BEM_Manager.emit("stabRules"):
            method.resolve(self.Env)

    def set_type_effectiveness(self):
        self.Env.typeEffectiveness = self.Env.move.get_type_effectiveness(self.Env.defender)

    def set_burn_effect(self):
        if self.Env.move.category == "physical":
            if self.Env.attacker.status["main"] == "burned":
                if self.Env.attacker.get_ability() != "guts":
                    self.Env.burnEffect = True

    def set_final_mod(self):
        for method in self.BEM_Manager.emit("finalMods"):
            method.resolve(self.Env)

        self.Env.globalFinalModValue = self.chain_up(self.Env.globalFinalMods)

    def compute_base_power_param(self):
        for method in self.BEM_Manager.emit("basePowerRules"):
            method.resolve(self.Env)

        for method in self.BEM_Manager.emit("basePowerMods"):
            method.resolve(self.Env)

        self.Env.basePowerFinalMod = self.chain_up(self.Env.basePowerMods)
        self.basePowerParam = self.apply_mod(self.Env.basePowerValue, self.Env.basePowerFinalMod)

        print("basePower : " + str(self.basePowerParam))

    def compute_atk_stat_param(self):
        for method in self.BEM_Manager.emit("atkStatRules"):
            method.resolve(self.Env)

        self.Env.atkStatValue = self.Env.atkStatUser.get_stage_stat(
            self.Env.atkStat, ignore_boost=self.Env.atkStatIgnoreBoost, crit=self.Env.criticalHit
        )

        for method in self.BEM_Manager.emit("atkStatMods"):
            method.resolve(self.Env)

        self.Env.atkStatFinalMod = self.chain_up(self.Env.atkStatMods)
        self.atkStatParam = self.apply_mod(self.Env.atkStatValue, self.Env.atkStatFinalMod)

        print("atkStat : " + str(self.atkStatParam))

    def compute_defe_stat_param(self):
        for method in self.BEM_Manager.emit("defeStatRules"):
            method.resolve(self.Env)

        self.Env.defeStatValue = self.Env.defeStatUser.get_stage_stat(
            self.Env.defeStat, ignore_boost=self.Env.defeStatIgnoreBoost, crit=self.Env.criticalHit
        )

        for method in self.BEM_Manager.emit("defeStatMods"):
            method.resolve(self.Env)

        self.Env.defeStatFinalMod = self.chain_up(self.Env.defeStatMods)
        self.defeStatParam = self.apply_mod(self.Env.defeStatValue, self.Env.defeStatFinalMod)

        print("defeStat : " + str(self.defeStatParam))

    def compute_base_damage(self):
        self.damageValue = ((((2 * self.atkLvlParam) // 5 + 2)
                             * self.basePowerParam * self.atkStatParam) // self.defeStatParam) // 50 + 2

    def calcul_damage(self, ignore_crit=False, r="random"):
        print(self.Env.attacker.globalStats)
        print(self.Env.defender.globalStats)

        self.check_special_cases()

        if not self.Env.fullOverride:
            self.set_weather_mod()
            self.set_critical_hit(ignore=ignore_crit)
            self.set_random_factor(const=r)
            self.set_stab_mod()
            self.set_type_effectiveness()
            self.set_burn_effect()
            self.set_final_mod()

            self.compute_base_power_param()
            self.compute_atk_stat_param()
            self.compute_defe_stat_param()

            self.compute_base_damage()

            self.damageValue = self.apply_mod(self.damageValue, self.Env.weatherFinalMod)

            if self.Env.criticalHit:
                self.damageValue *= 2

            self.damageValue = (self.damageValue * (100 - self.Env.randomFactor)) // 100

            self.damageValue = self.apply_mod(self.damageValue, self.Env.stabFinalMod)

            if self.Env.typeEffectiveness > 0:
                self.damageValue = self.damageValue << self.Env.typeEffectiveness
            elif self.Env.typeEffectiveness < 0:
                self.damageValue = self.damageValue >> self.Env.typeEffectiveness

            if self.Env.burnEffect:
                self.damageValue = self.damageValue // 2

            if self.damageValue < 1:
                self.damageValue = 1

            self.damageValue = self.apply_mod(self.damageValue, self.Env.globalFinalModValue)
            print(self.damageValue)

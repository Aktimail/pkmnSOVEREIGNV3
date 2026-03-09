import random

from damageCalcEnv import DamageCalcEnv
from battleEngineMethodManager import BattleEngineMethodManager


class DamageCalcEngine:
    def __init__(self):
        self.Env = None
        self.BEM_Manager = BattleEngineMethodManager()

        self.atkLvlParam = 0
        self.basePowerParam = 0
        self.atkStatParam = 0
        self.defeStatParam = 0

        self.damageValue = 0

    def init_env(self, attacker, defender, move, battle_data):
        self.Env = DamageCalcEnv(attacker, defender, move, battle_data)

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
        for role, pkmn in {"attacker": self.Env.attacker, "defender": self.Env.defender}.items():
            if pkmn.ability.bem and role in (pkmn.ability.bem.relative, "pokemons"):
                self.BEM_Manager.register(pkmn.ability.bem)
            if pkmn.get_item() and pkmn.item.bem and role in (pkmn.item.bem.relative, "pokemons"):
                self.BEM_Manager.register(pkmn.item.bem)

        if self.Env.move.bem:
            self.BEM_Manager.register(self.Env.move.bem)

    def resolve_trigger(self, trigger):
        for method in self.BEM_Manager.emit(trigger):
            method.resolve(self.Env)

    def check_special_cases(self):
        self.resolve_trigger("specialCasesRules")

    def set_weather_mod(self):
        if self.Env.battleData.weather in ("rain", "sunny") and self.Env.move.get_type() in ("water", "fire"):
            self.resolve_trigger("weatherRules")
            weather_mods_table = {
                "rain": {
                    "water": 0x1800,
                    "fire": 0x800
                },
                "sunny": {
                    "water": 0x800,
                    "fire": 0x1800
                }
            }
            self.Env.weatherFinalMod = weather_mods_table[self.Env.battleData.weather][self.Env.move.get_type()]

    def set_critical_hit(self, ignore=False):
        if not ignore:
            self.resolve_trigger("criticalHitRules")

            if not self.Env.ignoreCriticalHit:
                critical_hit_factors = [1/16, 1/8, 1/4, 1/3, 1/2]
                r = random.random()

                if self.Env.criticalHitLevel >= len(critical_hit_factors):
                    self.Env.criticalHitLevel = len(critical_hit_factors) - 1

                if r <= critical_hit_factors[self.Env.criticalHitLevel]:
                    self.Env.criticalHit = True

    def set_random_factor(self, const=False):
        if not const:
            r = random.randint(0, 15)
            self.Env.randomFactor = r
        else:
            self.Env.randomFactor = 0

    def set_stab_mod(self):
        if self.Env.move.get_type() in self.Env.attacker.get_type():
            self.Env.stabFinalMod = 0x1800

            self.resolve_trigger("stabRules")

    def set_type_effectiveness(self):
        self.Env.typeEffectiveness = self.Env.move.get_type_effectiveness(self.Env.defender)

    def set_burn_effect(self):
        if self.Env.move.category == "physical":
            if self.Env.attacker.status["main"] == "burned":
                if self.Env.attacker.get_ability() != "guts":
                    self.Env.burnEffect = True

    def set_final_mod(self):
        self.resolve_trigger("finalModifiers")
        self.Env.globalFinalMod = self.chain_up(self.Env.globalFinalMods)

    def compute_level_param(self):
        self.atkLvlParam = self.Env.attacker.level

    def compute_base_power_param(self):
        self.resolve_trigger("basePowerRules")

        self.resolve_trigger("basePowerModifiers")

        self.Env.basePowerFinalMod = self.chain_up(self.Env.basePowerMods)
        self.basePowerParam = self.apply_mod(self.Env.basePowerValue, self.Env.basePowerFinalMod)

        print("basePower : " + str(self.basePowerParam))

    def compute_atk_stat_param(self):
        self.resolve_trigger("atkStatRules")

        self.Env.atkStatValue = self.Env.atkStatUser.get_stage_stat(
            self.Env.atkStatId,
            boost_id=self.Env.atkBoostId,
            ignore_boost=self.Env.atkIgnoreBoost,
            crit=self.Env.criticalHit
        )

        self.resolve_trigger("atkStatModifiers")

        self.Env.atkStatFinalMod = self.chain_up(self.Env.atkStatMods)
        self.atkStatParam = self.apply_mod(self.Env.atkStatValue, self.Env.atkStatFinalMod)

        print("atkStat : " + str(self.atkStatParam))

    def compute_defe_stat_param(self):
        self.resolve_trigger("defeStatRules")

        self.Env.defeStatValue = self.Env.defeStatUser.get_stage_stat(
            self.Env.defeStatId,
            boost_id=self.Env.defeBoostId,
            ignore_boost=self.Env.defeIgnoreBoost,
            crit=self.Env.criticalHit
        )

        self.resolve_trigger("defeStatModifiers")

        self.Env.defeStatFinalMod = self.chain_up(self.Env.defeStatMods)
        self.defeStatParam = self.apply_mod(self.Env.defeStatValue, self.Env.defeStatFinalMod)

        print("defeStat : " + str(self.defeStatParam))

    def compute_base_damage(self):
        self.damageValue = ((((2 * self.atkLvlParam) // 5 + 2)
                             * self.basePowerParam * self.atkStatParam) // self.defeStatParam) // 50 + 2

    def calcul_damage(self, ignore_crit=False, const_r=False):
        self.collect_methods()

        self.check_special_cases()

        if self.Env.damageValueOverride is None:
            self.set_weather_mod()
            self.set_critical_hit(ignore=ignore_crit)
            self.set_random_factor(const=const_r)
            self.set_stab_mod()
            self.set_type_effectiveness()
            self.set_burn_effect()
            self.set_final_mod()

            self.compute_level_param()
            self.compute_base_power_param()
            self.compute_atk_stat_param()
            self.compute_defe_stat_param()

            self.compute_base_damage()

            if not self.Env.ignoreWeather:
                self.damageValue = self.apply_mod(self.damageValue, self.Env.weatherFinalMod)

            if self.Env.criticalHit:
                self.damageValue *= 2

            self.damageValue = (self.damageValue * (100 - self.Env.randomFactor)) // 100

            self.damageValue = self.apply_mod(self.damageValue, self.Env.stabFinalMod)

            if self.Env.typeEffectiveness > 0:
                self.damageValue = self.damageValue << self.Env.typeEffectiveness
            elif self.Env.typeEffectiveness < 0:
                self.damageValue = self.damageValue >> abs(self.Env.typeEffectiveness)

            if self.Env.burnEffect:
                self.damageValue = self.damageValue // 2

            if self.damageValue < 1:
                self.damageValue = 1

            self.damageValue = self.apply_mod(self.damageValue, self.Env.globalFinalMod)

            if self.Env.damageFactor:
                self.damageValue = int(self.damageValue * self.Env.damageFactor)

            print(self.damageValue)

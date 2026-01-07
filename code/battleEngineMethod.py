class BattleEngineMethod:
    TRIGGER = None
    PRIORITY = 0

    def resolve(self, env): ...


class FrustrationMethod(BattleEngineMethod):
    TRIGGER = "basePowerRulesX"
    PRIORITY = 0

    def resolve(self, env):
        env.basePowerValue = max(1, int(((255 - env.attacker.happiness) * 10) / 25))
        env.basePowerOverride = True


class HeatProofMethod(BattleEngineMethod):
    TRIGGER = "basePowerModifiersX"
    PRIORITY = 8

    def resolve(self, env):
        if env.move.get_type() == "fire":
            env.basePowerMods.append(0x800)

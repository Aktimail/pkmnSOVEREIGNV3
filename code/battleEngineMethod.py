class BattleEngineMethod:
    TRIGGER = None
    PRIORITY = 0

    def resolve(self, env): ...


class FrustrationMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 1

    def resolve(self, env):
        env.basePowerValue = max(1, ((255 - env.attacker.happiness) * 10) // 25)


class PaybackMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 2

    def resolve(self, env):
        if env.battleData.has_target_moved():  # to do
            env.basePowerValue = 100


class ReturnMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 3

    def resolve(self, env):
        env.basePowerValue = max(1, (env.attacker.happiness * 10) // 25)


class ElectroBallMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 4

    def resolve(self, env):
        speed_delta = env.attacker.get_stage_stat("spd") // env.defender.get_stage_stat("spd")
        if speed_delta >= 4:
            env.basePowerValue = 150
        elif 4 > speed_delta >= 3:
            env.basePowerValue = 120
        elif 3 > speed_delta >= 2:
            env.basePowerValue = 80
        elif 2 > speed_delta >= 1:
            env.basePowerValue = 60
        else:
            env.basePowerValue = 40


class AvalancheMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 5

    def resolve(self, env):
        if env.battleData.check_avalanche_effect():  # to do
            env.basePowerValue = 120


class GyroBallMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 6

    def resolve(self, env):
        env.basePowerValue = min(150, 25 * env.attacker.get_stage_stat("spd") // env.defender.get_stage_stat("spd"))


class EruptionMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 7

    def resolve(self, env):
        env.basePowerValue = max(1, (150 * env.attacker.currentHp) // env.attacker.globalStats["hp"])


class PunishementMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 8

    def resolve(self, env):
        statup_total = 0
        for lvl in env.defender.boosts.values():
            if lvl > 0:
                statup_total += 1
        env.basePowerValue = min(120, 60 + 20 * statup_total)


class FuryCutterMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 9

    def resolve(self, env):
        use_counter = env.battleData.successive_uses_counter(env.move, successfull=True)  # to do
        env.basePowerValue = 20 * 2 ** use_counter


class LowKickMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 10

    def resolve(self, env):
        target_weight = env.defender.get_weight()
        if target_weight >= 200:
            env.basePowerValue = 120
        elif 200 > target_weight >= 100:
            env.basePowerValue = 100
        elif 100 > target_weight >= 50:
            env.basePowerValue = 80
        elif 50 > target_weight >= 25:
            env.basePowerValue = 60
        elif 25 > target_weight >= 10:
            env.basePowerValue = 40
        else:
            env.basePowerValue = 20


class EchoedVoiceMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 11

    def resolve(self, env):
        use_counter = env.battleData.successive_uses_counter(env.move, successfull=False)  # to do
        env.basePowerValue = 40 * use_counter


class HexMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 12

    def resolve(self, env):
        if env.defender.get_main_status():
            env.basePowerValue = 100


class WringOutMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 13

    def resolve(self, env):
        target_hp_ratio = env.defender.currentHp / env.defender.globalStats["hp"]
        env.basePowerValue = round(120 * target_hp_ratio) // 100


class AssuranceMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 14

    def resolve(self, env):
        if env.battleData.check_assurance_effect():  # to do
            env.basePowerValue = 100


class HeavySlamMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 15

    def resolve(self, env):
        weight_delta = env.attacker.get_weight() // env.defender.get_weight()
        if weight_delta >= 5:
            env.basePowerValue = 120
        elif 5 > weight_delta >= 4:
            env.basePowerValue = 100
        elif 4 > weight_delta >= 3:
            env.basePowerValue = 80
        elif 3 > weight_delta >= 2:
            env.basePowerValue = 60
        else:
            env.basePowerValue = 40


class StoredPowerMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 16

    def resolve(self, env):
        statup_total = 0
        for lvl in env.defender.boosts.values():
            if lvl > 0:
                statup_total += lvl
        env.basePowerValue = 20 + 20 * statup_total


class AcrobaticMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 17

    def resolve(self, env):
        if not env.attacker.get_item():
            env.basePowerValue = 110


class FlailMethod(BattleEngineMethod):
    TRIGGER = "basePowerRules"
    PRIORITY = 18

    def resolve(self, env):
        p = (48 * env.attacker.currentHp) // env.attacker.globalStats["hp"]
        if p <= 1:
            env.basePowerValue = 200
        elif 2 <= p <= 4:
            env.basePowerValue = 150
        elif 5 <= p <= 9:
            env.basePowerValue = 100
        elif 10 <= p <= 16:
            env.basePowerValue = 80
        elif 17 <= p <= 32:
            env.basePowerValue = 40
        else:
            env.basePowerValue = 20


class HeatproofMethod(BattleEngineMethod):
    TRIGGER = "basePowerModifiers"
    PRIORITY = 8

    def resolve(self, env):
        if env.move.get_type() == "fire":
            env.basePowerMods.append(0x800)

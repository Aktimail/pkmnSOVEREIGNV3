import random


class BattleEngineMethod:
    relative = None
    client = None
    trigger = None
    priority = 0

    def resolve(self, env): ...


class FrustrationMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 1

    def resolve(self, env):
        env.basePowerValue = max(1, ((255 - env.attacker.happiness) * 10) // 25)


class PaybackMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 2

    def resolve(self, env):
        if env.battleData.has_target_moved():  # to do
            env.basePowerValue = 100


class ReturnMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 3

    def resolve(self, env):
        env.basePowerValue = max(1, (env.attacker.happiness * 10) // 25)


class ElectroBallMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 4

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
    trigger = "basePowerRules"
    priority = 5

    def resolve(self, env):
        if env.battleData.check_avalanche_effect():  # to do
            env.basePowerValue = 120


class GyroBallMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 6

    def resolve(self, env):
        env.basePowerValue = min(150, 25 * env.attacker.get_stage_stat("spd") // env.defender.get_stage_stat("spd"))


class EruptionMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 7

    def resolve(self, env):
        env.basePowerValue = max(1, (150 * env.attacker.currentHp) // env.attacker.globalStats["hp"])


class PunishementMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 8

    def resolve(self, env):
        statup_total = 0
        for lvl in env.defender.boosts.values():
            if lvl > 0:
                statup_total += 1
        env.basePowerValue = min(120, 60 + 20 * statup_total)


class FuryCutterMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 9

    def resolve(self, env):
        use_counter = env.battleData.successive_uses_counter(env.move, successfull=True)  # to do
        env.basePowerValue = 20 * 2 ** use_counter


class LowKickMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 10

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
    trigger = "basePowerRules"
    priority = 11

    def resolve(self, env):
        use_counter = env.battleData.successive_uses_counter(env.move)  # to do
        env.basePowerValue = 40 * use_counter


class HexMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 12

    def resolve(self, env):
        if env.defender.get_main_status():
            env.basePowerValue = 100


class WringOutMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 13

    def resolve(self, env):
        target_hp_ratio = env.defender.currentHp * 0x1000 // env.defender.globalStats["hp"] * 0x1000
        env.basePowerValue = round(120 * target_hp_ratio) // 100


class AssuranceMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 14

    def resolve(self, env):
        if env.battleData.check_assurance_effect():  # to do
            env.basePowerValue = 100


class HeavySlamMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 15

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
    trigger = "basePowerRules"
    priority = 16

    def resolve(self, env):
        statup_total = 0
        for lvl in env.defender.boosts.values():
            if lvl > 0:
                statup_total += lvl
        env.basePowerValue = 20 + 20 * statup_total


class AcrobaticMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 17

    def resolve(self, env):
        if not env.attacker.get_item():
            env.basePowerValue = 110


class FlailMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 18

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

class TrumpCardMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 19

    def resolve(self, env):
        if env.move.pp >= 5:
            env.basePowerValue = 40
        elif env.move.pp == 4:
            env.basePowerValue = 50
        elif env.move.pp == 3:
            env.basePowerValue = 60
        elif env.move.pp == 2:
            env.basePowerValue = 80
        elif env.move.pp == 1:
            env.basePowerValue = 200


class RoundMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 20

    def resolve(self, env):
        pass  # BP is doubled to 120 if used in direct succession of an ally


class TripleKickMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 21

    def resolve(self, env):
        if env.attacker.multipleHitCounter == 1:
            env.basePowerValue = 10
        elif env.attacker.multipleHitCounter == 2:
            env.basePowerValue = 20
        elif env.attacker.multipleHitCounter == 3:
            env.basePowerValue = 30


class WakeUpSlapMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 22

    def resolve(self, env):
        if env.defender.get_main_status() == "asleep":
            env.basePowerValue = 120


class SmellingSaltMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 23

    def resolve(self, env):
        if env.defender.get_main_status() == "paralyzed":
            env.basePowerValue = 120


class WeatherBallMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 24

    def resolve(self, env):
        if env.battleData.weather.status:
            env.basePowerValue = 100


class GustMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 25

    def resolve(self, env):
        if env.defender.isInTheSky:
            env.basePowerValue = 80


class BeatUpMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 26

    def resolve(self, env):
        pkmn_remaining = env.battleData.get_team_len(env.attacker)
        env.basePowerValue = pkmn_remaining // 10 + 5


class HiddenPowerMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 27

    def resolve(self, env):
        ivs = [env.attacker.ivs["hp"],
               env.attacker.ivs["atk"],
               env.attacker.ivs["defe"],
               env.attacker.ivs["spd"],
               env.attacker.ivs["aspe"],
               env.attacker.ivs["dspe"]]
        ivs_sum = 0
        for i in range(len(ivs)):
            ivs_sum += ((ivs[i] >> 1) & 1) << i

        env.basePowerValue = 30 + (40 * ivs_sum) // 63

class SpitUpMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 28

    def resolve(self, env):
        env.basePowerValue = 100 * env.attacker.stockpile


class PursuitMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 29

    def resolve(self, env):
        if env.battleData.check_puirsuit_effect():
            env.basePowerValue = 80


class PresentMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 30

    def resolve(self, env):
        r = random.randint(0, 79)
        if r < 40:
            env.basePowerValue = 40
        elif 40 <= r < 70:
            env.basePowerValue = 80
        else:
            env.basePowerValue = 120


class NaturalGiftMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 31

    def resolve(self, env):
        berries_table = {
            "cheri_berry": {
                "id": 1,
                "type": "fire",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "chesto_berry": {
                "id": 2,
                "type": "water",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "pecha_berry": {
                "id": 3,
                "type": "electric",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "rawst_berry": {
                "id": 4,
                "type": "grass",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "aspear_berry": {
                "id": 5,
                "type": "ice",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "leppa_berry": {
                "id": 6,
                "type": "fighting",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "oran_berry": {
                "id": 7,
                "type": "poison",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "persim_berry": {
                "id": 8,
                "type": "ground",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "lum_berry": {
                "id": 9,
                "type": "flying",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "sitrus_berry": {
                "id": 10,
                "type": "psychic",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "figy_berry": {
                "id": 11,
                "type": "bug",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "wiki_berry": {
                "id": 12,
                "type": "rock",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "mago_berry": {
                "id": 13,
                "type": "ghost",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "aguav_berry": {
                "id": 14,
                "type": "dragon",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "lapapa_berry": {
                "id": 15,
                "type": "dark",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "razz_berry": {
                "id": 16,
                "type": "steel",
                "naturalGiftPower": 60,
                "damageLoweringType": False
            },
            "bluk_berry": {
                "id": 17,
                "type": "fire",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "nanab_berry": {
                "id": 18,
                "type": "water",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "wepear_berry": {
                "id": 19,
                "type": "electric",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "pinap_berry": {
                "id": 20,
                "type": "grass",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "pomeg_berry": {
                "id": 21,
                "type": "ice",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "kelpsy_berry": {
                "id": 22,
                "type": "fighting",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "qualot_berry": {
                "id": 23,
                "type": "poison",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "hondew_berry": {
                "id": 24,
                "type": "ground",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "grepa_berry": {
                "id": 25,
                "type": "flying",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "tamato_berry": {
                "id": 26,
                "type": "psychic",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "comn_berry": {
                "id": 27,
                "type": "bug",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "magost_berry": {
                "id": 28,
                "type": "rock",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "rabuta_berry": {
                "id": 29,
                "type": "ghost",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "nomel_berry": {
                "id": 30,
                "type": "dragon",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "spelon_berry": {
                "id": 31,
                "type": "dark",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "pamtre_berry": {
                "id": 32,
                "type": "steel",
                "naturalGiftPower": 70,
                "damageLoweringType": False
            },
            "watmel_berry": {
                "id": 33,
                "type": "fire",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "durin_berry": {
                "id": 34,
                "type": "water",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "belue_berry": {
                "id": 35,
                "type": "electric",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "occa_berry": {
                "id": 36,
                "type": "fire",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "passho_berry": {
                "id": 37,
                "type": "water",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "wacan_berry": {
                "id": 38,
                "type": "electric",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "rindo_berry": {
                "id": 39,
                "type": "grass",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "yache_berry": {
                "id": 40,
                "type": "ice",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "chople_berry": {
                "id": 41,
                "type": "fighting",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "kebia_berry": {
                "id": 42,
                "type": "poison",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "shuca_berry": {
                "id": 43,
                "type": "ground",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "coba_berry": {
                "id": 44,
                "type": "flying",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "payapa_berry": {
                "id": 45,
                "type": "psychic",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "tanga_berry": {
                "id": 46,
                "type": "bug",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "charti_berry": {
                "id": 47,
                "type": "rock",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "kasib_berry": {
                "id": 48,
                "type": "ghost",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "haban_berry": {
                "id": 49,
                "type": "dragon",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "colbur_berry": {
                "id": 50,
                "type": "dark",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "babiri_berry": {
                "id": 51,
                "type": "steel",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "chilan_berry": {
                "id": 52,
                "type": "normal",
                "naturalGiftPower": 60,
                "damageLoweringType": True
            },
            "liechi_berry": {
                "id": 53,
                "type": "grass",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "ganlon_berry": {
                "id": 54,
                "type": "ice",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "salac_berry": {
                "id": 55,
                "type": "fighing",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "petaya_berry": {
                "id": 56,
                "type": "poison",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "apicot_berry": {
                "id": 57,
                "type": "ground",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "lansat_berry": {
                "id": 58,
                "type": "flying",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "starf_berry": {
                "id": 59,
                "type": "psychic",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "enigma_berry": {
                "id": 60,
                "type": "bug",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "micle_berry": {
                "id": 61,
                "type": "rock",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "custap_berry": {
                "id": 62,
                "type": "ghost",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "jaboca_berry": {
                "id": 63,
                "type": "dragon",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            },
            "rowap_berry": {
                "id": 64,
                "type": "dark",
                "naturalGiftPower": 80,
                "damageLoweringType": False
            }
        }
        if env.attacker.get_item() in berries_table:
            env.basePowerValue = berries_table[env.attacker.get_item()]


class MagnitudeMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 32

    def resolve(self, env):
        r = random.randint(0, 100)
        if r < 5:
            factor = 0
        elif 5 <= r < 15:
            factor = 1
        elif 15 <= r < 35:
            factor = 2
        elif 35 <= r < 65:
            factor = 3
        elif 65 <= r < 85:
            factor = 4
        elif 85 <= r < 95:
            factor = 5
        else:
            factor = 7
        env.basePowerValue = 10 + 20 * factor


class RolloutMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 33

    def resolve(self, env):
        use_counter = env.battleData.successive_uses_counter(env.move, successfull=True, limit=5)
        defense_curl = 1 if env.attacker.defenseCurl else 0
        env.basePowerValue = 30 * 2 ** (use_counter + defense_curl)


class FlingMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 34

    def resolve(self, env):
        env.basePowerValue = env.move.flingPower


class PledgeMethod(BattleEngineMethod):
    trigger = "basePowerRules"
    priority = 35

    def resolve(self, env):
        pass  # skip ally turn if its used move is either grass/fire/water pledge and set bp to 150


class TechnicianMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 1

    def resolve(self, env):
        if env.basePowerValue <= 60:
            env.basePowerMods.append(0x1800)


class FlareBoostMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 2

    def resolve(self, env):
        if env.attacker.get_main_status() == "burn" and env.move.category == "special":
            env.basePowerMods.append(0x1800)


class AnalyticMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 3

    def resolve(self, env):
        if env.move.dbSymbol not in ["future_sight", "doom_desire"] and env.battleData.has_target_moved():
            env.basePowerMods.append(0x14CD)


class RecklessMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 4

    def resolve(self, env):
        if env.move.effects.get("recoil") or env.move.dbSymbol in ["jump_kick", "high_jump_kick"]:
            env.basePowerMods.append(0x1333)


class IronFistMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 5

    def resolve(self, env):
        if env.move.flags["isPunch"]:
            env.basePowerMods.append(0x1333)


class ToxicBoostMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 6

    def resolve(self, env):
        if env.attacker.get_main_status() == "poison" and env.move.category == "physical":
            env.basePowerMods.append(0x1800)


class RivalryMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 7

    def resolve(self, env):
        if env.attacker.get_gender() == "genderless" or env.defender.get_gender() == "genderless":
            env.basePowerMods.append(0x1000)
        elif env.attacker.get_gender() == env.defender.get_gender():
            env.basePowerMods.append(0x1400)
        elif env.attacker.get_gender() != env.defender.get_gender():
            env.basePowerMods.append(0xC00)


class HeatproofMethod(BattleEngineMethod):
    trigger = "basePowerModifiers"
    priority = 8

    def resolve(self, env):
        if env.move.get_type() == "fire":
            env.basePowerMods.append(0x800)

import random
import json


class DamageCalculator:
    def __init__(self):
        self.attacker = None
        self.defender = None
        self.move = None
        self.battleData = None

        self.calcData = {}
        self.debugReport = {}

        self.berries = json.load(open("../assets/data/other/berriesTable.json"))
        self.plates = json.load(open("../assets/data/other/platesTable.json"))
        self.gems = json.load(open("../assets/data/other/gemsTable.json"))
        self.incenses = json.load(open("../assets/data/other/typeEnhancingIncences.json"))
        self.items = json.load(open("../assets/data/other/typeEnhancingItems.json"))
        self.sheerforce_moves = json.load(open("../assets/data/other/sheerForceTable.json"))

    def init_calcul(self, attacker, defender, move, battle_data):
        self.attacker = attacker
        self.defender = defender
        self.move = move
        self.battleData = battle_data

        self.calcData.clear()

    @staticmethod
    def apply_mod(value, mod):
        return round((value * mod) / 0x1000)

    @staticmethod
    def chain_up(*mods):
        chained_mod = 0X1000
        for mod in mods:
            chained_mod = ((chained_mod * mod) + 0x800) >> 12
        return chained_mod

    def get_power(self):
        pass

    def check_power_trigger(self):
        if self.move.dbSymbol == "frustration":
            return max(int(((255 - self.attacker.happiness) * 10) / 25), 1)

        elif self.move.dbSymbol == "payback" and not self.battleData.is_first_to_move():
            return 100

        elif self.move.dbSymbol == "return":
            return max(int((self.attacker.happiness * 10) / 25), 1)

        elif self.move.dbSymbol == "electro_ball":
            d_speed = self.attacker.get_stage_stat("spd") / self.defender.get_stage_stat("spd")
            if d_speed >= 4:
                return 150
            elif 4 > d_speed >= 3:
                return 120
            elif 3 > d_speed >= 2:
                return 80
            elif 2 > d_speed >= 1:
                return 60
            else:
                return 40
        elif self.move.dbSymbol == "avalanche":  # 120 if the target has inflicted non-effect damage to the user
            # this turn
            return 120

        elif self.move.dbSymbol == "gyro_ball":
            return min(int(25 * self.defender.get_stage_stat("spd") / self.attacker.get_stage_stat("spd")), 150)

        elif self.move.dbSymbol in ["eruption", "water_spout"]:
            return max(int((150 * self.attacker.currentHp) / self.attacker.globalStats["hp"]), 1)

        elif self.move.dbSymbol == "punishment":
            sum_boost_lvl = sum(val for val in self.defender.boosts.values() if val >= 0)
            return min(120, 60 + 20 * sum_boost_lvl)

        elif self.move.dbSymbol == "fury_cutter":
            use_counter = 0  # counts successive and successful previous uses up to a maximum of 3
            return 20 * 2 ** use_counter

        elif self.move.dbSymbol in ["low_kick", "grass_knot"]:
            if self.defender.get_weight() >= 200:
                return 120
            elif 200 > self.defender.get_weight() >= 100:
                return 100
            elif 100 > self.defender.get_weight() >= 50:
                return 80
            elif 50 > self.defender.get_weight() >= 25:
                return 60
            elif 25 > self.defender.get_weight() >= 10:
                return 40
            else:
                return 20

        elif self.move.dbSymbol == "echoed_voice":
            pass  # BP increases in the listed order every turn this move is used successively on the user's side of
            # the field

        elif self.move.dbSymbol == "hex" and self.defender.status["main"]:
            return 100

        elif self.move.dbSymbol in ["wring_out", "crush_grip"]:
            return int(120 * (self.defender.currentHp / self.defender.globalStats["hp"]))

        elif self.move.dbSymbol == "assurance":  # BP is doubled to 100 if target has already been inflicted
            # non-effect damage this turn
            return 100

        elif self.move.dbSymbol in ["heavy_slam", "heat_crash"]:
            d_weight = self.attacker.get_weight() / self.defender.get_weight()
            if d_weight >= 5:
                return 120
            elif 5 > d_weight >= 4:
                return 100
            elif 4 > d_weight >= 3:
                return 80
            elif 3 > d_weight >= 2:
                return 60
            else:
                return 40

        elif self.move.dbSymbol == "stored_power":
            sum_boost_lvl2 = sum(val for val in self.attacker.boosts.values() if val >= 0)
            return 20 + 20 * sum_boost_lvl2

        elif self.move.dbSymbol == "acrobatics" and not self.attacker.get_item():
            return 110

        elif self.move.dbSymbol in ["flail", "reversal"]:
            p = (48 * self.attacker.currentHp) / self.attacker.globalStats["hp"]
            if p <= 1:
                return 200
            elif 2 <= p <= 4:
                return 150
            elif 5 <= p <= 9:
                return 100
            elif 10 <= p <= 16:
                return 80
            elif 17 <= p <= 32:
                return 40
            else:
                return 20

        elif self.move.dbSymbol == "trump_card":
            if self.move.pp >= 5:
                return 40
            elif self.move.pp == 4:
                return 50
            elif self.move.pp == 3:
                return 60
            elif self.move.pp == 2:
                return 80
            else:
                return 200

        elif self.move.dbSymbol == "round":  # BP is doubled to 120 if used in direct succession of an ally
            return 60

        elif self.move.dbSymbol == "triple_kick":  # BP is listed for the successive hits
            return 10

        elif self.move.dbSymbol == "wake_up_slap" and self.defender.status["main"] == "asleep":
            return 120

        elif self.move.dbSymbol == "smelling_salts" and self.defender.status["main"] == "paralysis":
            return 120

        elif self.move.dbSymbol == "weather_ball":  # BP is doubled to 100 in any non-default weather
            return 100

        elif self.move.dbSymbol in ["guts", "twister"]:  # BP is doubled to 80 is target is in the charging turn of
            # Bounce, Fly or Sky Drop / personals flags for pkmn instead
            return 80

        elif self.move.dbSymbol == "beat_up":  # this move attacks once for every non fainted member in the user's
            # party, including the user
            return 1

        elif self.move.dbSymbol == "hidden_power":
            ivs_value = 0
            i = 0
            for iv in self.attacker.ivs.values():
                ivs_value += ((iv >> 1) & 1) << i
                i += 1
            return int(30 + (40 * ivs_value) / 63)

        elif self.move.dbSymbol == "spit_up":  # stockpile is the stockpile counter ranging from 0 to 3
            return 100

        elif self.move.dbSymbol == "pursuit":  # BP is doubled to 80 if target is switching out
            return 80

        elif self.move.dbSymbol == "present":
            r = random.randint(0, 80)
            if r < 40:
                return 40
            elif 40 <= r < 70:
                return 80
            else:
                return 120

        elif self.move.dbSymbol == "natural_gift":
            if self.attacker.get_item() in self.berries:
                return self.berries[self.attacker.get_item()]["naturalGiftPower"]

        elif self.move.dbSymbol == "magnitude":
            r = random.randint(0, 100)
            if r < 5:
                result = 0
            elif 5 <= r < 15:
                result = 1
            elif 15 <= r < 35:
                result = 2
            elif 35 <= r < 65:
                result = 3
            elif 65 <= r < 85:
                result = 4
            elif 85 <= r < 95:
                result = 5
            else:
                result = 7
            return 10 + 20 * result

        elif self.move.dbSymbol == "rollout":  # use_counter counts successive and successful previous uses up to a
            # maximum of 5, defense_curl is 1 if user used Defense Curl previously on field, 0 otherwise
            return 30 * 2 ** 1

        elif self.move.dbSymbol == "fling" and self.attacker.get_item():
            return self.attacker.get_item().flingPower

        elif self.move.dbSymbol in ["grass_pledge", "fire_pledge", "water_pledge"]:  # if a slower ally used a different
            # Pledge move this turn, it will skip its turn and this move's base power will be set to 150
            return 150

    def get_power_mod(self):
        pass

    def get_atk(self):
        pass

    def check_atk_trigger(self):
        pass

    def get_atk_mod(self):
        pass

    def get_defe(self):
        pass

    def check_defe_trigger(self):
        pass

    def get_defe_mod(self):
        pass

    def calcul_base_damage(self, pwr, atk, defe):
        return int(((((2 * self.attacker.level) / 5 + 2) * pwr * atk) / defe) / 50 + 2)

    def get_weather_mod(self):
        pass

    def get_crit_mod(self):
        pass

    def get_stab_mod(self):
        pass

    def get_type_mod(self):
        pass

    def get_burn_mod(self):
        pass

    def get_last_mod(self):
        pass

    def get_result(self):
        pass

    def check_special_case(self):
        pass

    def calcul_damage(self, attacker, defender, move, battle_data):
        self.init_calcul(attacker, defender, move, battle_data)

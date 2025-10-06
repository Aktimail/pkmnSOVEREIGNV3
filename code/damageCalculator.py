import json


class DamageCalculator:
    def __init__(self):
        self.attacker = None
        self.defender = None
        self.move = None
        self.battleData = None

        self.calcData = {}

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
        if self.move.dbSymbol == "frustration":
            return int(((255 - self.attacker.happiness) * 10) / 25)
        elif self.move.dbSymbol == "payback" and not self.battleData.is_first_to_move():
            return 100

    def get_power_mod(self):
        pass

    def get_atk(self):
        pass

    def get_atk_mod(self):
        pass

    def get_defe(self):
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

    def calcul_damage(self, attacker, defender, move, battle_data):
        self.init_calcul(attacker, defender, move, battle_data)

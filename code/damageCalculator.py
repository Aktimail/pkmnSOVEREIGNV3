import random
import json


class DamageCalculator:
    def __init__(self, pkmn1, pkmn2, move, battle_data):
        self.pkmn1 = pkmn1
        self.pkmn2 = pkmn2
        self.move = move
        self.battleData = battle_data

        self.berries = json.load(open("../assets/data/other/berriesTable.json"))
        self.plates = json.load(open("../assets/data/other/platesTable.json"))
        self.gems = json.load(open("../assets/data/other/gemsTable.json"))
        self.incenses = json.load(open("../assets/data/other/typeEnhancingIncences.json"))
        self.items = json.load(open("../assets/data/other/typeEnhancingItems.json"))
        self.sheerforce_moves = json.load(open("../assets/data/other/sheerForceTable.json"))

    @staticmethod
    def apply_mod(value, mod):
        return round((value * mod) / 0x1000)

    @staticmethod
    def chain_up(*mods):
        chained_mod = 0X1000
        for mod in mods:
            chained_mod = ((chained_mod * mod) + 0x800) >> 12
        return chained_mod

    def get_base_damage(self, pwr, atk, defe):
        return int(((((2 * self.pkmn1.level) / 5 + 2) * pwr * atk) / defe) / 50 + 2)


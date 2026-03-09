import os
import math
import random
import json
import uuid

from specie import Specie
from move import Move
from ability import Ability
from item import Item


class Pokemon(Specie):
    def __init__(self, dbsymbol, level, mod=None):
        super().__init__(dbsymbol)

        self.UID = uuid.uuid4().hex
        self.shiny = True if random.random() <= 1 / 8192 else False

        self.level = level

        self.gender = self.init_gender()
        self.ability = self.init_ability()
        self.item = self.init_item()

        self.moveset = self.init_moveset()

        self.ivs = {"hp": random.randint(0, 31),
                    "atk": random.randint(0, 31),
                    "defe": random.randint(0, 31),
                    "aspe": random.randint(0, 31),
                    "dspe": random.randint(0, 31),
                    "spd": random.randint(0, 31)
                    }

        self.evs = {"hp": 0,
                    "atk": 0,
                    "defe": 0,
                    "aspe": 0,
                    "dspe": 0,
                    "spd": 0
                    }

        self.nature = self.init_nature()

        self.boosts = {"atk": 0, "defe": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
        self.status = {"main": None, "sec": []}

        self.exp = 0
        self.remainingExp = self.exp_to_nxt_lvl()

        self.sprites = {
            "front": self.get_sprite_path("front", gender=self.gender, shiny=self.shiny),
            "back": self.get_sprite_path("back", gender=self.gender, shiny=self.shiny)
        }

        self.happiness = 0

        if mod:
            self.init_mod(mod)

        self.globalStats = {
            "hp": self.init_stat("hp"),
            "atk": self.init_stat("atk"),
            "defe": self.init_stat("defe"),
            "aspe": self.init_stat("aspe"),
            "dspe": self.init_stat("dspe"),
            "spd": self.init_stat("spd")
        }
        self.currentHp = self.globalStats["hp"]

        self.multipleHitCounter = 0
        self.stockpile = 0
        self.defenseCurl = False
        self.skyChargingTurn = False
        self.digChargingTurn = False
        self.diveChargingTurn = False
        self.minimize = False

    def init_gender(self):
        if self.femaleRate == -1:
            return "genderless"
        return "female" if random.randint(1, 100) <= self.femaleRate else "male"

    def init_ability(self):
        ability = random.choice(self.abilities)
        return Ability(ability)

    @staticmethod
    def init_nature():
        path = "../assets/data/natures"
        files = os.listdir(path)
        nature = random.choice(files)
        return json.load(open(path + "/" + nature))

    def init_item(self):
        items = []
        for item in self.itemHeld:
            if random.randint(0, 100) < item["chance"]:
                items.append(item["dbSymbol"])
        if items:
            final_item = random.choice(items)
            return Item(final_item)
        return None

    def init_moveset(self):
        moveset = []
        for move in self.movepool:
            if move["klass"] == "LevelLearnableMove":
                if move["level"] <= self.level:
                    if len(moveset) >= 4:
                        moveset.remove(random.choice(moveset))
                    moveset.append(Move(move["move"]))
        return moveset

    def init_stat(self, stat):
        if stat == "hp":
            return math.floor(((self.ivs[stat] + 2 * self.baseStats[stat] + math.floor(self.evs[stat] // 4)) *
                               self.level // 100) + self.level + 10)
        return math.floor((((self.ivs[stat] + 2 * self.baseStats[stat] + math.floor(self.evs[stat] // 4)) *
                            self.level // 100) + 5) * self.nature[stat])

    def get_gender(self):
        return self.gender

    def get_ability(self):
        return self.ability.dbSymbol

    def get_item(self):
        if self.item:
            return self.item.dbSymbol
        return None

    def get_main_status(self):
        return self.status["main"]

    def get_sec_status(self):
        return self.status["sec"]

    def get_stage_stat(self, stat_id, boost_id=None, ignore_boost=False, crit=False):
        if ignore_boost:
            return self.globalStats[stat_id]

        if boost_id is None:
            boost_id = stat_id

        if crit:
            if stat_id in ("atk", "aspe") and self.boosts[stat_id] < 0:
                return self.globalStats[stat_id]
            elif stat_id in ("defe", "dspe") and self.boosts[stat_id] > 0:
                return self.globalStats[stat_id]

        boost_levels = {
            "eva": [3, 8 / 3, 7 / 3, 2, 5 / 3, 4 / 3, 1, 0.75, 0.6, 0.5, 3 / 7, 3 / 8, 1 / 3],
            "acc": [1 / 3, 3 / 8, 3 / 7, 0.5, 0.6, 0.75, 1, 4 / 3, 5 / 3, 2, 7 / 3, 8 / 3, 3],
            "general": [0.25, 2 / 7, 1 / 3, 0.4, 0.5, 2 / 3, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        }
        boost_factor = boost_levels[stat_id if stat_id in ("eva", "acc") else "general"]

        return int(self.globalStats[stat_id] * boost_factor[self.boosts[boost_id] + 6])

    def exp_to_nxt_lvl(self):
        if self.level == 100:
            return 0
        if self.expType == 0:
            return self.level ** 3
        elif self.expType == 1:
            return math.floor((4 * (self.level ** 3)) / 5)
        elif self.expType == 2:
            return 5 * (self.level ** 3) / 4
        elif self.expType == 3:
            return math.floor(((6 / 5) * (self.level ** 3)) - (15 * (self.level ** 2)) + (100 * self.level) - 140)
        elif self.expType == 4:
            if self.level <= 50:
                return math.floor((self.level ** 3) * (100 - self.level) / 50)
            elif self.level <= 68:
                return math.floor((self.level ** 3) * (150 - self.level) / 100)
            elif self.level <= 98:
                return math.floor((self.level ** 3) * math.floor((1911 - 10 * self.level) / 3) / 500)
            elif self.level < 100:
                return math.floor((self.level ** 3) * (160 - self.level) / 100)

    def is_ko(self):
        return not self.currentHp

    def init_mod(self, mod):
        if "gender" in mod:
            self.gender = mod["gender"]

        if "ability" in mod:
            self.ability = Ability(mod["ability"])

        if "item" in mod:
            self.item = Item(mod["item"])

        if "moveset" in mod:
            for move in self.moveset:
                for newmove in mod["moveset"]:
                    if newmove == move.dbSymbol:
                        mod["moveset"].remove(newmove)
            for _ in range(len(mod["moveset"])):
                self.moveset.remove(random.choice(self.moveset))
            for move in mod["moveset"]:
                if move != "":
                    self.moveset.append(Move(move))

        if "ivs" in mod:
            for stat in mod["ivs"]:
                self.ivs[stat] = mod["ivs"][stat]

        if "evs" in mod:
            for stat in mod["evs"]:
                self.evs[stat] = mod["evs"][stat]

        if "nature" in mod:
            self.nature = json.load(open(f"../assets/data/natures/{mod["nature"]}.json"))

        if "status" in mod:
            self.status = mod["status"]

        if "exp" in mod:
            self.exp = mod["exp"]

        if "shiny" in mod:
            self.shiny = mod["shiny"]

        if "hp" in mod:
            self.currentHp = mod["hp"]

    def save_pkmn(self):
        return {
            "UID": self.UID,
            "name": self.name,
            "level": self.level,
            "gender": self.gender,
            "ability": self.ability.dbSymbol,
            "item": self.item.dbSymbol if self.item else None,
            "moveset": [move.save_move() for move in self.moveset],
            "ivs": self.ivs,
            "evs": self.evs,
            "nature": self.nature,
            "status": self.status,
            "exp": self.exp,
            "shiny": self.shiny,
            "currentHp": self.currentHp
        }

    def load_pokemon(self, data):
        self.UID = data["UID"]
        self.gender = data["gender"]
        self.ability = Ability(data["ability"])
        self.item = Item(data["item"]) if data["item"] else None
        self.moveset.clear()
        for d in data["moveset"]:
            M = Move(d["name"])
            M.load_move(d)
            self.moveset.append(M)
        self.ivs = data["ivs"]
        self.evs = data["evs"]
        self.nature = data["nature"]
        self.status = data["status"]
        self.exp = data["exp"]
        self.shiny = data["shiny"]
        self.currentHp = data["currentHp"]

        self.globalStats = {
            "hp": self.init_stat("hp"),
            "atk": self.init_stat("atk"),
            "defe": self.init_stat("defe"),
            "aspe": self.init_stat("aspe"),
            "dspe": self.init_stat("dspe"),
            "spd": self.init_stat("spd")
        }

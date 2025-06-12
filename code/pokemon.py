import math
import random
import json

from data import DATA
from move import Move
from type import Type
from ability import Ability
from item import Item
from modifier import Modifier


class Pokemon:
    def __init__(self, name, level, mod=None):
        data = json.load(open(f"../assets/data/pokemons/{name.lower()}.json"))
        self.forms = data["forms"]

        self.id = data["id"]
        self.name = data["dbSymbol"].title()
        self.height = self.forms[0]["height"]
        self.weight = self.forms[0]["weight"]
        self.shiny = True if random.random() <= 1 / 8192 else False

        self.level = level

        self.gender = self.get_gender()
        self.type = self.get_type()
        self.Ability = self.get_ability()
        self.Item = self.get_item()

        self.movepool = self.forms[0]["moveSet"]
        self.moveset = self.init_moveset()

        self.baseStats = {"hp": self.forms[0]["baseHp"],
                          "atk": self.forms[0]["baseAtk"],
                          "defe": self.forms[0]["baseDfe"],
                          "aspe": self.forms[0]["baseAts"],
                          "dspe": self.forms[0]["baseDfs"],
                          "spd": self.forms[0]["baseSpd"]
                          }

        self.ivs = {"hp": random.randint(0, 31),
                    "atk": random.randint(0, 31),
                    "defe": random.randint(0, 31),
                    "aspe": random.randint(0, 31),
                    "dspe": random.randint(0, 31),
                    "spd": random.randint(0, 31)
                    }

        self.evs = {"hp": self.forms[0]["evHp"],
                    "atk": self.forms[0]["evAtk"],
                    "defe": self.forms[0]["evDfe"],
                    "aspe": self.forms[0]["evAts"],
                    "dspe": self.forms[0]["evDfs"],
                    "spd": self.forms[0]["evSpd"]
                    }

        self.nature = random.choice(tuple(DATA.NATURES.values()))

        self.boosts = {"atk": 0, "defe": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
        self.status = {"main": None, "sec": []}

        self.exp = 0
        self.expType = self.forms[0]["experienceType"]
        self.remainingExp = self.exp_to_nxt_lvl()

        self.catchRate = self.forms[0]["catchRate"]

        self.sprites = {
            "front": self.get_sprite_path("front"),
            "back": self.get_sprite_path("back")
        }
        self.frontOffsetY = self.forms[0]["frontOffsetY"]

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

        self.stageStats = self.globalStats

    def get_gender(self):
        if self.forms[0]["femaleRate"] == -1:
            return "genderless"
        return "female" if random.randint(1, 100) <= self.forms[0]["femaleRate"] else "male"

    def get_type(self):
        if self.forms[0]["type2"] == "__undef__":
            return [Type(self.forms[0]["type1"])]
        return Type(self.forms[0]["type1"]), Type(self.forms[0]["type2"])

    def get_ability(self):
        ability = random.choice(self.forms[0]["abilities"])
        return Ability(ability)

    def get_item(self):
        items = []
        for item in self.forms[0]["itemHeld"]:
            if random.randint(0, 100) < item["chance"]:
                items.append(item["dbSymbol"])
        if items:
            final_item = random.choice(items)
            return Item(final_item)
        return None

    def get_sprite_path(self, direction):
        path = f"../assets/graphics/pokemons/{direction}/"
        if self.shiny:
            path += "shiny/"
            if self.gender == "female" and self.forms[0]["resources"]["hasFemale"]:
                if not self.forms[0]["femaleRate"] == 100:
                    path += "female/"
        elif self.gender == "female" and self.forms[0]["resources"]["hasFemale"]:
            if not self.forms[0]["femaleRate"] == 100:
                path += "female/"

        return path + f"{self.id}.png"

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
            return math.floor(((self.ivs[stat] + 2 * self.baseStats[stat] + math.floor(self.evs[stat] / 4)) *
                               self.level / 100) + self.level + 10)
        return math.floor((((self.ivs[stat] + 2 * self.baseStats[stat] + math.floor(self.evs[stat] / 4)) *
                            self.level / 100) + 5) * self.nature[stat])

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

    def can_attack(self, move: Move):
        if self.status["main"] == "sleep" and move.name != "Sleep Talk":
            return False

        elif self.status["main"] == "freeze":
            return False

        elif self.status["main"] == "paralysis":
            if random.randint(0, 100) <= 25:
                return False

        if "flinch" in self.status["sec"]:
            return False

        if "confusion" in self.status["sec"]:
            if random.randint(0, 100) <= 33:
                return False

        if "attract" in self.status["sec"]:
            if random.randint(0, 100) <= 50:
                return False

        return True

    def check_accuracy(self, move, battle_data):
        target = battle_data["opponent"].get_lead()
        if random.randint(0, 100) >= move.accuracy * self.boosts["acc"] * target.boosts["eva"]:
            return True
        return False

    def calcul_damage(self, move, battle_data):
        target = battle_data["opponent"].get_lead()
        if move.power:
            damage = int((2 * self.level) / 5) + 2

            power = move.power
            attack = self.stageStats["atk"] if move.category == "physical" else self.stageStats["aspe"]
            defense = target.stageStats["defe"] if move.category == "special" else target.stageStats["dspe"]
            damage = int(damage * power * (attack / defense))
            damage = int(damage / 50)

            type = move.type.get_type_ratio(target)
            damage = int(damage * type)

            return damage
        return 0

    def additional_effects(self, move, battle_data):
        target = battle_data["opponent"].get_lead()
        if random.randint(0, 100) <= move.effectChance:
            if move.boosts:
                pkmn = self if move.battleEngineMethod == "s_self_stat" else target
                for stat in move.boosts:
                    pkmn.boosts[stat] += move.boosts[stat]

                    if pkmn.boosts[stat] > 6:
                        pkmn.boosts[stat] = 6
                    elif pkmn.boosts[stat] < -6:
                        pkmn.boosts[stat] = -6

                    if stat == "acc":
                        pkmn.stageStats[stat] = pkmn.globalStats[stat] * DATA.ACC_F_BOOST[pkmn.boosts[stat] + 6]
                    elif stat == "eva":
                        pkmn.stageStats[stat] = pkmn.globalStats[stat] * DATA.EVA_F_BOOST[pkmn.boosts[stat] + 6]
                    else:
                        pkmn.stageStats[stat] = pkmn.globalStats[stat] * DATA.GEN_F_BOOSTS[pkmn.boosts[stat] + 6]

        for status in move.status:
            if status:
                if random.randint(0, 100) <= status["luckRate"]:
                    if status["status"] in ["FROZEN", "PARALYZED", "ASLEEP", "BURN", "TOXIC"]:
                        if not self.status["main"]:
                            self.status["main"] = status["status"]
                    else:
                        if not status["status"] in self.status["sec"]:
                            self.status["sec"].append(status["status"])

    def attack(self, move, battle_data):
        if self.can_attack(move):
            if self.check_accuracy(move, battle_data):
                damage = self.calcul_damage(move, battle_data)
                self.additional_effects(move, battle_data)

    def is_ko(self):
        return not self.stageStats["hp"]

    def get_lead(self):
        return self

    def init_mod(self, mod):
        if "gender" in mod:
            self.gender = mod["gender"]

        if "ability" in mod:
            self.Ability = mod["ability"]

        if "item" in mod:
            self.Item = mod["item"]

        if "moveset" in mod:
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
            self.nature = DATA.NATURES[mod["nature"]]

        if "status" in mod:
            self.status = mod["status"]

        if "exp" in mod:
            self.exp = mod["exp"]

        if "shiny" in mod:
            self.shiny = mod["shiny"]

        if "hp" in mod:
            self.stageStats["hp"] = mod["hp"]

    def save_pkmn(self):
        return {
            "name": self.name,
            "level": self.level,
            "gender": self.gender,
            "ability": self.Ability.dbSymbol,
            "item": self.Item.dbSymbol if self.Item else None,
            "moveset": [move.save_move() for move in self.moveset],
            "ivs": self.ivs,
            "evs": self.evs,
            "nature": self.nature,
            "status": self.status,
            "exp": self.exp,
            "shiny": self.shiny,
            "hp": self.stageStats["hp"]
        }

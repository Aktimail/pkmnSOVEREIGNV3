import os
import math
import random
import json

from move import Move
from type import Type
from ability import Ability
from item import Item


class Pokemon:
    def __init__(self, name, level, mod=None):
        data = json.load(open(f"../assets/data/pokemons/{name.lower()}.json"))
        self.forms = data["forms"]

        self.id = data["id"]
        self.UID = 0
        self.dbSymbol = data["dbSymbol"]
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

        self.nature = self.get_nature()

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

        self.currentHp = self.init_stat("hp")

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

        self.happiness = 0

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

    @staticmethod
    def get_nature():
        path = "../assets/data/natures"
        files = os.listdir(path)
        nature = random.choice(files)
        return json.load(open(path + "/" + nature))

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

        return path + f"{self.id}.png"

    def get_lead(self):
        return self

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

    def get_stage_stat(self, stat):
        boost_factors = json.load(open("../assets/data/other/boostFactors.json"))
        gen_boost = boost_factors["general"]
        eva_boost = boost_factors["evasion"]
        acc_boost = boost_factors["accuracy"]
        if stat == "eva":
            return int(self.globalStats[stat] * eval(eva_boost[self.boosts[stat] + 6]))
        elif stat == "acc":
            return int(self.globalStats[stat] * eval(acc_boost[self.boosts[stat] + 6]))
        else:
            return int(self.globalStats[stat] * eval(gen_boost[self.boosts[stat] + 6]))

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

    def can_attack(self, move, target, context):
        if self.status["main"] == "sleep" and move.dbSymbol != "sleep_talk":
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

        pp_losses = 2 if target.Ability.dbSymbol == "pressure" else 1
        move.pp -= pp_losses
        return True

    def check_accuracy(self, move, target, context):
        if random.randint(0, 100) >= move.accuracy * self.boosts["acc"] * target.boosts["eva"]:
            return True
        return False

    def calcul_damage(self, move: Move, target, context):
        def apply_mod(value, mod):
            return round((value * mod) / 0x1000)

        def chain_up(*mods):
            last = len(mods)
            chained_mod = mods[0]
            for i in range(1, last):
                chained_mod = ((chained_mod * mods[i]) + 0x800) >> 12
            return chained_mod

        CAT = "atk" if move.category == "physical" else "aspe"
        FOULPLAYTRIGGER = True if move.dbSymbol == "foul_play" else False
        STATCLIENT = target if FOULPLAYTRIGGER else self
        UNAWARETRIGGER = True if target.Ability.dbSymbol == "unaware" else False
        STAGEATK = STATCLIENT.globalStats[CAT] if UNAWARETRIGGER else STATCLIENT.get_stage_stat(CAT)
        PARAMATK = STAGEATK
        MODTF = 0x800 if (target.Ability.dbSymbol == "thick_fat" and
                          move.type.dbSymbol in ["ice", "fire"]) else 0x1000
        MODTRNT = 0x1800 if (self.Ability.dbSymbol == "torrent" and
                             self.currentHp <= self.globalStats["hp"] / 3 and
                             move.type.dbSymbol == "water") else 0x1000
        MODGUTS = 0x1800 if (self.Ability.dbSymbol == "guts" and
                             self.status["main"] and
                             move.category == "physical") else 0x1000
        MODSWA = 0x1800 if (self.Ability.dbSymbol == "swarm" and
                            self.currentHp <= self.globalStats["hp"] / 3 and
                            move.type.dbSymbol == "bug") else 0x1000
        MODOVG = 0x1800 if (self.Ability.dbSymbol == "overgrow" and
                            self.currentHp <= self.globalStats["hp"] / 3 and
                            move.type.dbSymbol == "grass") else 0x1000
        MODPLMI = 0x1800 if (self.Ability.dbSymbol in ["plus", "minus"] and
                             context["ally"] and
                             context["ally"].Ability.dbSymbol in ["plus", "minus"] and
                             move.category == "special") else 0x1000
        MODBLZ = 0x1800 if (self.Ability.dbSymbol == "blaze" and
                            self.currentHp <= self.globalStats["hp"] / 3 and
                            move.type.dbSymbol == "fire") else 0x1000
        MODDFT = 0x800 if (self.Ability.dbSymbol == "defeatist" and
                           self.currentHp <= self.globalStats["hp"] / 2) else 0x1000
        MODPHPW = 0x2000 if (self.Ability.dbSymbol in ["pure_power", "huge_power"] and
                             move.category == "physical") else 0x1000
        MODSLRP = 0x1800 if (self.Ability.dbSymbol == "solar_power" and
                             context["wheater"] == "intense_sunlight" and
                             move.category == "special") else 0x1000
        MODHSTL = 0x1800 if (self.Ability.dbSymbol == "hustle" and
                             move.category == "physical") else 0x1000
        MODFLFR = 0x1800 if (self.Ability.dbSymbol == "flash_fire" and
                             self.Ability.active and
                             move.type.dbSymbol == "fire") else 0x1000
        MODSLST = 0x800 if (self.Ability.dbSymbol == "slow_start" and
                            context["onFieldCounter"] < 5) else 0x1000
        MODFLGF = 0x1800 if (context["ally"] and
                             context["ally"].Ability.dbSymbol == "flower_gift" and
                             context["wheater"] == "intense_sunlight" and
                             move.category == "special") else 0x1000
        MODCLUB = 0x2000 if (self.dbSymbol in ["cubone", "marowak"] and
                             self.Item and
                             self.Item.dbSymbol == "thick_club" and
                             move.category == "physical") else 0x1000
        MODDST = 0x2000 if (self.dbSymbol == "clamperl" and
                            self.Item and
                            self.Item.dbSymbol == "deep_sea_tooth" and
                            move.category == "special") else 0x1000
        MODPIKA = 0x2000 if (self.dbSymbol == "pikachu" and
                             self.Item and
                             self.Item.dbSymbol == "light_ball") else 0x1000
        MODLATI = 0x1800 if (self.dbSymbol in ["latios", "latias"] and
                             self.Item and
                             self.Item.dbSymbol == "soul_dew" and
                             move.category == "special") else 0x1000
        MODCHBN = 0x1800 if (self.Item and
                             self.Item.dbSymbol == "choice_band" and
                             move.category == "physical") else 0x1000
        MODCHSP = 0x1800 if (self.Item and
                             self.Item.dbSymbol == "choice_specs" and
                             move.category == "special") else 0x1000
        MODATK1 = chain_up(MODTF, MODTRNT, MODGUTS, MODSWA, MODOVG, MODPLMI, MODBLZ, MODDFT, MODPHPW, MODSLRP)
        ATK = apply_mod(PARAMATK, MODATK1)
        ATK = apply_mod(ATK, MODHSTL)
        MODATK2 = chain_up(MODFLFR, MODSLST, MODFLGF, MODCLUB, MODDST, MODPIKA, MODLATI, MODCHBN, MODCHSP)
        ATK = apply_mod(ATK, MODATK2)

        POWER = move.power
        if move.dbSymbol == "frustration":
            POWER = int(((255 - self.happiness) * 10) / 25)
        elif move.dbSymbol == "payback" and not context["firstToMove"]:
            POWER = 100
        elif move.dbSymbol == "return":
            POWER = int((self.happiness * 10) / 25)
        elif move.dbSymbol == "electro_ball":
            deltaSpeed = self.get_stage_stat("spd") / target.get_stage_stat("spd")
            results = {
                deltaSpeed >= 4: 150,
                4 > deltaSpeed >= 3: 120,
                3 > deltaSpeed >= 2: 80,
                2 > deltaSpeed >= 1: 60,
                deltaSpeed < 1: 40
            }
            POWER = results[True]
        elif move.dbSymbol == "avalanche" and context["gotHit"]:
            POWER = 120
        elif move.dbSymbol == "gyro_ball":
            POWER = int(min(150, 25 * target.get_stage_stat("spd") / self.get_stage_stat("spd")))
        elif move.dbSymbol in ["eruption", "water_spout"]:
            POWER = int((150 * self.currentHp) / self.globalStats["hp"])
        elif move.dbSymbol == "punishment":
            boostlvltotal = sum(val for val in target.boosts.values() if val >= 0)
            POWER = min(120, 60 + 20 * boostlvltotal)
        elif move.dbSymbol == "fury_cutter":
            succes_streak = 0
            for i in range(len(context["selfMovesLogs"])-1, len(context["selfMovesLogs"])-4, -1):
                if context["selfMovesLogs"]["move"] == "fury_cutter" and context["selfMovesLogs"]["hit"]:
                    succes_streak += 1
            POWER = 20 * 2 ** succes_streak
        elif move.dbSymbol in ["low_kick", "grass_knot"]:
            w = target.weight
            result = {
                w >= 200: 120,
                200 > w >= 100: 100,
                100 > w >= 50: 80,
                50 > w >= 25: 60,
                25 > w >= 10: 40,
                10 > w: 20
            }
            POWER = result[True]
        elif move.dbSymbol == "echoed_voice":
            use_streak = 0
            for i in range(len(context["teamMovesLogs"]) - 1, len(context["teamMovesLogs"]) - 6, -1):
                if context["teamMovesLogs"]["move"] == "echoed_voice":
                    use_streak += 1
            result = [40, 80, 120, 160, 200]
            POWER = result[use_streak]
        elif move.dbSymbol == "hex" and target.status["main"]:
            POWER = 100

        return 0

    def additional_effects(self, move, target, context):
        if random.randint(0, 100) <= move.effectChance:
            if move.boosts:
                pkmn = self if move.battleEngineMethod == "s_self_stat" else target
                for stat in move.boosts:
                    pkmn.boosts[stat] += move.boosts[stat]

                    if pkmn.boosts[stat] > 6:
                        pkmn.boosts[stat] = 6
                    elif pkmn.boosts[stat] < -6:
                        pkmn.boosts[stat] = -6

        for status in move.status:
            if status:
                if random.randint(0, 100) <= status["luckRate"]:
                    if status["status"] in ["FROZEN", "PARALYZED", "ASLEEP", "BURN", "TOXIC"]:
                        if not self.status["main"]:
                            self.status["main"] = status["status"]
                    else:
                        if not status["status"] in self.status["sec"]:
                            self.status["sec"].append(status["status"])

    def attack(self, move, target, context):

        if self.can_attack(move, target, context):
            if self.check_accuracy(move, target, context):

                if move.power:
                    damage = self.calcul_damage(move, target, context)
                    target.currentHp -= damage
                    if target.currentHp < 0:
                        target.currentHp = 0

                self.additional_effects(move, target, context)

    def is_ko(self):
        return not self.currentHp

    def init_mod(self, mod):
        if "gender" in mod:
            self.gender = mod["gender"]

        if "ability" in mod:
            self.Ability = Ability(mod["ability"])

        if "item" in mod:
            self.Item = Item(mod["item"])

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
            "hp": self.currentHp
        }

    def load_pokemon(self, data):
        self.gender = data["gender"]
        self.Ability = Ability(data["ability"])
        self.Item = Item(data["item"]) if data["item"] else None
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
        self.currentHp = data["hp"]

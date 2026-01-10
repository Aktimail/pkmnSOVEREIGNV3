import os
import math
import random
import json
import uuid

from move import Move
from type import Type
from ability import Ability
from item import Item


class Pokemon:
    def __init__(self, name, level, mod=None):
        data = json.load(open(f"../assets/data/pokemons/{name.lower()}.json"))
        self.forms = data["forms"]

        self.UID = uuid.uuid4().hex
        self.id = data["id"]
        self.dbSymbol = data["dbSymbol"]
        self.name = data["dbSymbol"].title()
        self.height = self.forms[0]["height"]
        self.weight = self.forms[0]["weight"]
        self.shiny = True if random.random() <= 1 / 8192 else False

        self.level = level

        self.gender = self.init_gender()
        self.type = self.init_type()
        self.Ability = self.init_ability()
        self.Item = self.init_item()

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

        self.nature = self.init_nature()

        self.boosts = {"atk": 0, "defe": 0, "aspe": 0, "dspe": 0, "spd": 0, "acc": 0, "eva": 0}
        self.status = {"main": None, "sec": []}

        self.exp = 0
        self.expType = self.forms[0]["experienceType"]
        self.remainingExp = self.exp_to_nxt_lvl()
        self.evolution = self.forms[0]["evolutions"]

        self.catchRate = self.forms[0]["catchRate"]

        self.sprites = {
            "front": self.get_sprite_path("front"),
            "back": self.get_sprite_path("back")
        }
        self.frontOffsetY = self.forms[0]["frontOffsetY"]

        self.currentHp = self.init_stat("hp")

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

    def init_gender(self):
        if self.forms[0]["femaleRate"] == -1:
            return "genderless"
        return "female" if random.randint(1, 100) <= self.forms[0]["femaleRate"] else "male"

    def init_type(self):
        if self.forms[0]["type2"] == "__undef__":
            return [Type(self.forms[0]["type1"])]
        return Type(self.forms[0]["type1"]), Type(self.forms[0]["type2"])

    def init_ability(self):
        ability = random.choice(self.forms[0]["abilities"])
        return Ability(ability)

    @staticmethod
    def init_nature():
        path = "../assets/data/natures"
        files = os.listdir(path)
        nature = random.choice(files)
        return json.load(open(path + "/" + nature))

    def init_item(self):
        items = []
        for item in self.forms[0]["itemHeld"]:
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

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_ability(self):
        return self.Ability.dbSymbol

    def get_item(self):
        if self.Item:
            return self.Item.dbSymbol
        return None

    def get_type(self):
        return [t.dbSymbol for t in self.type]

    def get_main_status(self):
        return self.status["main"]

    def get_sec_status(self):
        return self.status["sec"]

    def get_stage_stat(self, stat, ignore_boost=False, crit=False):
        if ignore_boost:
            return self.globalStats[stat]

        if crit:
            if stat == "atk" or stat == "aspe":
                if self.boosts[stat] < 0:
                    return self.globalStats[stat]
            elif stat == "defe" or stat == "dspe":
                if self.boosts[stat] > 0:
                    return self.globalStats[stat]

        boost_levels = {
            "eva": [3, 8 / 3, 7 / 3, 2, 5 / 3, 4 / 3, 1, 0.75, 0.6, 0.5, 3 / 7, 3 / 8, 1 / 3],
            "acc": [1 / 3, 3 / 8, 3 / 7, 0.5, 0.6, 0.75, 1, 4 / 3, 5 / 3, 2, 7 / 3, 8 / 3, 3],
            "general": [0.25, 2 / 7, 1 / 3, 0.4, 0.5, 2 / 3, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        }
        return int(
            self.globalStats[stat] *
            boost_levels[stat if stat == "eva" or stat == "acc" else "general"][self.boosts[stat] + 6]
        )

    def get_sprite_path(self, direction):
        path = f"../assets/graphics/pokemons/{direction}/"
        if self.shiny:
            path += "shiny/"
        if self.gender == "female" and self.forms[0]["resources"]["hasFemale"]:
            if not self.forms[0]["femaleRate"] == 100:
                path += "female/"

        return path + f"{self.id}.png"

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

    def can_attack(self, move, target, battle_data):
        if self.status["main"] == "asleep" and move.dbSymbol != "sleep_talk":
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

    def check_accuracy(self, move, target, battle_data):
        if random.randint(0, 100) >= move.accuracy * self.boosts["acc"] * target.boosts["eva"]:
            return True
        return False

    def calcul_damage(self, move: Move, target, battle_data):
        berries = json.load(open("../assets/data/other/berriesTable.json"))
        plates = json.load(open("../assets/data/other/platesTable.json"))
        gems = json.load(open("../assets/data/other/gemsTable.json"))
        incenses = json.load(open("../assets/data/other/typeEnhancingIncences.json"))
        items = json.load(open("../assets/data/other/typeEnhancingItems.json"))
        sheerforce_moves = json.load(open("../assets/data/other/sheerForceTable.json"))

        def apply_mod(value, mod):
            return round((value * mod) / 0x1000)

        def chain_up(*mods):
            chained_mod = 0X1000
            for mod in mods:
                chained_mod = ((chained_mod * mod) + 0x800) >> 12
            return chained_mod

        ATK = 0
        DEFE = 0
        POWER = 0
        CRIT = False
        R = random.randint(0, 15)
        STAB = False
        TYPEEFFECTIVENESS = move.type.get_type_ratio(target)
        DAMAGE = 0

        if move.dbSymbol == "psywave":
            DAMAGE = int(max(1, ((random.randint(0, 101) + 50) * self.level) / 100))
        elif move.dbSymbol == "night_shade":
            DAMAGE = self.level
        elif move.dbSymbol == "sonicboom":
            DAMAGE = 20
        elif move.dbSymbol == "super_fang":
            DAMAGE = int(max(1, target.currentHp / 2))

        elif move.dbSymbol == "dragon_rage":
            DAMAGE = 40
        elif move.dbSymbol == "endeavor":
            DAMAGE = (0, target.currentHp - self.currentHp)
        elif move.dbSymbol == "final_gambit":
            DAMAGE = self.currentHp
        elif move.dbSymbol == "brick_break":
            if battle_data["targetLightScreen"]:
                battle_data["targetLightScreen"] = False
            if battle_data["targetReflect"]:
                battle_data["targetReflect"] = False
        elif move.dbSymbol == "counter":
            if battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["action"] == "fight":
                if battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["move"].category == "physical":
                    DAMAGE = battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["damage"] * 2
        elif move.dbSymbol == "mirror_coat":
            if battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["action"] == "fight":
                if battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["move"].category == "special":
                    DAMAGE = battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["damage"] * 2
        elif move.dbSymbol == "metal_burst":
            if battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["action"] == "fight":
                    DAMAGE = battle_data["logs"][battle_data["nb_round"]][battle_data["target"]]["damage"] * 1,5
        elif move.dbSymbol == "bide":
            DAMAGE = 0 * 2
        else:

            ATKCAT = "atk" if move.category == "physical" else "aspe"
            ATKSTATUSER = self if not move.dbSymbol == "foul_play" else target
            PARAMATK = ATKSTATUSER.get_stage_stat(ATKCAT) if not target.Ability.dbSymbol == "unaware" \
                else ATKSTATUSER.globalStats[ATKCAT]
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
                                 battle_data["selfAlly"] and
                                 battle_data["selfAlly"].Ability.dbSymbol in ["plus", "minus"] and
                                 move.category == "special") else 0x1000
            MODBLZ = 0x1800 if (self.Ability.dbSymbol == "blaze" and
                                self.currentHp <= self.globalStats["hp"] / 3 and
                                move.type.dbSymbol == "fire") else 0x1000
            MODDFT = 0x800 if (self.Ability.dbSymbol == "defeatist" and
                               self.currentHp <= self.globalStats["hp"] / 2) else 0x1000
            MODPHPW = 0x2000 if (self.Ability.dbSymbol in ["pure_power", "huge_power"] and
                                 move.category == "physical") else 0x1000
            MODSLRP = 0x1800 if (self.Ability.dbSymbol == "solar_power" and
                                 battle_data["weather"] == "intense_sunlight" and
                                 move.category == "special") else 0x1000
            MODHSTL = 0x1800 if (self.Ability.dbSymbol == "hustle" and
                                 move.category == "physical") else 0x1000
            MODFLFR = 0x1800 if (self.Ability.dbSymbol == "flash_fire" and
                                 self.Ability.active and
                                 move.type.dbSymbol == "fire") else 0x1000
            MODSLST = 0x800 if (self.Ability.dbSymbol == "slow_start" and
                                battle_data["onFieldCounter"] < 5) else 0x1000
            MODFLGF = 0x1800 if (battle_data["selfAlly"] and
                                 battle_data["selfAlly"].Ability.dbSymbol == "flower_gift" and
                                 battle_data["wheater"] == "intense_sunlight" and
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

            DEFECAT = "defe" if move.category == "physical" else "dspe"
            if move.dbSymbol in ["psyshock", "psystrike", "secret_sword"]:
                DEFECAT = "defe"
            if battle_data["fieldStatus"] == "wonderRoom":
                if move.category == "physical":
                    DEFECAT = "dspe"
                elif move.category == "special":
                    DEFECAT = "defe"
            PARAMDEFE = target.get_stage_stat(DEFECAT)
            if self.Ability.dbSymbol == "unaware":
                PARAMDEFE = target.globalStats[DEFECAT]
            elif move.dbSymbol == "chip_away":
                PARAMDEFE = target.globalStats[DEFECAT]
            if battle_data["weather"] == "sandstorm" and self.type.count(Type("rock")) and ATKCAT == "special":
                PARAMDEFE = apply_mod(PARAMDEFE, 0x1800)
            MODMRVL = 0x1800 if (target.Ability.dbSymbol == "marvel_scale" and
                                 target.status["main"] and
                                 move.category == "special") else 0x1000
            MODTGFG = 0x1800 if (battle_data["selfAlly"] and
                                 battle_data["selfAlly"].dbSymbol == "cherrim" and
                                 battle_data["selfAlly"].Ability.dbSymbol == "flower_gift" and
                                 battle_data["weather"] == "Harsh_sunlight" and
                                 move.category == "special") else 0x1000
            MODDSS = 0x1800 if (target.dbSymbol == "clamperl" and
                                target.Item and
                                target.Item.dbSymbol == "deep_sea_scale" and
                                move.category == "special") else 0x1000
            MODDTTO = 0x2000 if (target.dbSymbol == "ditto" and
                                 not target.Ability.active and
                                 target.Item and
                                 target.Item.dbSymbol == "metal_powder" and
                                 move.category == "physical") else 0x1000
            MODEVIO = 0x1800 if (target.Item and
                                 target.Item.dbSymbol == "eviolite" and
                                 target.evolution) else 0x1000
            MODTGLA = 0x1800 if (target.dbSymbol in ["latios", "latias"] and
                                 target.Item and
                                 target.Item.dbSymbol == "soul_dew" and
                                 move.category == "special") else 0x1000
            MODDEFE = chain_up(MODMRVL, MODTGFG, MODDSS, MODDTTO, MODEVIO, MODTGLA)
            DEFE = apply_mod(PARAMDEFE, MODDEFE)

            BASEPOWER = move.basePower
            if move.dbSymbol == "frustration":
                BASEPOWER = int(((255 - self.happiness) * 10) / 25)
            elif move.dbSymbol == "payback" and not battle_data["firstToMove"]:
                BASEPOWER = 100
            elif move.dbSymbol == "return":
                BASEPOWER = int((self.happiness * 10) / 25)
            elif move.dbSymbol == "electro_ball":
                deltaSpeed = self.get_stage_stat("spd") / target.get_stage_stat("spd")
                results = {
                    deltaSpeed >= 4: 150,
                    4 > deltaSpeed >= 3: 120,
                    3 > deltaSpeed >= 2: 80,
                    2 > deltaSpeed >= 1: 60,
                    deltaSpeed < 1: 40
                }
                BASEPOWER = results[True]
            elif move.dbSymbol == "avalanche" and battle_data["gotHit"]:
                BASEPOWER = 120
            elif move.dbSymbol == "gyro_ball":
                BASEPOWER = int(min(150, 25 * target.get_stage_stat("spd") / self.get_stage_stat("spd")))
            elif move.dbSymbol in ["eruption", "water_spout"]:
                BASEPOWER = int((150 * self.currentHp) / self.globalStats["hp"])
            elif move.dbSymbol == "punishment":
                sumboostlvl = sum(val for val in target.boosts.values() if val >= 0)
                BASEPOWER = min(120, 60 + 20 * sumboostlvl)
            elif move.dbSymbol == "fury_cutter":
                succes_streak = 0
                for i in range(len(battle_data["selfMovesLogs"]) - 1, len(battle_data["selfMovesLogs"]) - 4, -1):
                    if battle_data["selfMovesLogs"][i]["move"] == "fury_cutter" and battle_data["selfMovesLogs"][i]["hit"]:
                        succes_streak += 1
                    else:
                        break
                BASEPOWER = 20 * 2 ** succes_streak
            elif move.dbSymbol in ["low_kick", "grass_knot"]:
                weight = target.init_weight()
                result = {
                    weight >= 200: 120,
                    200 > weight >= 100: 100,
                    100 > weight >= 50: 80,
                    50 > weight >= 25: 60,
                    25 > weight >= 10: 40,
                    10 > weight: 20
                }
                BASEPOWER = result[True]
            elif move.dbSymbol == "echoed_voice":
                use_streak = 0
                for i in range(len(battle_data["teamMovesLogs"]) - 1, len(battle_data["teamMovesLogs"]) - 6, -1):
                    if battle_data["teamMovesLogs"][i]["move"] == "echoed_voice":
                        use_streak += 1
                    else:
                        break
                result = [40, 80, 120, 160, 200]
                BASEPOWER = result[use_streak]
            elif move.dbSymbol == "hex" and target.status["main"]:
                BASEPOWER = 100
            elif move.dbSymbol in ["wring_out", "crush_grip"]:
                BASEPOWER = int(120 * (target.currentHp / target.globalStats["hp"]))
            elif move.dbSymbol == "assurance" and battle_data["targetGotHit"]:
                BASEPOWER = 100
            elif move.dbSymbol in ["heavy_slam", "heat_crash"]:
                weight = self.get_weight() / target.get_weight()
                result = {
                    weight >= 5: 120,
                    5 > weight >= 4: 100,
                    4 > weight >= 3: 80,
                    3 > weight >= 2: 60,
                    2 > weight: 40
                }
                BASEPOWER = result[True]
            elif move.dbSymbol == "stored_power":
                sumboostlvl = sum(val for val in self.boosts.values() if val >= 0)
                BASEPOWER = 20 + 20 * sumboostlvl
            elif move.dbSymbol == "acrobatics" and not self.Item:
                BASEPOWER = 110
            elif move.dbSymbol in ["flail", "reversal"]:
                p = (48 * self.currentHp) / self.globalStats["hp"]
                result = {
                    p <= 1: 200,
                    2 <= p <= 4: 150,
                    5 <= p <= 9: 100,
                    10 <= p <= 16: 80,
                    17 <= p <= 32: 40,
                    33 <= p: 20
                }
                BASEPOWER = result[True]
            elif move.dbSymbol == "trump_card":
                result = {
                    move.pp == 5: 40,
                    move.pp == 4: 50,
                    move.pp == 3: 60,
                    move.pp == 2: 80,
                    move.pp == 1: 200
                }
                BASEPOWER = result[True]
            elif move.dbSymbol == "round" and battle_data["selfAlly"] and battle_data["allyJustUsedRound"]:
                BASEPOWER = 120
            elif move.dbSymbol == "triple_kick" and "trileKickStreak" in battle_data:
                BASEPOWER = move.basePower * battle_data["trileKickStreak"]
            elif move.dbSymbol == "wake_up_slap" and target.status["main"] == "asleep":
                BASEPOWER = 120
            elif move.dbSymbol == "smelling_salts" and target.status["main"] == "paralysis":
                BASEPOWER = 120
            elif move.dbSymbol == "weather_ball" and battle_data["weather"]:
                BASEPOWER = 100
            elif move.dbSymbol in ["guts", "twister"] and battle_data["targetInSky"]:
                BASEPOWER = 80
            elif move.dbSymbol == "beat_up":
                totalatk = [pkmn.baseStats["atk"]
                            for pkmn in battle_data["selfTrainer"].team
                            if not pkmn.status["main"] or not pkmn.is_ko()]
                BASEPOWER = int(sum(totalatk) / 10 + 5)
            elif move.dbSymbol == "hidden_power":
                ivs_value = 0
                i = 0
                for iv in self.ivs.values():
                    ivs_value += ((iv >> 1) & 1) << i
                    i += 1
                BASEPOWER = int(30 + (40 * ivs_value) / 63)
            elif move.dbSymbol == "spit_up":
                BASEPOWER = 100 * battle_data["selfSpitUpCounter"]
            elif move.dbSymbol == "pursuit" and battle_data["targetSwitch"]:
                BASEPOWER = 80
            elif move.dbSymbol == "present":
                r = random.randint(0, 80)
                result = {
                    r < 40: 40,
                    40 <= r < 70: 80,
                    r >= 70: 120
                }
                BASEPOWER = result[True]
            elif move.dbSymbol == "natural_gift":
                if self.Item and self.Item.dbSymbol in berries:
                    BASEPOWER = berries[self.Item.dbSymbol]["naturalGiftPower"]
            elif move.dbSymbol == "magnitude":
                r = random.randint(0, 100)
                result = {
                    r < 5: 0,
                    5 <= r < 15: 1,
                    15 <= r < 35: 2,
                    35 <= r < 65: 3,
                    65 <= r < 85: 4,
                    85 <= r < 95: 5,
                    95 <= r: 7
                }
                BASEPOWER = 10 + 20 * result[True]
            elif move.dbSymbol == "rollout":
                rollout_succes_streak = 0
                for i in range(len(battle_data["selfMovesLogs"]) - 1, len(battle_data["selfMovesLogs"]) - 6, -1):
                    if battle_data["selfMovesLogs"][i]["move"] == "rollout" and battle_data["selfMovesLogs"][i]["hit"]:
                        rollout_succes_streak += 1
                    else:
                        break
                defense_curl = 0
                for move in battle_data["selfMovesLogs"]:
                    if move["move"] == "defense_curl":
                        defense_curl = 1
                BASEPOWER = 30 * 2 ** (rollout_succes_streak + defense_curl)
            elif move.dbSymbol == "fling" and self.Item:
                BASEPOWER = self.Item.flingPower
            elif (move.dbSymbol in ["grass_pledge", "fire_pledge", "water_pledge"] and
                  battle_data["selfAllyMove"].dbSymbol in ["grass_pledge", "fire_pledge", "water_pledge"] and
                  battle_data["selfAllyHasPlayed"]):
                BASEPOWER = 150
            MODTECH = 0x1800 if (self.Ability.dbSymbol == "technician" and
                                 move.basePower <= 60) else 0x1000
            MODFBST = 0x1800 if (self.Ability.dbSymbol == "flare_boost" and
                                 self.status["main"] == "burn" and
                                 move.category == "special") else 0x1000
            MODANLT = 0x14CD if (self.Ability.dbSymbol == "analytic" and
                                 move.dbSymbol not in ["future_sight", "doom_desire"] and
                                 not battle_data["firstToPlay"]) else 0x1000
            MODRCKL = 0x1333 if (self.Ability.dbSymbol == "reckless" and
                                 (move.battleModifier == "s_recoil" or
                                  move.dbSymbol in ["jump_kick", "high_jump_kick"])) else 0x1000
            MODIFST = 0x1333 if (self.Ability.dbSymbol == "iron_fist" and
                                 move.flags["isPunch"]) else 0x1000
            MODTBST = 0x1800 if (self.Ability.dbSymbol == "toxic_boost" and
                                 self.status["main"] in ["poison", "badly_poisoned"] and
                                 move.category == "physical") else 0x1000
            MODRVLY = 0x1000
            if self.Ability.dbSymbol == "rivalry":
                if not self.gender == "genderless" and not target.gender == "genderless":
                    if self.gender == target.gender:
                        MODRVLY = 0x1400
                    elif self.gender != target.gender:
                        MODRVLY = 0xC00
            MODSNDF = 0x14CD if (self.Ability.dbSymbol == "sand_force" and
                                 move.type.dbSymbol in ["rock", "ground", "steel"]) else 0x1000
            MODHTPR = 0x800 if (self.Ability.dbSymbol == "heatproof" and
                                move.type.dbSymbol == "fire") else 0x1000
            MODDRYS = 0x1400 if (self.Ability.dbSymbol == "dry_skin" and
                                 move.type.dbSymbol == "fire") else 0x1000
            MODSHRF = 0x14CD if (self.Ability.dbSymbol == "sheer_force" and
                                 move.dbSymbol in sheerforce_moves) else 0x1000
            MODTYBS = 0x1333 if (self.Item and
                                 self.Item.dbSymbol in plates and
                                 move.type.dbSymbol == plates[self.Item.dbSymbol]) or \
                                (self.Item and
                                 self.Item.dbSymbol in incenses and
                                 move.type.dbSymbol == incenses[self.Item.dbSymbol]) or \
                                (self.Item and
                                 self.Item.dbSymbol in items and
                                 move.type.dbSymbol == items[self.Item.dbSymbol]) else 0x1000
            MODMBND = 0x1199 if (self.Item and
                                 self.Item.dbSymbol == "muscle_band" and
                                 move.category == "physical") else 0x1000
            MODPLK = 0x1333 if (self.dbSymbol == "palkia" and
                                self.Item and
                                self.Item.dbSymbol == "lustrous_orb" and
                                move.type.dbSymbol in ["water", "dragon"]) else 0x1000
            MODWGLS = 0x1199 if (self.Item and
                                 self.Item.dbSymbol == "wise_glasses" and
                                 move.category == "special") else 0x1000
            MODGRTN = 0x1333 if (self.dbSymbol == "giratina" and
                                 self.Item and
                                 self.Item.dbSymbol == "griseous_orb" and
                                 move.type.dbSymbol in ["ghost", "dragon"]) else 0x1000
            MODOINS = 0x1333 if (self.Item and
                                 self.Item.dbSymbol == "odd_incense" and
                                 move.type.dbSymbol == "psychic") else 0x1000
            MODDLG = 0x1333 if (self.dbSymbol == "dialga" and
                                self.Item and
                                self.Item.dbSymbol == "adamant_orb" and
                                move.type.dbSymbol in ["steel", "dragon"]) else 0x1000
            MODGEMS = 0x1800 if (self.Item and
                                 self.Item.dbSymbol in gems and
                                 move.type.dbSymbol == gems[self.Item.dbSymbol]) else 0x1000
            MODFCD = 0x2000 if (move.dbSymbol == "facade" and
                                self.status["main"] in ["paralysis", "poison", "badly_poisoned", "burn"]) else 0x1000
            MODBRN = 0x2000 if (move.dbSymbol == "brine" and
                                target.currentHp <= target.globalStats["hp"]) else 0x1000
            MODVENO = 0x2000 if (move.dbSymbol == "venoshock" and
                                 target.status["main"] in ["poison", "badly_poisoned"]) else 0x1000
            MODRETAL = 0x2000 if (move.dbSymbol == "retaliate" and
                                  battle_data["targetJustFainted"]) else 0x1000
            MODFUSIO = 0x2000 if (move.dbSymbol in ["fusion_bolt", "fusion_flare"] and
                                  battle_data["selfMovesLogs"][-1]["move"] == move.dbSymbol) else 0x1000
            MODFRST = 0x1800 if battle_data["moveUsedByMeFirst"] else 0x1000
            MODSLRB = 0x800 if (move.dbSymbol == "solar_beam" and
                                battle_data["weather"] and
                                battle_data["weather"] not in ["harsh_sunlight", "extremely_harsh_sunlight"]) else 0x1000
            MODCHRG = 0x2000 if (battle_data["selfMovesLogs"] and
                                 battle_data["selfMovesLogs"][-1]["move"] == "charge" and
                                 move.type.dbSymbol == "electric") else 0x1000
            MODHH = 0x1800 if battle_data["selfHelpingHand"] else 0x1000
            MODWTRS = 0x548 if (({"move": "water_sport", "hit": True} in battle_data["selfMovesLogs"] or
                                 {"move": "water_sport", "hit": True} in battle_data["targetMovesLogs"]) and
                                move.type.dbSymbol == "fire") else 0x1000
            MODMUDS = 0x548 if (({"move": "mud_sport", "hit": True} in battle_data["selfMovesLogs"] or
                                 {"move": "mud_sport", "hit": True} in battle_data["targetMovesLogs"]) and
                                move.type.dbSymbol == "electric") else 0x1000
            MODPOWER = chain_up(MODTECH, MODFBST, MODANLT, MODRCKL, MODIFST, MODTBST, MODRVLY, MODSNDF, MODHTPR,
                                MODDRYS, MODSHRF, MODTYBS, MODMBND, MODPLK, MODWGLS, MODGRTN, MODOINS, MODDLG, MODGEMS,
                                MODFCD, MODBRN, MODVENO, MODRETAL, MODFUSIO, MODFRST, MODSLRB, MODCHRG, MODHH, MODWTRS,
                                MODMUDS)
            POWER = apply_mod(BASEPOWER, MODPOWER)

            PARAMDAMAGE = int(((((2 * self.level) / 5 + 2) * POWER * ATK) / DEFE) / 50 + 2)

            if battle_data["weather"] == "rain":
                if move.type.count(Type("water")):
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, 0x1800)
                elif move.type.count(Type("fire")):
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, 0x800)
            elif battle_data["weather"] in ["harsh_sunlight", "extremely_harsh_sunlight"]:
                if move.type.count(Type("water")):
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, 0x800)
                elif move.type.count(Type("fire")):
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, 0x1800)

            if not target.Ability.dbSymbol in ["battle_armor","shell_armor"] or battle_data["selfLuckyChant"]:
                critical_hit_factors = [1/16, 1/8, 1/4, 1/3, 1/2]
                critical_rate = move.criticalRate
                if self.Ability.dbSymbol == "super_luck":
                    critical_rate += 1
                if self.dbSymbol == "Farfetch_d" and self.Item and self.Item.dbSymbol == "leek":
                    critical_rate += 2
                elif self.dbSymbol == "chansey" and self.Item and self.Item.dbSymbol == "lucky_punch":
                    critical_rate += 2
                if self.Item and self.Item.dbSymbol == "razor_claw":
                    critical_rate += 1
                if random.random() <= critical_hit_factors[critical_rate-1]:
                    CRIT = True
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, 0X2000)

            PARAMDAMAGE = int((PARAMDAMAGE * (100 - R)) / 100)

            MODSTAB = 0x1800
            if self.Ability.dbSymbol == "adaptability":
                MODSTAB = 0x2000
            for t in self.type:
                if move.type.dbSymbol == t.dbSymbol:
                    STAB = True
                    PARAMDAMAGE = apply_mod(PARAMDAMAGE, MODSTAB)

            if TYPEEFFECTIVENESS:
                if TYPEEFFECTIVENESS > 0:
                    PARAMDAMAGE = PARAMDAMAGE<<abs(TYPEEFFECTIVENESS)
                elif TYPEEFFECTIVENESS < 0:
                    PARAMDAMAGE = PARAMDAMAGE>>abs(TYPEEFFECTIVENESS)

            if move.category == "physical" and self.status["main"] == "burn" and self.Ability.dbSymbol != "guts":
                PARAMDAMAGE = PARAMDAMAGE>>1

            MODRFLCT = 0x800 if (battle_data["targetReflect"] and move.category == "physical" and
                    self.Ability.dbSymbol != "Infiltrator" and not CRIT) else 0x1000

            MODLGTSCRN = 0x800 if (battle_data["targetLightScreen"] and move.category == "special" and
                    self.Ability.dbSymbol != "Infiltrator" and not CRIT) else 0x1000

            MODMLTSCL = 0x800 if target.Ability.dbSymbol == "multiscale" and target.currentHp == target.globalStats["hp"] \
                else 0x1000

            MODTNTD = 0x2000 if self.Ability.dbSymbol == "tinted" and TYPEEFFECTIVENESS < 0 else 0x1000

            MODSNPR = 0x1800 if self.Ability.dbSymbol == "sniper" and CRIT else 0x1000

            MODSLDFLTR = 0xC00 if target.Ability.dbSymbol in ["solid_rock", "filter"] and TYPEEFFECTIVENESS > 0 else 0x1000

            MODMTRNM = 0x1000
            n = 0
            for i in range(len(battle_data["selfMovesLogs"])-1, 0, -1):
                if battle_data["selfMovesLogs"][i]["move"] == move.dbSymbol and battle_data["selfMovesLogs"][i]["hit"]:
                    n += 1
                else:
                    break
            if n <= 4:
                MODMTRNM = 0x1000 + n * 0x333
            elif n > 4:
                MODMTRNM = 0x2000

            MODXPRTBLT = 0x1333 if self.Item and self.Item.dbSymbol == "expert_belt" and TYPEEFFECTIVENESS > 0 else 0x1000

            MODLFORB = 0x14CC if self.Item and self.Item.dbSymbol == "life_orb" else 0x1000

            MODBRY = 0x1000
            if TYPEEFFECTIVENESS > 0:
                if target.Item and target.Item.dbSymbol in berries:
                    if berries[target.Item.dbSymbol]["damageLoweringType"]:
                        if move.type == berries[target.Item.dbSymbol]["type"]:
                            MODBRY = 0x800

            MODSTMP = 0x2000 if move.dbSymbol == "stomp" and battle_data["targetMinimize"] else 0x1000

            MODRTHQK = 0x2000 if move.dbSymbol == "earthquake" and battle_data["targetChargingDig"] else 0x1000

            MODSRF = 0x2000 if move.dbSymbol == "surf" and battle_data["targetChargingDive"] else 0x1000

            MODSTMRLR = 0x2000 if move.dbSymbol == "steamroller" and battle_data["targetMinimize"] else 0x1000

            LASTMOD = chain_up(MODRFLCT, MODLGTSCRN, MODMLTSCL, MODTNTD, MODSNPR, MODSLDFLTR, MODMTRNM, MODXPRTBLT,
                               MODLFORB, MODBRY, MODSTMP, MODRTHQK, MODSRF, MODSTMRLR)

            DAMAGE = apply_mod(PARAMDAMAGE, LASTMOD)

        print("power " + str(POWER))
        print("atk " + str(ATK))
        print("defe " + str(DEFE))
        print("crit " + str(CRIT))
        print("R " + str(R))
        print("STAB " + str(STAB))
        print("type effectiveness " + str(TYPEEFFECTIVENESS))
        print()
        print("damage " + str(DAMAGE))

        return DAMAGE


    def additional_effects(self, move, target, battle_data):
        if random.randint(0, 100) <= move.effectChance:
            if move.boosts:
                pkmn = self if move.battleModifier == "s_self_stat" else target
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

    def attack(self, move, target, battle_data):

        if self.can_attack(move, target, battle_data):
            if self.check_accuracy(move, target, battle_data):

                if move.category != "status":
                    damage = self.calcul_damage(move, target, battle_data)
                    target.currentHp -= damage
                    if target.currentHp < 0:
                        target.currentHp = 0

                self.additional_effects(move, target, battle_data)

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
            "ability": self.Ability.dbSymbol,
            "item": self.Item.dbSymbol if self.Item else None,
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
        self.currentHp = data["currentHp"]

        self.globalStats = {
            "hp": self.init_stat("hp"),
            "atk": self.init_stat("atk"),
            "defe": self.init_stat("defe"),
            "aspe": self.init_stat("aspe"),
            "dspe": self.init_stat("dspe"),
            "spd": self.init_stat("spd")
        }


"""P1 = Pokemon("haxorus", 50, mod={"ivs": {"atk": 31, "defe": 31, "aspe": 31, "dspe": 31, "spd": 31},
                                        "nature": "adamant", "ability": "rivalry", "gender": "male", "item": "life_orb"})
P2 = Pokemon("garchomp", 50, mod={"ivs": {"atk": 31, "defe": 31, "aspe": 31, "dspe": 31, "spd": 31},
                                      "nature": "hardy", "gender": "male"})
P1.calcul_damage(Move("dragon_claw"), P2, {
            "selfMovesLogs": [],
            "teamMovesLogs": [],
            "targetMovesLogs": [],
            "selfAlly": None,
            "weather": None,
            "onFieldCounter": 0,
            "moveUsedByMeFirst": False,
            "targetJustFainted": False,
            "selfHelpingHand": False,
            "fieldStatus": None,
            "targetGotHit": False,
            "targetReflect": False,
            "targetLightScreen": False
        })"""

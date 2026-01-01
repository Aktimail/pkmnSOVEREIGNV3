import random
import json


class DamageCalculator:
    def __init__(self, pkmn1, pkmn2, move, battle_data):
        self.pkmn1 = pkmn1
        self.pkmn2 = pkmn2
        self.move = move
        self.battleData = battle_data

        self.berries = json.load(open("../../assets/data/other/berriesTable.json"))
        self.plates = json.load(open("../../assets/data/other/platesTable.json"))
        self.gems = json.load(open("../../assets/data/other/gemsTable.json"))
        self.incenses = json.load(open("../../assets/data/other/typeEnhancingIncences.json"))
        self.items = json.load(open("../../assets/data/other/typeEnhancingItems.json"))
        self.sheerforce_moves = json.load(open("../../assets/data/other/sheerForceTable.json"))

    @staticmethod
    def apply_mod(value, mod):
        return round((value * mod) / 0x1000)

    @staticmethod
    def chain_up(*mods):
        chained_mod = 0X1000
        for mod in mods:
            chained_mod = ((chained_mod * mod) + 0x800) >> 12
        return chained_mod

    def get_atk(self):
        ATKCAT = "atk" if self.move.category == "physical" else "aspe"
        ATKSTATUSER = self.pkmn2 if not self.move.dbSymbol == "foul_play" else self.pkmn2
        PARAMATK = ATKSTATUSER.get_stage_stat(ATKCAT) if not self.pkmn2.Ability.dbSymbol == "unaware" \
            else ATKSTATUSER.globalStats[ATKCAT]
        MODTF = 0x800 if (self.pkmn2.Ability.dbSymbol == "thick_fat" and
                          self.move.type.dbSymbol in ["ice", "fire"]) else 0x1000
        MODTRNT = 0x1800 if (self.pkmn1.Ability.dbSymbol == "torrent" and
                             self.pkmn1.currentHp <= self.pkmn1.globalStats["hp"] / 3 and
                             self.move.type.dbSymbol == "water") else 0x1000
        MODGUTS = 0x1800 if (self.pkmn1.Ability.dbSymbol == "guts" and
                             self.pkmn1.status["main"] and
                             self.move.category == "physical") else 0x1000
        MODSWA = 0x1800 if (self.pkmn1.Ability.dbSymbol == "swarm" and
                            self.pkmn1.currentHp <= self.pkmn1.globalStats["hp"] / 3 and
                            self.move.type.dbSymbol == "bug") else 0x1000
        MODOVG = 0x1800 if (self.pkmn1.Ability.dbSymbol == "overgrow" and
                            self.pkmn1.currentHp <= self.pkmn1.globalStats["hp"] / 3 and
                            self.move.type.dbSymbol == "grass") else 0x1000
        MODPLMI = 0x1800 if (self.pkmn1.Ability.dbSymbol in ["plus", "minus"] and
                             self.battleData["selfAlly"] and
                             self.battleData["selfAlly"].Ability.dbSymbol in ["plus", "minus"] and
                             self.move.category == "special") else 0x1000
        MODBLZ = 0x1800 if (self.pkmn1.Ability.dbSymbol == "blaze" and
                            self.pkmn1.currentHp <= self.pkmn1.globalStats["hp"] / 3 and
                            self.move.type.dbSymbol == "fire") else 0x1000
        MODDFT = 0x800 if (self.pkmn1.Ability.dbSymbol == "defeatist" and
                           self.pkmn1.currentHp <= self.pkmn1.globalStats["hp"] / 2) else 0x1000
        MODPHPW = 0x2000 if (self.pkmn1.Ability.dbSymbol in ["pure_power", "huge_power"] and
                             self.move.category == "physical") else 0x1000
        MODSLRP = 0x1800 if (self.pkmn1.Ability.dbSymbol == "solar_power" and
                             self.battleData["weather"] == "intense_sunlight" and
                             self.move.category == "special") else 0x1000
        MODATK1 = self.chain_up(MODTF, MODTRNT, MODGUTS, MODSWA, MODOVG, MODPLMI, MODBLZ, MODDFT, MODPHPW, MODSLRP)
        ATK = self.apply_mod(PARAMATK, MODATK1)

        MODHSTL = 0x1800 if (self.pkmn1.Ability.dbSymbol == "hustle" and
                             self.move.category == "physical") else 0x1000
        ATK = self.apply_mod(ATK, MODHSTL)

        MODFLFR = 0x1800 if (self.pkmn1.Ability.dbSymbol == "flash_fire" and
                             self.pkmn1.Ability.active and
                             self.move.type.dbSymbol == "fire") else 0x1000
        MODSLST = 0x800 if (self.pkmn1.Ability.dbSymbol == "slow_start" and
                            self.battleData["onFieldCounter"] < 5) else 0x1000
        MODFLGF = 0x1800 if (self.battleData["selfAlly"] and
                             self.battleData["selfAlly"].Ability.dbSymbol == "flower_gift" and
                             self.battleData["wheater"] == "intense_sunlight" and
                             self.move.category == "special") else 0x1000
        MODCLUB = 0x2000 if (self.pkmn1.dbSymbol in ["cubone", "marowak"] and
                             self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "thick_club" and
                             self.move.category == "physical") else 0x1000
        MODDST = 0x2000 if (self.pkmn1.dbSymbol == "clamperl" and
                            self.pkmn1.Item and
                            self.pkmn1.Item.dbSymbol == "deep_sea_tooth" and
                            self.move.category == "special") else 0x1000
        MODPIKA = 0x2000 if (self.pkmn1.dbSymbol == "pikachu" and
                             self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "light_ball") else 0x1000
        MODLATI = 0x1800 if (self.pkmn1.dbSymbol in ["latios", "latias"] and
                             self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "soul_dew" and
                             self.move.category == "special") else 0x1000
        MODCHBN = 0x1800 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "choice_band" and
                             self.move.category == "physical") else 0x1000
        MODCHSP = 0x1800 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "choice_specs" and
                             self.move.category == "special") else 0x1000
        MODATK2 = self.chain_up(MODFLFR, MODSLST, MODFLGF, MODCLUB, MODDST, MODPIKA, MODLATI, MODCHBN, MODCHSP)
        ATK = self.apply_mod(ATK, MODATK2)
        return ATK

    def get_defe(self):
        DEFECAT = "defe" if self.move.category == "physical" else "dspe"
        if self.move.dbSymbol in ["psyshock", "psystrike", "secret_sword"]:
            DEFECAT = "defe"
        if self.battleData["fieldStatus"] == "wonderRoom":
            if self.move.category == "physical":
                DEFECAT = "dspe"
            elif self.move.category == "special":
                DEFECAT = "defe"
        PARAMDEFE = self.pkmn2.get_stage_stat(DEFECAT)
        if self.pkmn1.Ability.dbSymbol == "unaware":
            PARAMDEFE = self.pkmn2.globalStats[DEFECAT]
        elif self.move.dbSymbol == "chip_away":
            PARAMDEFE = self.pkmn2.globalStats[DEFECAT]
        if (self.battleData["weather"] == "sandstorm" and
                "rock" in self.pkmn1.get_type() and
                self.move.category == "special"):
            PARAMDEFE = self.apply_mod(PARAMDEFE, 0x1800)
        MODMRVL = 0x1800 if (self.pkmn2.Ability.dbSymbol == "marvel_scale" and
                             self.pkmn2.status["main"] and
                             self.move.category == "special") else 0x1000
        MODTGFG = 0x1800 if (self.battleData["selfAlly"] and
                             self.battleData["selfAlly"].dbSymbol == "cherrim" and
                             self.battleData["selfAlly"].Ability.dbSymbol == "flower_gift" and
                             self.battleData["weather"] == "Harsh_sunlight" and
                             self.move.category == "special") else 0x1000
        MODDSS = 0x1800 if (self.pkmn2.dbSymbol == "clamperl" and
                            self.pkmn2.Item and
                            self.pkmn2.Item.dbSymbol == "deep_sea_scale" and
                            self.move.category == "special") else 0x1000
        MODDTTO = 0x2000 if (self.pkmn2.dbSymbol == "ditto" and
                             not self.pkmn2.Ability.active and
                             self.pkmn2.Item and
                             self.pkmn2.Item.dbSymbol == "metal_powder" and
                             self.move.category == "physical") else 0x1000
        MODEVIO = 0x1800 if (self.pkmn2.Item and
                             self.pkmn2.Item.dbSymbol == "eviolite" and
                             self.pkmn2.evolution) else 0x1000
        MODTGLA = 0x1800 if (self.pkmn2.dbSymbol in ["latios", "latias"] and
                             self.pkmn2.Item and
                             self.pkmn2.Item.dbSymbol == "soul_dew" and
                             self.move.category == "special") else 0x1000
        MODDEFE = self.chain_up(MODMRVL, MODTGFG, MODDSS, MODDTTO, MODEVIO, MODTGLA)
        DEFE = self.apply_mod(PARAMDEFE, MODDEFE)
        return DEFE

    def get_power(self):
        BASEPOWER = self.move.power
        if self.move.dbSymbol == "frustration":
            BASEPOWER = int(((255 - self.pkmn1.happiness) * 10) / 25)
        elif self.move.dbSymbol == "payback" and not self.battleData["firstToMove"]:
            BASEPOWER = 100
        elif self.move.dbSymbol == "return":
            BASEPOWER = int((self.pkmn1.happiness * 10) / 25)
        elif self.move.dbSymbol == "electro_ball":
            deltaSpeed = self.pkmn1.get_stage_stat("spd") / self.pkmn2.get_stage_stat("spd")
            BASEPOWER = {
                deltaSpeed >= 4: 150,
                4 > deltaSpeed >= 3: 120,
                3 > deltaSpeed >= 2: 80,
                2 > deltaSpeed >= 1: 60,
                deltaSpeed < 1: 40
            }[True]
        elif self.move.dbSymbol == "avalanche" and self.battleData["gotHit"]:
            BASEPOWER = 120
        elif self.move.dbSymbol == "gyro_ball":
            BASEPOWER = int(min(150, 25 * self.pkmn2.get_stage_stat("spd") / self.pkmn1.get_stage_stat("spd")))
        elif self.move.dbSymbol in ["eruption", "water_spout"]:
            BASEPOWER = int((150 * self.pkmn1.currentHp) / self.pkmn1.globalStats["hp"])
        elif self.move.dbSymbol == "punishment":
            sumboostlvl = sum(val for val in self.pkmn2.boosts.values() if val >= 0)
            BASEPOWER = min(120, 60 + 20 * sumboostlvl)
        elif self.move.dbSymbol == "fury_cutter":
            succes_streak = 0
            for i in range(len(self.battleData["selfMovesLogs"]) - 1, len(self.battleData["selfMovesLogs"]) - 4, -1):
                if (self.battleData["selfMovesLogs"][i]["move"] == "fury_cutter" and
                        self.battleData["selfMovesLogs"][i]["hit"]):
                    succes_streak += 1
                else:
                    break
            BASEPOWER = 20 * 2 ** succes_streak
        elif self.move.dbSymbol in ["low_kick", "grass_knot"]:
            weight = self.pkmn2.init_weight()
            result = {
                weight >= 200: 120,
                200 > weight >= 100: 100,
                100 > weight >= 50: 80,
                50 > weight >= 25: 60,
                25 > weight >= 10: 40,
                10 > weight: 20
            }
            BASEPOWER = result[True]
        elif self.move.dbSymbol == "echoed_voice":
            use_streak = 0
            for i in range(len(self.battleData["teamMovesLogs"]) - 1, len(self.battleData["teamMovesLogs"]) - 6, -1):
                if self.battleData["teamMovesLogs"][i]["move"] == "echoed_voice":
                    use_streak += 1
                else:
                    break
            result = [40, 80, 120, 160, 200]
            BASEPOWER = result[use_streak]
        elif self.move.dbSymbol == "hex" and self.pkmn2.status["main"]:
            BASEPOWER = 100
        elif self.move.dbSymbol in ["wring_out", "crush_grip"]:
            BASEPOWER = int(120 * (self.pkmn2.currentHp / self.pkmn2.globalStats["hp"]))
        elif self.move.dbSymbol == "assurance" and self.battleData["targetGotHit"]:
            BASEPOWER = 100
        elif self.move.dbSymbol in ["heavy_slam", "heat_crash"]:
            weight = self.pkmn1.init_weight() / self.pkmn2.init_weight()
            result = {
                weight >= 5: 120,
                5 > weight >= 4: 100,
                4 > weight >= 3: 80,
                3 > weight >= 2: 60,
                2 > weight: 40
            }
            BASEPOWER = result[True]
        elif self.move.dbSymbol == "stored_power":
            sumboostlvl = sum(val for val in self.pkmn1.boosts.values() if val >= 0)
            BASEPOWER = 20 + 20 * sumboostlvl
        elif self.move.dbSymbol == "acrobatics" and not self.pkmn1.Item:
            BASEPOWER = 110
        elif self.move.dbSymbol in ["flail", "reversal"]:
            p = (48 * self.pkmn1.currentHp) / self.pkmn1.globalStats["hp"]
            result = {
                p <= 1: 200,
                2 <= p <= 4: 150,
                5 <= p <= 9: 100,
                10 <= p <= 16: 80,
                17 <= p <= 32: 40,
                33 <= p: 20
            }
            BASEPOWER = result[True]
        elif self.move.dbSymbol == "trump_card":
            result = {
                self.move.pp == 5: 40,
                self.move.pp == 4: 50,
                self.move.pp == 3: 60,
                self.move.pp == 2: 80,
                self.move.pp == 1: 200
            }
            BASEPOWER = result[True]
        elif self.move.dbSymbol == "round" and self.battleData["selfAlly"] and self.battleData["allyJustUsedRound"]:
            BASEPOWER = 120
        elif self.move.dbSymbol == "triple_kick" and "trileKickStreak" in self.battleData:
            BASEPOWER = self.move.power * self.battleData["trileKickStreak"]
        elif self.move.dbSymbol == "wake_up_slap" and self.pkmn2.status["main"] == "asleep":
            BASEPOWER = 120
        elif self.move.dbSymbol == "smelling_salts" and self.pkmn2.status["main"] == "paralysis":
            BASEPOWER = 120
        elif self.move.dbSymbol == "weather_ball" and self.battleData["weather"]:
            BASEPOWER = 100
        elif self.move.dbSymbol in ["guts", "twister"] and self.battleData["targetInSky"]:
            BASEPOWER = 80
        elif self.move.dbSymbol == "beat_up":
            totalatk = [pkmn.baseStats["atk"]
                        for pkmn in self.battleData["selfTrainer"].team
                        if not pkmn.status["main"] or not pkmn.is_ko()]
            BASEPOWER = int(sum(totalatk) / 10 + 5)
        elif self.move.dbSymbol == "hidden_power":
            ivs_value = 0
            i = 0
            for iv in self.pkmn1.ivs.values():
                ivs_value += ((iv >> 1) & 1) << i
                i += 1
            BASEPOWER = int(30 + (40 * ivs_value) / 63)
        elif self.move.dbSymbol == "spit_up":
            BASEPOWER = 100 * self.battleData["selfSpitUpCounter"]
        elif self.move.dbSymbol == "pursuit" and self.battleData["targetSwitch"]:
            BASEPOWER = 80
        elif self.move.dbSymbol == "present":
            r = random.randint(0, 80)
            result = {
                r < 40: 40,
                40 <= r < 70: 80,
                r >= 70: 120
            }
            BASEPOWER = result[True]
        elif self.move.dbSymbol == "natural_gift":
            if self.pkmn1.Item and self.pkmn1.Item.dbSymbol in self.berries:
                BASEPOWER = self.berries[self.pkmn1.Item.dbSymbol]["naturalGiftPower"]
        elif self.move.dbSymbol == "magnitude":
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
        elif self.move.dbSymbol == "rollout":
            rollout_succes_streak = 0
            for i in range(len(self.battleData["selfMovesLogs"]) - 1, len(self.battleData["selfMovesLogs"]) - 6, -1):
                if self.battleData["selfMovesLogs"][i]["move"] == "rollout" and self.battleData["selfMovesLogs"][i][
                    "hit"]:
                    rollout_succes_streak += 1
                else:
                    break
            defense_curl = 0
            for self.move in self.battleData["selfMovesLogs"]:
                if self.move["move"] == "defense_curl":
                    defense_curl = 1
            BASEPOWER = 30 * 2 ** (rollout_succes_streak + defense_curl)
        elif self.move.dbSymbol == "fling" and self.pkmn1.Item:
            BASEPOWER = self.pkmn1.Item.flingPower
        elif (self.move.dbSymbol in ["grass_pledge", "fire_pledge", "water_pledge"] and
              self.battleData["selfAllyMove"].dbSymbol in ["grass_pledge", "fire_pledge", "water_pledge"] and
              self.battleData["selfAllyHasPlayed"]):
            BASEPOWER = 150
        MODTECH = 0x1800 if (self.pkmn1.Ability.dbSymbol == "technician" and
                             self.move.power <= 60) else 0x1000
        MODFBST = 0x1800 if (self.pkmn1.Ability.dbSymbol == "flare_boost" and
                             self.pkmn1.status["main"] == "burn" and
                             self.move.category == "special") else 0x1000
        MODANLT = 0x14CD if (self.pkmn1.Ability.dbSymbol == "analytic" and
                             self.move.dbSymbol not in ["future_sight", "doom_desire"] and
                             not self.battleData["firstToPlay"]) else 0x1000
        MODRCKL = 0x1333 if (self.pkmn1.Ability.dbSymbol == "reckless" and
                             (self.move.battleEngineMethod == "s_recoil" or
                              self.move.dbSymbol in ["jump_kick", "high_jump_kick"])) else 0x1000
        MODIFST = 0x1333 if (self.pkmn1.Ability.dbSymbol == "iron_fist" and
                             self.move.flags["isPunch"]) else 0x1000
        MODTBST = 0x1800 if (self.pkmn1.Ability.dbSymbol == "toxic_boost" and
                             self.pkmn1.status["main"] in ["poison", "badly_poisoned"] and
                             self.move.category == "physical") else 0x1000
        MODRVLY = 0x1000
        if self.pkmn1.Ability.dbSymbol == "rivalry":
            if not self.pkmn1.gender == "genderless" and not self.pkmn2.gender == "genderless":
                if self.pkmn1.gender == self.pkmn2.gender:
                    MODRVLY = 0x1400
                elif self.pkmn1.gender != self.pkmn2.gender:
                    MODRVLY = 0xC00
        MODSNDF = 0x14CD if (self.pkmn1.Ability.dbSymbol == "sand_force" and
                             self.move.type.dbSymbol in ["rock", "ground", "steel"]) else 0x1000
        MODHTPR = 0x800 if (self.pkmn1.Ability.dbSymbol == "heatproof" and
                            self.move.type.dbSymbol == "fire") else 0x1000
        MODDRYS = 0x1400 if (self.pkmn1.Ability.dbSymbol == "dry_skin" and
                             self.move.type.dbSymbol == "fire") else 0x1000
        MODSHRF = 0x14CD if (self.pkmn1.Ability.dbSymbol == "sheer_force" and
                             self.move.dbSymbol in self.sheerforce_moves) else 0x1000
        MODTYBS = 0x1333 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol in self.plates and
                             self.move.type.dbSymbol == self.plates[self.pkmn1.Item.dbSymbol]) or \
                            (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol in self.incenses and
                             self.move.type.dbSymbol == self.incenses[self.pkmn1.Item.dbSymbol]) or \
                            (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol in self.items and
                             self.move.type.dbSymbol == self.items[self.pkmn1.Item.dbSymbol]) else 0x1000
        MODMBND = 0x1199 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "muscle_band" and
                             self.move.category == "physical") else 0x1000
        MODPLK = 0x1333 if (self.pkmn1.dbSymbol == "palkia" and
                            self.pkmn1.Item and
                            self.pkmn1.Item.dbSymbol == "lustrous_orb" and
                            self.move.type.dbSymbol in ["water", "dragon"]) else 0x1000
        MODWGLS = 0x1199 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "wise_glasses" and
                             self.move.category == "special") else 0x1000
        MODGRTN = 0x1333 if (self.pkmn1.dbSymbol == "giratina" and
                             self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "griseous_orb" and
                             self.move.type.dbSymbol in ["ghost", "dragon"]) else 0x1000
        MODOINS = 0x1333 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol == "odd_incense" and
                             self.move.type.dbSymbol == "psychic") else 0x1000
        MODDLG = 0x1333 if (self.pkmn1.dbSymbol == "dialga" and
                            self.pkmn1.Item and
                            self.pkmn1.Item.dbSymbol == "adamant_orb" and
                            self.move.type.dbSymbol in ["steel", "dragon"]) else 0x1000
        MODGEMS = 0x1800 if (self.pkmn1.Item and
                             self.pkmn1.Item.dbSymbol in self.gems and
                             self.move.type.dbSymbol == self.gems[self.pkmn1.Item.dbSymbol]) else 0x1000
        MODFCD = 0x2000 if (self.move.dbSymbol == "facade" and
                            self.pkmn1.status["main"] in ["paralysis", "poison", "badly_poisoned", "burn"]) else 0x1000
        MODBRN = 0x2000 if (self.move.dbSymbol == "brine" and
                            self.pkmn2.currentHp <= self.pkmn2.globalStats["hp"]) else 0x1000
        MODVENO = 0x2000 if (self.move.dbSymbol == "venoshock" and
                             self.pkmn2.status["main"] in ["poison", "badly_poisoned"]) else 0x1000
        MODRETAL = 0x2000 if (self.move.dbSymbol == "retaliate" and
                              self.battleData["targetJustFainted"]) else 0x1000
        MODFUSIO = 0x2000 if (self.move.dbSymbol in ["fusion_bolt", "fusion_flare"] and
                              self.battleData["selfMovesLogs"][-1]["move"] == self.move.dbSymbol) else 0x1000
        MODFRST = 0x1800 if self.battleData["moveUsedByMeFirst"] else 0x1000
        MODSLRB = 0x800 if (self.move.dbSymbol == "solar_beam" and
                            self.battleData["weather"] and
                            self.battleData["weather"] not in ["harsh_sunlight",
                                                               "extremely_harsh_sunlight"]) else 0x1000
        MODCHRG = 0x2000 if (self.battleData["selfMovesLogs"] and
                             self.battleData["selfMovesLogs"][-1]["move"] == "charge" and
                             self.move.type.dbSymbol == "electric") else 0x1000
        MODHH = 0x1800 if self.battleData["selfHelpingHand"] else 0x1000
        MODWTRS = 0x548 if (({"move": "water_sport", "hit": True} in self.battleData["selfMovesLogs"] or
                             {"move": "water_sport", "hit": True} in self.battleData["targetMovesLogs"]) and
                            self.move.type.dbSymbol == "fire") else 0x1000
        MODMUDS = 0x548 if (({"move": "mud_sport", "hit": True} in self.battleData["selfMovesLogs"] or
                             {"move": "mud_sport", "hit": True} in self.battleData["targetMovesLogs"]) and
                            self.move.type.dbSymbol == "electric") else 0x1000
        MODPOWER = self.chain_up(MODTECH, MODFBST, MODANLT, MODRCKL, MODIFST, MODTBST, MODRVLY, MODSNDF, MODHTPR,
                                 MODDRYS, MODSHRF, MODTYBS, MODMBND, MODPLK, MODWGLS, MODGRTN, MODOINS, MODDLG, MODGEMS,
                                 MODFCD, MODBRN, MODVENO, MODRETAL, MODFUSIO, MODFRST, MODSLRB, MODCHRG, MODHH, MODWTRS,
                                 MODMUDS)
        POWER = self.apply_mod(BASEPOWER, MODPOWER)
        return POWER

    def get_weather_mod(self):
        if self.battleData.get_weather() == "rain":
            if self.move.init_type() == "water":
                return 0x1800
            elif self.move.init_type() == "fire":
                return 0x800
        elif self.battleData.get_weather() in ["harsh_sunlight", "extremely_harsh_sunlight"]:
            if self.move.init_type() == "water":
                return 0x800
            elif self.move.init_type() == "fire":
                return 0x1800

    def get_crit_mod(self):
        if not self.pkmn2.get_ability() in ["battle_armor", "shell_armor"] or self.battleData["selfLuckyChant"]:
            critical_hit_factors = [1 / 16, 1 / 8, 1 / 4, 1 / 3, 1 / 2]
            critical_rate = self.move.criticalRate
            if self.pkmn1.get_ability() == "super_luck":
                critical_rate += 1
            if self.pkmn1.dbSymbol == "Farfetch_d" and self.pkmn1.get_item() == "leek":
                critical_rate += 2
            elif self.pkmn1.dbSymbol == "chansey" and self.pkmn1.get_item() == "lucky_punch":
                critical_rate += 2
            if self.pkmn1.get_item() == "razor_claw":
                critical_rate += 1
            if random.random() <= critical_hit_factors[critical_rate - 1]:
                return 0X2000

    @staticmethod
    def get_r():
        return random.randint(85, 100)

    def get_stab_mod(self):
        if self.move.get_type() in self.pkmn1.get_type():
            if self.pkmn1.get_ability() == "adaptability":
                return 0x2000
            return 0x1800

    def get_type_effect_mod(self):
        return self.move.get_type_effectiveness(self.pkmn2)

    def get_burn_mod(self):
        if (self.move.category == "physical" and
                self.pkmn1.get_main_status() == "burn" and
                self.pkmn1.get_ability != "guts"):
            return 1

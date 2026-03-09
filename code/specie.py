import json

from type import Type


class Specie:
    def __init__(self, dbsymbol):
        data = json.load(open(f"../assets/data/pokemons/{dbsymbol.lower()}.json"))
        self.forms = data["forms"]

        self.id = data["id"]
        self.dbSymbol = data["dbSymbol"]
        self.name = data["dbSymbol"].title()
        self.height = self.forms[0]["height"]
        self.weight = self.forms[0]["weight"]

        self.femaleRate = self.forms[0]["femaleRate"]
        self.loyalty = self.forms[0]["baseLoyalty"]
        self.type = self.init_type()
        self.abilities = self.forms[0]["abilities"]
        self.itemHeld = self.forms[0]["itemHeld"]

        self.movepool = self.forms[0]["moveSet"]

        self.baseStats = {"hp": self.forms[0]["baseHp"],
                          "atk": self.forms[0]["baseAtk"],
                          "defe": self.forms[0]["baseDfe"],
                          "aspe": self.forms[0]["baseAts"],
                          "dspe": self.forms[0]["baseDfs"],
                          "spd": self.forms[0]["baseSpd"]
                          }

        self.evsDrop = {"hp": self.forms[0]["evHp"],
                        "atk": self.forms[0]["evAtk"],
                        "defe": self.forms[0]["evDfe"],
                        "aspe": self.forms[0]["evAts"],
                        "dspe": self.forms[0]["evDfs"],
                        "spd": self.forms[0]["evSpd"]
                        }

        self.expType = self.forms[0]["experienceType"]
        self.baseExperience = self.forms[0]["baseExperience"]
        self.evolution = self.forms[0]["evolutions"]

        self.breedGroups = self.forms[0]["breedGroups"]
        self.hatchSteps = self.forms[0]["hatchSteps"]
        self.babyDbSymbol = self.forms[0]["babyDbSymbol"]

        self.catchRate = self.forms[0]["catchRate"]

        self.frontOffsetY = self.forms[0]["frontOffsetY"]

    def init_type(self):
        if self.forms[0]["type2"] == "__undef__":
            return [Type(self.forms[0]["type1"])]
        return Type(self.forms[0]["type1"]), Type(self.forms[0]["type2"])

    def get_name(self):
        return self.name

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_ability(self):
        return self.abilities

    def get_item(self):
        return self.itemHeld

    def get_type(self):
        return (t.dbSymbol for t in self.type)

    def get_sprite_path(self, side, gender="male", shiny=False):
        path = f"../assets/graphics/pokemons/{side}/"
        if shiny:
            path += "shiny/"
        if gender == "female" and self.forms[0]["resources"]["hasFemale"]:
            if not self.forms[0]["femaleRate"] == 100:
                path += "female/"

        return path + f"{self.id}.png"

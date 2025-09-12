import json


class Type:
    def __init__(self, name):
        data = json.load(open(f"../assets/data/types/{name}.json"))
        self.dbSymbol = data["dbSymbol"]
        self.name = data["dbSymbol"]
        self.color = data["color"]

        self.factors = {
            "bug": 1,
            "dark": 1,
            "dragon": 1,
            "electric": 1,
            "fairy": 1,
            "fighting": 1,
            "fire": 1,
            "flying": 1,
            "ghost": 1,
            "grass": 1,
            "ground": 1,
            "ice": 1,
            "normal": 1,
            "poison": 1,
            "psychic": 1,
            "rock": 1,
            "steel": 1,
            "water": 1,
        }
        for type in data["damageTo"]:
            self.factors[type["defensiveType"]] = type["factor"]

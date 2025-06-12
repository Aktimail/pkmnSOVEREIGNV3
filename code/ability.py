import json


class Ability:
    def __init__(self, dbsymbol):
        data = json.load(open(f"../assets/data/abilities/{dbsymbol}.json"))

        self.dbSymbol = data["dbSymbol"]
        self.id = data["id"]

        self.active = False

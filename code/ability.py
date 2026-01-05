import json


class Ability:
    def __init__(self, dbsymbol):
        data = json.load(open(f"../assets/data/abilities/{dbsymbol.lower()}.json"))

        self.dbSymbol = data["dbSymbol"]
        self.id = data["id"]
        self.battleEngineMethod = data["dbSymbol"]

        self.active = False



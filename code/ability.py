import json

from battleEngineMethodRegistry import BEMRegistry


class Ability:
    def __init__(self, dbsymbol):
        data = json.load(open(f"../assets/data/abilities/{dbsymbol.lower()}.json"))

        self.dbSymbol = data["dbSymbol"]
        self.id = data["id"]
        self.bem = None  # BEMRegistry[data["battleEngineMethod"]] if data["battleEngineMethod"] else None

        self.active = False

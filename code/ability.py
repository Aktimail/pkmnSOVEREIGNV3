import json

from data import Data


class Ability:
    def __init__(self, dbsymbol):
        data = json.load(open(f"../assets/data/abilities/{dbsymbol.lower()}.json"))

        self.dbSymbol = data["dbSymbol"]
        self.id = data["id"]
        self.battleEngineMethod = self.init_bem(data["dbSymbol"])

        self.active = False

    @staticmethod
    def init_bem(bem_title):
        if Data.BATTLE_ENGINE_METHODS.get(bem_title):
            return Data.BATTLE_ENGINE_METHODS[bem_title]()
        return None



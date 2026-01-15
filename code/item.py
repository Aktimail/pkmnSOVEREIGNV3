import json

from data import Data


class Item:
    def __init__(self, dbsymbol):
        super().__init__()
        data = json.load(open(f"../assets/data/items/{dbsymbol.lower()}.json"))

        self.id = data["id"]
        self.dbSymbol = data["dbSymbol"]
        self.icon = data["icon"]
        self.price = data["price"]
        self.socket = data["socket"]
        self.isHoldable = data["isHoldable"]
        self.isBattleUsable = data["isBattleUsable"]
        self.isMapUsable = data["isMapUsable"]
        self.isLimited = data["isLimited"]
        self.flingPower = data["flingPower"]
        self.battleEngineMethod = (data["dbSymbol"])

    @staticmethod
    def init_bem(bem_title):
        if Data.BATTLE_ENGINE_METHODS.get(bem_title):
            return Data.BATTLE_ENGINE_METHODS[bem_title]()
        return None


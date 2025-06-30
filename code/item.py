import json


class Item:
    def __init__(self, dbsymbol):
        super().__init__()
        data = json.load(open(f"../assets/data/items/{dbsymbol}.json"))

        self.dbSymbol = data["dbSymbol"]
        self.id = data["id"]
        self.UID = 0
        self.icon = data["icon"]
        self.price = data["price"]
        self.socket = data["socket"]
        self.isHoldable = data["isHoldable"]
        self.isBattleUsable = data["isBattleUsable"]
        self.isMapUsable = data["isMapUsable"]
        self.isLimited = data["isLimited"]
        self.flingPower = data["flingPower"]

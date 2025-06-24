import json
from type import Type


class Move:
    def __init__(self, name):
        data = json.load(open(f"../assets/data/moves/{name}.json"))

        self.klass = data["klass"]
        self.id = data["id"]
        self.dbSymbol = data["dbSymbol"]
        self.name = data["dbSymbol"].title()
        self.type = Type(data["type"])

        self.power = data["power"]
        self.accuracy = data["accuracy"]
        self.pp = data["pp"]
        self.maxPp = self.pp
        self.category = data["category"]

        self.criticalRate = data["movecriticalRate"]
        self.priority = data["priority"]
        self.features = {
            "isDirect": data["isDirect"],
            "isCharge": data["isCharge"],
            "isRecharge": data["isRecharge"],
            "isBlocable": data["isBlocable"],
            "isSnatchable": data["isSnatchable"],
            "isMirrorMove": data["isMirrorMove"],
            "isPunch": data["isPunch"],
            "isGravity": data["isGravity"],
            "isMagicCoatAffected": data["isMagicCoatAffected"],
            "isUnfreeze": data["isUnfreeze"],
            "isSoundAttack": data["isSoundAttack"],
            "isDistance": data["isDistance"],
            "isHeal": data["isHeal"],
            "isAuthentic": data["isAuthentic"],
            "isBite": data["isBite"],
            "isPulse": data["isPulse"],
            "isBallistics": data["isBallistics"],
            "isMental": data["isMental"],
            "isNonSkyBattle": data["isNonSkyBattle"],
            "isDance": data["isDance"],
            "isKingRockUtility": data["isKingRockUtility"],
            "isPowder": data["isPowder"],
        }
        self.effectChance = data["effectChance"]
        self.target = data["battleEngineAimedTarget"]
        self.boosts = self.get_boosts(data["battleStageMod"])
        self.status = data["moveStatus"]
        self.battleEngineMethod = data["battleEngineMethod"]

    @staticmethod
    def get_boosts(data):
        if data:
            boosts = {}
            stats_trad = {"ATK_STAGE": "atk",
                          "DFE_STAGE": "defe",
                          "ATS_STAGE": "aspe",
                          "DFS_STAGE": "dspe",
                          "SPD_STAGE": "spd",
                          "ACC_STAGE": "acc",
                          "EVA_STAGE": "eva"}
            for mod in data:
                for stat in stats_trad:
                    if mod["battleStage"] == stat:
                        boosts[stats_trad[stat]] = mod["modificator"]
            return boosts
        return None

    def save_move(self):
        return {
            "name": self.name,
            "pp": self.pp
        }

    def load_move(self, data):
        self.pp = data["pp"]

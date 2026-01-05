from battleEngineMethod import *


class BattleEngineMethodManager:

    BATTLE_ENGINE_METHODS = {
        "frustration": FrustrationMethod,
        "heatproof": HeatProofMethod
    }

    def __init__(self):
        self.registry = []

    def register(self, method):
        if method in self.BATTLE_ENGINE_METHODS.keys():
            BEM = self.BATTLE_ENGINE_METHODS[method]()
            if not BEM in self.registry:
                self.registry.append(BEM)

    def emit(self, trigger):
        return sorted([method for method in self.registry if method.TRIGGER == trigger], key=lambda m: m.PRIORITY)

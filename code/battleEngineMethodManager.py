from battleEngineMethod import *


class BattleEngineMethodManager:
    def __init__(self):
        self.registry = []

    def register(self, bem):
        if bem and bem not in self.registry:
            self.registry.append(bem)

    def emit(self, trigger):
        return sorted([method for method in self.registry if method.trigger == trigger], key=lambda m: m.priority)
